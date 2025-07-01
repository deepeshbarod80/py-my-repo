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