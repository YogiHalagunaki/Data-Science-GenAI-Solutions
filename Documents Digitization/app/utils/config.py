import asyncio
import os
import boto3

from utils.custom_logger import get_logger
logger = get_logger("Documents Digitization Process", file_handler=False)

from utils.access_secrets import AccessSecrets

try:
    # loop = asyncio.get_event_loop()

    vault_url = os.environ["vault_url"]
    client_id_managed_identity = os.environ["client_id_managed_identity"]

    # MongoDB Configs
    mdb_db = os.getenv("cosmos_mdb_db", "skns_db_tvlbuddy")
    mdb_collection_data = os.getenv("cosmos_mdb_collection_data", "documents")
    mdb_conn_str = os.getenv("mdb_conn_str")
    #mdb_conn_str = AccessSecrets.get_secret("cosmos-mdb-conn-str")

    # AWS S3 Configs
    s3_bucket_input = os.getenv("aws_s3_bucket_input", "travelbuddyappian")
    s3_access_key_id = os.getenv("s3_access_key_id")
    #s3_access_key_id = AccessSecrets.get_secret("aws-s3-access-key-id")
    s3_secret_access_key = os.getenv("s3_secret_access_key")
    #s3_secret_access_key = AccessSecrets.get_secret("aws-s3-secret-access-key")
    boto3_client = boto3.client(
        's3',
        aws_access_key_id = s3_access_key_id,
        aws_secret_access_key = s3_secret_access_key
    )

    # storage account
    storage_ac_conn_str = os.getenv("storage_ac_conn_str")
    #storage_ac_conn_str = AccessSecrets.get_secret("storage-ac-conn-str")  

    # event hub
    eventhub_name = os.getenv("eventhub_name")
    eventhub_checkpoint_container = os.getenv("eventhub_checkpoint_container")
    eventhub_conn_str_listen = os.getenv("eventhub_conn_str_listen")
    #eventhub_conn_str_listen = AccessSecrets.get_secret("eventhub-conn-str-listen")

    max_event_batch_size = int(os.getenv("eh_max_batch_size_eventhub", "10"))
    max_api_tries = int(os.getenv("eh_max_api_tries","3"))
    backoff_factor = int(os.getenv("eh_backoff_factor","10"))
    retry_exp_wait_multiplier = int(os.environ.get("eh_retry_exp_wait_multiplier","1"))
    retry_wait_max = int(os.getenv("eh_retry_wait_max","60"))

    # module specific configs
    llm_model_name = os.getenv("llm_model_name", "azure/gpt-35-turbo-16k")

    azure_openai_api_key = os.getenv("azure_openai_api_key")
    #azure_openai_api_key = AccessSecrets.get_secret("azure-openai-api-key")
    azure_openai_api_base = os.getenv("azure_openai_api_base")
    azure_openai_api_version = os.getenv("azure_openai_api_version")
    os.environ["AZURE_API_KEY"] = azure_openai_api_key
    os.environ["AZURE_API_BASE"] = azure_openai_api_base
    os.environ["AZURE_API_VERSION"] = azure_openai_api_version

    cognitive_services_subscription_key = os.getenv("cognitive_services_subscription_key")
    #cognitive_services_subscription_key = AccessSecrets.get_secret("cognitive-services-subscription-key")
    cognitive_services_base_url = os.getenv("cognitive_services_base_url")
    cognitive_services_endpoint = os.getenv("cognitive_services_endpoint")

    # Appian API Details
    appian_api_key = os.getenv("appian_api_key")
    appian_api_url = os.getenv("appian_api_url")

except:
    logger.error("Exception while retrieving environment variables!")
