import os
# from codes.access_secrets import AccessSecrets
from utils.custom_logger import get_logger

logger = get_logger(__name__)

try:

    db_url = os.getenv("DB_URL", "./tmp/lancedb")

    llm_model = os.getenv("LLM_MODEL", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")    
    
    # Azure credentials
    subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY")
    azure_region = os.getenv("AZURE_REGION")
    vision_base_url = os.getenv("VISION_BASE_URL")
 
except Exception as e:
    logger.error(f"Environment variables configuration access issue............. {e}")


