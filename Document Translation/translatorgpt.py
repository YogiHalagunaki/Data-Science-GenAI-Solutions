import fitz  # PyMuPDF for PDF handling
from io import BytesIO
import streamlit as st
from googletrans import Translator  # Translation API


# Upload PDF
st.title("PDF Translation Service")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
target_language = st.selectbox("Select Target Language", ["en", "fr", "de", "es"])  # Add languages as needed

if uploaded_file:
    # Open the uploaded PDF
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    # Initialize translator
    translator = Translator()
    translated_pdf = BytesIO()

    # Character width approximation for Helvetica font
    char_width_approx = 0.5  # Adjust as needed based on font scaling

    # Create a new PDF for the translated pages
    with fitz.open() as new_pdf:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text_instances = page.get_text("blocks")  # Get text with position data

            # Add original page to new PDF as background
            new_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

            # Load the newly added page as overlay
            overlay_page = new_pdf[page_num]
            overlay_page.clean_contents()  # Clean contents to overlay translated text

            # Translate and overlay text, replacing the original
            for block in text_instances:
                if len(block) >= 5:  # Ensure block has at least 5 elements
                    x, y, width, height = block[0], block[1], block[2] - block[0], block[3] - block[1]
                    original_text = block[4]  # Get the text part
                    
                    # Translate text
                    translated_text = translator.translate(original_text, dest=target_language).text
                    
                    # Calculate approximate font size based on block height
                    font_size = min(12, max(8, height / 2.5))
                    
                    # Draw a white rectangle to cover original text
                    overlay_page.draw_rect(fitz.Rect(x, y, x + width, y + height), color=(1, 1, 1), fill=True)

                    # Approximate characters per line based on width and font size
                    max_chars_per_line = int(width / (char_width_approx * font_size))
                    
                    # Wrap text manually to fit within the width
                    wrapped_text = ""
                    line = ""
                    
                    for word in translated_text.split():
                        test_line = line + word + " "
                        if len(test_line) <= max_chars_per_line:
                            line = test_line
                        else:
                            wrapped_text += line.strip() + "\n"  # Move to next line
                            line = word + " "
                    
                    wrapped_text += line.strip()  # Add remaining text

                    # Calculate vertical offset to center text vertically in the box
                    lines = wrapped_text.split("\n")
                    text_height = len(lines) * font_size * 1.2  # Estimate total text height
                    y_offset = y + (height - text_height) / 2  # Center vertically

                    # Insert each line with proper positioning
                    for i, line in enumerate(lines):
                        overlay_page.insert_text((x, y_offset + i * font_size * 1.2), line, fontsize=font_size, fontname="helv", color=(0, 0, 0))

        # Save the translated PDF to BytesIO for download
        new_pdf.save(translated_pdf)
        translated_pdf.seek(0)

    # Display download button
    st.download_button(
        label="Download Translated PDF",
        data=translated_pdf,
        file_name="translated_document.pdf",
        mime="application/pdf"
    )
st.markdown("---")
st.markdown("Developed with ❤️ by Yogi Halaguanki")
