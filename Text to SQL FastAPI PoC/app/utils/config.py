import os
# from codes.access_secrets import AccessSecrets
from utils.custom_logger import get_logger

logger = get_logger(__name__)

try:

    # Database path
    DB_PATH= os.getenv("DB_PATH", "/home/yogi/DBDA_HOME/database.db")

    # OpenAI API Key (optional)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

    # Server config
    HOST=127.0.0.1
    PORT=8000
    
except Exception as e:
    logger.error(f"Environment variables configuration access issue............. {e}")

