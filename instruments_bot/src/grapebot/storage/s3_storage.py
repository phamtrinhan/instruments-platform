import boto3

from botocore.exceptions import ClientError
import os
import logging
import pathlib
from grapebot.storage import local as storage_local

BASE_DIR = pathlib.Path(__file__).parent.resolve()
BUCKET_NAME = os.getenv('AWS_S3_BUCKET') if os.getenv('AWS_S3_BUCKET') else 'grapechain'

IGNORE_FILE = ['.DS_Store']


def get_client_aws():
    client = boto3.client("s3", region_name=os.getenv('AWS_REGION'))
    try:
        client.list_buckets()
    except Exception as e:
        logging.error('Client AWS error ', e)
        return None

    return client


def get_s3_resource():
    s3 = boto3.resource('s3')
    return s3


# def dir_in_s3(bucket=os.getenv('AWS_S3_BUCKET')):
#     s3_client = get_s3_resource()
#     obj = s3_client.Object()
#     obj.get()['Body'].read().decode('utf-8')


def upload_files_to_s3(file_name, object_name=None, bucket=BUCKET_NAME, args=None):
    if not storage_local.check_file_exist(file_name):
        logging.error("Can't upload to S3 from {path}".format(path=file_name))
        raise Exception("File not found")
    s3_client = get_client_aws()
    file_path = f"{BASE_DIR}/../../../{file_name}"
    if not s3_client:
        raise Exception
    if object_name is None:
        object_name = file_name
    try:
        s3_client.upload_file(file_path, bucket, object_name, ExtraArgs=args)
    except Exception as e:
        logging.error("Fail to upload file "+ e)
        raise Exception("Fail to upload file {path}".format(path=file_name))
    return True


def upload_folder_to_s3(input_path, output_path=None, bucket=BUCKET_NAME):

    s3_client = get_client_aws()
    folder_path = f"{BASE_DIR}/../../../{input_path}"
    if output_path is None:
        output_path = input_path
    try:
        for path, subdirs, files in os.walk(folder_path):
            for file in files:
                if file not in IGNORE_FILE:
                    dest_path = path.replace(folder_path, "")
                    __s3file = os.path.normpath(output_path + '/' + dest_path + '/' + file)
                    __local_file = os.path.join(path, file)
                    s3_client.upload_file(__local_file, bucket, __s3file)
    except Exception as e:
        logging.info("Upload folder failed: ", e)
        raise Exception("Upload folder failed")


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    
    # The response contains the presigned URL
    return response