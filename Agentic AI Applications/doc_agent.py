import os
import json
import base64
import litellm
import requests
import instructor
import numpy as np
from loguru import logger
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import google.generativeai as genai 
from pydantic import BaseModel, Field
from PIL import Image, ImageDraw, ImageFont
from typing import List, Optional, Tuple, Dict, Any
 
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  
class BoundingBox(BaseModel):
    x1: float = Field(..., description="Top-left x coordinate (normalized 0-1)")
    y1: float = Field(..., description="Top-left y coordinate (normalized 0-1)")
    x2: float = Field(..., description="Bottom-right x coordinate (normalized 0-1)")
    y2: float = Field(..., description="Bottom-right y coordinate (normalized 0-1)")

    def to_pixel_coords(self, width: int, height: int) -> Tuple[int, int, int, int]:
        """Convert normalized coordinates to pixel coordinates"""
        return (
            int(self.x1 * width),
            int(self.y1 * height),
            int(self.x2 * width),
            int(self.y2 * height)
        )

class LayoutElement(BaseModel):
    element_type: str = Field(..., description="Type of document element")
    confidence: float = Field(..., description="Detection confidence score")
    bbox: BoundingBox = Field(..., description="Normalized bounding box coordinates")
    text_content: Optional[str] = Field(None, description="Text content if available")

class DocumentLayout(BaseModel):
    elements: List[LayoutElement] = Field(..., description="List of detected layout elements")
    width: int = Field(..., description="Document width in pixels")
    height: int = Field(..., description="Document height in pixels")

class DocumentLayoutDetector:
    def __init__(self, use_litellm=True):
        self.use_litellm = use_litellm
        
        # Initialize instructor client with litellm
        self.client = instructor.from_litellm(litellm.completion)

        # Define the layout element classes we want to detect
        self.layout_classes = [
            "header", "footer", "paragraph", "title", "table",
            "figure", "list", "caption", "page_number", "signature"
        ]

        # Configure API settings
        if use_litellm:
            AZURE_API_KEY = ""
            AZURE_API_BASE = ""
            AZURE_API_VERSION = ""

    def encode_image(self, image_path):
        """Encode image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def detect_layout(self, image_path: str) -> DocumentLayout:
        """Detect layout elements in a document image"""
        # Load image and get original dimensions
        image = Image.open(image_path)
        
        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        original_width, original_height = image.size
        
        # Resize image if too large (keeping aspect ratio)
        max_size = 1600  # Maximum dimension
        if max(original_width, original_height) > max_size:
            ratio = max_size / max(original_width, original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"Resized image from {original_width}x{original_height} to {new_width}x{new_height}")
        
        # Save resized image temporarily
        temp_path = "temp_resized.jpg"
        try:
            image.save(temp_path, "JPEG", quality=95)
            
            # Process image with VLM
            elements = self._process_with_llm(temp_path)
            
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            # Scale bounding boxes back to original dimensions if image was resized
            if max(original_width, original_height) > max_size:
                for element in elements:
                    # Scale bbox coordinates back to original dimensions
                    element.bbox.x1 = element.bbox.x1 * (original_width / new_width)
                    element.bbox.y1 = element.bbox.y1 * (original_height / new_height)
                    element.bbox.x2 = element.bbox.x2 * (original_width / new_width)
                    element.bbox.y2 = element.bbox.y2 * (original_height / new_height)
            
            return DocumentLayout(
                elements=elements,
                width=original_width,
                height=original_height
            )
        except Exception as e:
            logger.error(f"Error in detect_layout: {e}")
            # Clean up temporary file in case of error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

    def _process_with_llm(self, image_path: str) -> List[LayoutElement]:
        """Process image with Vision Language Model to detect layout elements"""
        # Encode image to base64
        base64_image = self.encode_image(image_path)

        # Prepare the system prompt
        system_prompt = (
            "You are a document layout analysis expert. Analyze the provided document image and "
            "identify different layout elements with their bounding boxes. "
            "For each element, provide the element type, bounding box coordinates (normalized 0-1), "
            "and a confidence score."
        )

        # Prepare the user prompt
        user_prompt = (
            f"Detect and classify document layout elements with bounding boxes. "
            f"For each element, provide the element type, bounding box coordinates (normalized 0-1), "
            f"and confidence score. Element types include: {', '.join(self.layout_classes)}. "
            f"Return the results in a JSON format with a list of elements, where each element has "
            f"'element_type', 'confidence', 'bbox' (with x1, y1, x2, y2 normalized coordinates), "
            f"and 'text_content' (if visible text is present)."
        )

        # Call the LLM
        if self.use_litellm:
            response = self._call_with_litellm(base64_image, system_prompt, user_prompt)
        else:
            response = self._call_azure_openai(base64_image, system_prompt, user_prompt)

        # Parse the response
        return self._parse_llm_response(response)

    def _call_with_litellm(self, base64_image, system_prompt, user_prompt):
        """Call LLM using LiteLLM with Instructor"""
        try:
            # Define the response model using Pydantic with more specific bbox structure
            class BBoxCoordinates(BaseModel):
                x1: float = Field(..., ge=0.0, le=1.0)
                y1: float = Field(..., ge=0.0, le=1.0)
                x2: float = Field(..., ge=0.0, le=1.0)
                y2: float = Field(..., ge=0.0, le=1.0)

            class Element(BaseModel):
                element_type: str
                confidence: float = Field(..., ge=0.0, le=1.0)
                bbox: BBoxCoordinates
                text_content: Optional[str] = None

            class DocumentResponse(BaseModel):
                elements: List[Element]

            # Update the user prompt to be more specific about bbox format
            enhanced_prompt = (
                f"{user_prompt}\n"
                "Important: Bounding box coordinates must be normalized between 0 and 1, where:\n"
                "- x1,y1 is the top-left corner\n"
                "- x2,y2 is the bottom-right corner\n"
                "- Coordinates should be in the format: {'x1': float, 'y1': float, 'x2': float, 'y2': float}\n"
                "Example bbox: {'x1': 0.1, 'y1': 0.2, 'x2': 0.3, 'y2': 0.4}"
            )

            # Prepare messages
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": enhanced_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]

            # Use instructor to handle the response
            response = self.client.chat.completions.create(
                model="bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                # model="bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                # model="gemini/gemini-2.0-flash",
                response_model=DocumentResponse,
                messages=messages,
                max_tokens=4000
            )

            # Convert the validated response to JSON
            return json.dumps(response.model_dump())

        except Exception as e:
            logger.error(f"Error calling LiteLLM with Instructor: {e}")
            logger.error(f"Full error details: {str(e)}")
            return None

    def _parse_llm_response(self, response_text: str) -> List[LayoutElement]:
        """Parse LLM response to extract layout elements"""
        if not response_text:
            return []
        
        logger.info(f"Raw response: {response_text}")

        try:
            # Parse the JSON
            data = json.loads(response_text)
            elements_data = data.get("elements", [])

            # Convert to LayoutElement objects
            elements = []
            for elem_data in elements_data:
                try:
                    bbox_data = elem_data.get("bbox", {})
                    
                    # Ensure bbox values are within 0-1 range
                    bbox = BoundingBox(
                        x1=max(0.0, min(1.0, float(bbox_data.get("x1", 0.0)))),
                        y1=max(0.0, min(1.0, float(bbox_data.get("y1", 0.0)))),
                        x2=max(0.0, min(1.0, float(bbox_data.get("x2", 1.0)))),
                        y2=max(0.0, min(1.0, float(bbox_data.get("y2", 1.0))))
                    )

                    # Ensure x1 < x2 and y1 < y2
                    if bbox.x1 > bbox.x2:
                        bbox.x1, bbox.x2 = bbox.x2, bbox.x1
                    if bbox.y1 > bbox.y2:
                        bbox.y1, bbox.y2 = bbox.y2, bbox.y1

                    # Create LayoutElement
                    element = LayoutElement(
                        element_type=elem_data.get("element_type", "unknown"),
                        confidence=max(0.0, min(1.0, float(elem_data.get("confidence", 0.0)))),
                        bbox=bbox,
                        text_content=elem_data.get("text_content")
                    )
                    elements.append(element)
                    
                except Exception as e:
                    logger.error(f"Error processing element {elem_data}: {e}")
                    continue

            return elements

        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            logger.error(f"Response text: {response_text}")
            return []

def visualize_layout(document_layout: DocumentLayout, image_path: str, output_path: str = None):
    """Visualize detected layout elements on the document image"""
    # Load the original image
    image = Image.open(image_path)
    
    # If image has alpha channel (RGBA), convert to RGB
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 10)
    except IOError:
        font = ImageFont.load_default()
    
    # Define colors for different element types (RGB)
    colors = {
        "header": (255, 0, 0),      # Red
        "footer": (0, 0, 255),      # Blue
        "paragraph": (0, 255, 0),   # Green
        "title": (255, 0, 255),     # Magenta
        "table": (255, 165, 0),     # Orange
        "figure": (128, 0, 128),    # Purple
        "list": (0, 255, 255),      # Cyan
        "caption": (255, 255, 0),   # Yellow
        "page_number": (165, 42, 42), # Brown
        "signature": (0, 128, 128)  # Teal
    }
    
    # Draw bounding boxes for each element
    for element in document_layout.elements:
        # Get pixel coordinates
        x1, y1, x2, y2 = element.bbox.to_pixel_coords(document_layout.width, document_layout.height)
        
        # Get color for this element type (default to gray if not in our color map)
        color = colors.get(element.element_type, (128, 128, 128))
        
        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        
        # Draw label
        label = f"{element.element_type} ({element.confidence:.2f})"
        draw.text((x1, max(0, y1-20)), label, fill=color, font=font)
    
    # Save or display the result
    if output_path:
        # Ensure we're saving as PNG if the path ends with .png, otherwise save as JPEG
        if output_path.lower().endswith('.png'):
            image.save(output_path, format='PNG')
        else:
            # If not PNG, ensure we're saving as JPEG with RGB mode
            if not output_path.lower().endswith('.jpg') and not output_path.lower().endswith('.jpeg'):
                output_path += '.jpg'
            image.save(output_path, format='JPEG')
        
        print(f"Visualization saved to {output_path}")
        # Created/Modified files during execution:
        print(f"Created file: {output_path}")
    
    # Display the image
    plt.figure(figsize=(12, 12))
    plt.imshow(np.array(image))
    plt.axis('off')
    plt.show()

def main():
    # Initialize the detector
    # Set use_litellm=True to use LiteLLM, False to use Azure OpenAI directly
    detector = DocumentLayoutDetector(use_litellm=True)

    # Path to document image
    image_path = "./media/yogi/WORK_SPACE/GenAI_Solutions/Data/test_new.png"

    # Check if the image exists
    if not os.path.exists(image_path):
        print(f"Sample image not found at {image_path}. Please provide a valid document image.")
        return

    # Detect layout
    document_layout = detector.detect_layout(image_path)

    # Print detected elements
    print(f"Detected {len(document_layout.elements)} layout elements:")
    for i, element in enumerate(document_layout.elements):
        print(f"{i+1}. {element.element_type} (confidence: {element.confidence:.2f})")
        print(f"   Bounding box: {element.bbox}")
        if element.text_content:
            print(f"   Text: {element.text_content[:50]}...")
        print()

    # Save results to JSON file
    output_json = "layout_detection_result.json"
    with open(output_json, "w") as f:
        # Updated to use model_dump with json formatting
        json_str = json.dumps(document_layout.model_dump(), indent=2)
        f.write(json_str)
    print(f"Results saved to {output_json}")
    # Created/Modified files during execution:
    print(f"Created file: {output_json}")

    # Visualize layout
    output_image = "layout_detection_result.jpg"
    visualize_layout(document_layout, image_path, output_image)

if __name__ == "__main__":
    main()