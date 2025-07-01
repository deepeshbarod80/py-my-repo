import boto3 # type: ignore

ec2 = boto3.client('ec2', region_name='us-east-1')

def manage_instances(action):
    # Filter instances by tag
    response = ec2.describe_instances(Filters=[{'Name': 'tag:Environment', 'Values': ['Dev']}])
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    if not instance_ids:
        print("No instances found with tag Environment=Dev")
        return

    if action == 'start':
        ec2.start_instances(InstanceIds=instance_ids)
        print(f"Started instances: {instance_ids}")
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=instance_ids)
        print(f"Stopped instances: {instance_ids}")

# Start instances
manage_instances('start')
# Stop instances
# manage_instances('stop')