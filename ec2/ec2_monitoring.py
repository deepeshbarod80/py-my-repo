import boto3 # type: ignore
import json
from datetime import datetime, timedelta
import os

# Initialize AWS clients
ec2_client = boto3.client('ec2', region_name='us-east-1')
cloudwatch_client = boto3.client('cloudwatch', region_name='us-east-1')
ses_client = boto3.client('ses', region_name='us-east-1')

def get_instance_metrics(instance_id):
    # Get instance status
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    instance_name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'Unnamed')
    state = instance['State']['Name']
    
    # Get CPU utilization (last 24 hours average)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=24)
    cpu_metrics = cloudwatch_client.get_metric_data(
        MetricDataQueries=[{
            'Id': 'cpu',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/EC2',
                    'MetricName': 'CPUUtilization',
                    'Dimensions': [{'Name': 'InstanceId', 'Value': instance_id}]
                },
                'Period': 3600,
                'Stat': 'Average'
            }
        }],
        StartTime=start_time,
        EndTime=end_time
    )
    cpu_usage = cpu_metrics['MetricDataResults'][0]['Values'][0] if cpu_metrics['MetricDataResults'][0]['Values'] else 0.0
    
    return {
        'InstanceId': instance_id,
        'Name': instance_name,
        'State': state,
        'CPUUtilization': f"{cpu_usage:.2f}%"
    }

def send_email(report, recipient_email, sender_email):
    body = "\n".join([f"Instance: {r['Name']} ({r['InstanceId']})\nState: {r['State']}\nCPU Utilization (24h avg): {r['CPUUtilization']}\n" for r in report])
    ses_client.send_email(
        Source=sender_email,
        Destination={'ToAddresses': [recipient_email]},
        Message={
            'Subject': {'Data': f'EC2 Monitoring Report - {datetime.now().strftime("%Y-%m-%d")}'},
            'Body': {'Text': {'Data': body}}
        }
    )

def lambda_handler(event, context):
    # Environment variables
    recipient_email = os.environ['RECIPIENT_EMAIL']
    sender_email = os.environ['SENDER_EMAIL']
    
    # Get all EC2 instances
    response = ec2_client.describe_instances()
    instances = [i for r in response['Reservations'] for i in r['Instances']]
    instance_ids = [i['InstanceId'] for i in instances]
    
    # Collect metrics
    report = [get_instance_metrics(instance_id) for instance_id in instance_ids]
    
    # Send email
    send_email(report, recipient_email, sender_email)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Monitoring report sent successfully')
    }