import boto3                # type:igr
from datetime import datetime

s3 = boto3.client('s3')

def upload_logs_to_s3(bucket_name, log_file_path):
    # Generate a unique key with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    s3_key = f'logs/{timestamp}_{log_file_path.split("/")[-1]}'

    # Upload the file
    s3.upload_file(log_file_path, bucket_name, s3_key)
    print(f"Uploaded {log_file_path} to s3://{bucket_name}/{s3_key}")

# Example: Upload syslog
upload_logs_to_s3('my-log-bucket', '/var/log/syslog')