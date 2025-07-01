import boto3 # type: ignore
from datetime import datetime

ec2 = boto3.client('ec2', region_name='us-east-1')

def create_instance_snapshot(instance_id):
    # Get all volumes attached to the instance
    response = ec2.describe_instances(InstanceIds=[instance_id])
    volumes = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for mapping in instance['BlockDeviceMappings']:
                volumes.append(mapping['Ebs']['VolumeId'])

    # Create snapshots for each volume
    snapshot_ids = []
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    for volume_id in volumes:
        snapshot = ec2.create_snapshot(
            VolumeId=volume_id,
            Description=f'Backup of {volume_id} for instance {instance_id} at {timestamp}',
            TagSpecifications=[{
                'ResourceType': 'snapshot',
                'Tags': [{'Key': 'Backup', 'Value': 'Automated'}]
            }]
        )
        snapshot_ids.append(snapshot['SnapshotId'])
    
    print(f"Created snapshots: {snapshot_ids}")

# Example: Backup a specific instance
create_instance_snapshot('i-1234567890abcdef0')


# Cron Job for Daily Backups

# Save the EBS snapshot script (e.g., backup.py) from above.
# Add a cron job to run it daily at 2 AM:
#crontab -e

# Add the line:
#0 2 * * * /usr/bin/python3 /path/to/backup.py >> /var/log/backup.log 2>&1

# Ensure the script has executable permissions:
#chmod +x /path/to/backup.py
