import boto3

s3_client = boto3.client(
    's3',
    endpoint_url="http://127.0.0.1:9000",  # MinIO endpoint
    aws_access_key_id="minio",  # Replace with your access key
    aws_secret_access_key="minio123",  # Replace with your secret key
)


bucket_name = "mybucket"
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f"Found object: {obj['Key']} (Size: {obj['Size']} bytes)")
    else:
        print(f"No objects found in bucket: {bucket_name}")
except Exception as e:
    print(f"Error listing objects: {e}")

object_key = 'data.csv'

object_keys = []


for i in range(0, 100):
    file_name = f"data{i}.csv"
    print(file_name)
    object_keys.append(file_name)

print(object_keys)

try:
    # Fetch the object
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    
    print(response)
    # Read the content of the object
    file_content = response["Body"].read().decode("utf-8")
    print(f"Content of '{object_key}':\n{file_content}")
except Exception as e:
    print(f"Error fetching object '{object_key}': {e}")
    
