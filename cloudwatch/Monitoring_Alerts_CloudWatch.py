import boto3 # type: ignore
import psutil # type: ignore
from datetime import datetime

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

def push_cpu_metric(instance_id):
    cpu_percent = psutil.cpu_percent(interval=1)
    cloudwatch.put_metric_data(
        Namespace='CustomMetrics',
        MetricData=[{
            'MetricName': 'CPUUtilization',
            'Dimensions': [{'Name': 'InstanceId', 'Value': instance_id}],
            'Value': cpu_percent,
            'Unit': 'Percent',
            'Timestamp': datetime.utcnow()
        }]
    )
    print(f"Pushed CPU utilization {cpu_percent}% for {instance_id}")

# Example: Push metric for an instance
push_cpu_metric('i-1234567890abcdef0')