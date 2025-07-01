
# Client Methods (boto3.client('s3')):
1) `create_bucket(Bucket, CreateBucketConfiguration)`: Creates an S3 bucket.
`Bucket`: Name of the bucket (string).
`CreateBucketConfiguration`: Dict with LocationConstraint (e.g., 'us-east-1').

2) `put_object(Bucket, Key, Body, **kwargs)`: Uploads an object to a bucket.
`Bucket`: Target bucket name.
`Key`: Object key (path in bucket).
`Body`: Data to upload (string, bytes, or file-like object).
`**kwargs`: Optional args like ContentType, ServerSideEncryption.

3) `get_object(Bucket, Key, **kwargs)`: Retrieves an object.
`Bucket`: Bucket name.
`Key`: Object key.
`**kwargs`: Optional args like Range for partial downloads.

4) `delete_object(Bucket, Key)`: Deletes an object.
`Bucket`: Bucket name.
`Key`: Object key.

5) `list_objects_v2(Bucket, Prefix, Delimiter, MaxKeys)`: Lists objects in a bucket.
`Bucket`: Bucket name.
`Prefix`: Filters objects by prefix (optional).
`Delimiter`: Groups objects by common prefix (optional).
`MaxKeys`: Maximum number of objects to return (integer).

6) `put_bucket_policy(Bucket, Policy)`: Applies a bucket policy.
`Bucket`: Bucket name.
`Policy`: JSON policy string.

7) `put_bucket_encryption(Bucket, ServerSideEncryptionConfiguration)`: Sets bucket encryption.
`Bucket`: Bucket name.
`ServerSideEncryptionConfiguration`: Dict specifying encryption rules.


# Resource Methods (boto3.resource('s3')):
`Bucket(name)`: Accesses a specific bucket.
- name: Bucket name.

`Object(bucket_name, key)`: Accesses a specific object.
- bucket_name`: Bucket name.
- key: Object key.

`Bucket.objects.all()`: Iterates over all objects in a bucket.

`Bucket.upload_file(Filename, Key, ExtraArgs)`: Uploads a local file.
- Filename: Local file path.
- Key: Destination key in bucket.
- ExtraArgs: Optional dict (e.g., {'ContentType': 'text/plain'}).

`Bucket.download_file(Key, Filename)`: Downloads an object to a local file.
- Key: Object key.
- Filename: Local file path.


ACL, 
Bucket, 
CreateBucketConfiguration, 
GrantFullControl, 
GrantRead, 
GrantReadACP, 
GrantWrite, 
GrantWriteACP, 
ObjectLockEnabledForBucket, 
ObjectOwnership



1) Bucket Creation and Configuration
Use Case: Create an S3 bucket with encryption and a basic access policy for DevOps automation.

```py

import boto3
import json
from botocore.exceptions import ClientError

def create_secure_bucket(bucket_name, region='us-east-1', account_id=None):
    """
    Creates a secure S3 bucket with encryption, versioning, and restricted access
    
    Args:
        bucket_name: Name of the bucket to create
        region: AWS region to create the bucket in
        account_id: AWS account ID for bucket policy (optional)
    """
    try:
        s3_client = boto3.client('s3', region_name=region)
        
        # Create bucket with region-specific configuration
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Created bucket {bucket_name} in {region}")
        
        # Enable server-side encryption
        s3_client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]
            }
        )
        print(f"Enabled default encryption for {bucket_name}")
        
        # Enable versioning
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print(f"Enabled versioning for {bucket_name}")
        
        # Block public access
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        print(f"Blocked public access for {bucket_name}")
        
        # Set bucket policy for restricted access if account_id is provided
        if account_id:
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                        "Action": "s3:*",
                        "Resource": [f"arn:aws:s3:::{bucket_name}", f"arn:aws:s3:::{bucket_name}/*"]
                    }
                ]
            }
            s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
            print(f"Applied access policy for {bucket_name}")
        
        return True, f"Bucket {bucket_name} created successfully with all security features"
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        if error_code == 'BucketAlreadyOwnedByYou':
            return False, f"Bucket {bucket_name} already exists and is owned by you"
        elif error_code == 'BucketAlreadyExists':
            return False, f"Bucket {bucket_name} already exists and is owned by another account"
        else:
            return False, f"Error: {e}"

if __name__ == "__main__":
    # Replace with your actual AWS account ID or pass it as a parameter
    success, message = create_secure_bucket("deepesh-devops-bucket-2025", account_id="221082194844")
    print(message)

```


---


2. File Upload and Download
Use Case: Automate uploading and downloading files to/from an S3 bucket, with metadata and

```py

import boto3
import json
from botocore.exceptions import ClientError

def upload_downlod_file(bucket_name, file_path, object_key):
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
    upload_downlod_file("deep-tf-test-bucket", "/home/deepesh-barod/Downloads/Devops/Boto3/Lib/test.py", "test.py")

```


---


3. Batch Object Operations
Use Case: List and delete objects in a bucket based on a prefix (e.g., cleaning up old logs).

```py

import boto3
from botocore.exceptions import ClientError

def clean_old_logs(bucket_name, prefix):
    try:
        s3_client = boto3.client('s3')
        # List objects with prefix
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' not in response:
            print("No objects found")
            return
        # Delete objects
        objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
        s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={'Objects': objects_to_delete}
        )
        print(f"Deleted {len(objects_to_delete)} objects from s3://{bucket_name}/{prefix}")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clean_old_logs("my-devops-bucket-2025", "logs/2024/")

```


---


4. Monitoring and Thresholds
Use Case: Monitor S3 bucket size and set a CloudWatch alarm if it exceeds a threshold (e.g., for cost control).

```py

import boto3
import datetime
from botocore.exceptions import ClientError

def monitor_bucket_size(bucket_name, threshold_bytes=1_000_000_000, sns_topic_arn=None):
    try:
        cloudwatch = boto3.client('cloudwatch')
        s3_client = boto3.client('s3')
        # Get bucket size
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/S3',
            MetricName='BucketSizeBytes',
            Dimensions=[
                {'Name': 'BucketName', 'Value': bucket_name},
                {'Name': 'StorageType', 'Value': 'StandardStorage'}
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(hours=1),
            EndTime=datetime.datetime.utcnow(),
            Period=3600,
            Statistics=['Average']
        )
        size = response['Datapoints'][0]['Average'] if response['Datapoints'] else 0
        print(f"Bucket {bucket_name} size: {size} bytes")
        # Set alarm if size exceeds threshold
        if size > threshold_bytes and sns_topic_arn:
            cloudwatch.put_metric_alarm(
                AlarmName=f"{bucket_name}-SizeAlarm",
                MetricName='BucketSizeBytes',
                Namespace='AWS/S3',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_name},
                    {'Name': 'StorageType', 'Value': 'StandardStorage'}
                ],
                Threshold=threshold_bytes,
                ComparisonOperator='GreaterThanThreshold',
                Period=3600,
                EvaluationPeriods=1,
                Statistic='Average',
                AlarmActions=[sns_topic_arn]
            )
            print(f"Alarm set for {bucket_name} at {threshold_bytes} bytes")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    monitor_bucket_size("my-devops-bucket-2025", sns_topic_arn="arn:aws:sns:us-east-1:123456789012:my-topic")

```


---


5. Access Control and Policy Management
Use Case: Apply a bucket policy to restrict access and enable public read for specific objects.

```py

import boto3
import json
from botocore.exceptions import ClientError

def set_bucket_access_policy(bucket_name, public_objects_prefix):
    try:
        s3_client = boto3.client('s3')
        # Define policy for public read on specific prefix
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/{public_objects_prefix}*"
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "arn:aws:iam::ACCOUNT_ID:role/devops-role"},
                    "Action": "s3:*",
                    "Resource": [f"arn:aws:s3:::{bucket_name}", f"arn:aws:s3:::{bucket_name}/*"]
                }
            ]
        }
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
        print(f"Applied policy to {bucket_name} with public read for {public_objects_prefix}")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    set_bucket_access_policy("my-devops-bucket-2025", "public/")

```


---     


