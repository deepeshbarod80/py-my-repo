import boto3 # type: ignore

ec2 = boto3.client('ec2', region_name='us-east-1')

def restore_volume_from_snapshot(snapshot_id, instance_id, availability_zone='us-east-1a'):
    # Create a new volume from the snapshot
    volume = ec2.create_volume(
        SnapshotId=snapshot_id,
        AvailabilityZone=availability_zone,
        TagSpecifications=[{
            'ResourceType': 'volume',
            'Tags': [{'Key': 'Restored', 'Value': 'DR'}]
        }]
    )
    volume_id = volume['VolumeId']

    # Wait for the volume to be available
    waiter = ec2.get_waiter('volume_available')
    waiter.wait(VolumeIds=[volume_id])

    # Attach the volume to the instance
    ec2.attach_volume(
        VolumeId=volume_id,
        InstanceId=instance_id,
        Device='/dev/sdf'
    )
    print(f"Restored volume {volume_id} from snapshot {snapshot_id} and attached to {instance_id}")

# Example: Restore and attach
restore_volume_from_snapshot('snap-1234567890abcdef0', 'i-1234567890abcdef0')