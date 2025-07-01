import boto3
import json
from botocore.exceptions import ClientError

def upload_downlaod_file(bucket_name, file_path, object_key):
    try:
        s3_client = boto3.client('s3')
        # Upload file to bucket
        s3_client.upload_file(
            Filename=file_path,
            Bucket=bucket_name,
            Key=object_key,
            ExtraArgs={
                'ContentType': 'application/json',
                'Metadata': {'environment': 'production'}
            }
        )
        print(f"uploaded {file_path} to s3://{bucket_name}/{object_key}")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    upload_downlaod_file("my-devops-bucket-2025", "/home/deepesh-barod/Downloads/Devops/Boto3/Lib/OS/test.py", "test.py")
