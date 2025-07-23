from botocore.exceptions import ClientError

from utils.config import logger

async def get_file_object_s3(s3_client, bucket: str, object_name: str):
    '''
    Retrieve file object from S3 bucket
    Param-
    s3_client: AWS S3 client created using boto3
    bucket: Name of the S3 bucket
    object_name: Name of the file in S3 bucket
    '''
    # create object of file in S3 bucket
    try:
        s3_response_object = s3_client.get_object(
            Bucket=bucket,
            Key=object_name
        )
        object_content = s3_response_object['Body'].read()
        return object_content
    except ClientError as e:
        logger.error(f"ClientError: get_file_object_s3, {e}")
        if e.response['Error']['Code'] == 'NoSuchKey':
            logger.info('No object found - returning empty')
            return None
        else:
            raise

async def get_file_list_s3(s3_client, bucket: str, prefix: str='') -> list:
    '''
    List all file from an S3 bucket
    Param-
    s3_client: AWS S3 client created using boto3
    bucket: Name of the S3 bucket
    prefix: Name of the file in S3 bucket
    '''
    try:
        # list all objects
        objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        lst_obj = [obj['Key'] for obj in objects['Contents']]
        return lst_obj
    except ClientError as e:
        logger.error(f"ClientError: get_file_list_s3, {e}")
        return None
    except Exception as e:
        logger.error(f"Exception: get_file_list_s3, {e}")
        return None

async def upload_file_s3(s3_client, file_path: str, bucket: str, object_name: str) -> bool:
    '''
    List all file from an S3 bucket
    Param-
    s3_client: AWS S3 client created using boto3
    file_path: Path to the local document
    bucket: Name of the S3 bucket
    object_name: Name of the file in S3 bucket
    '''
    try:
        response = s3_client.upload_file(
            Filename = file_path,       # The path to the file to upload
            Bucket = bucket,            # The name of the bucket to upload to
            Key = object_name           # The name of the key to upload to
        )
        if response:
            return True
        else:
            logger.info(f"response_upload_file_s3: {response.text}")
            return False
    except ClientError as e:
        logger.error(f"ClientError: upload_file_s3, {e}")
        return False
    except Exception as e:
        logger.error(f"Exception: upload_file_s3, {e}")
        return False
