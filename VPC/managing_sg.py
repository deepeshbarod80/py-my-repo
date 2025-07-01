import boto3 # type: ignore

ec2 = boto3.client('ec2', region_name='us-east-1')

def add_ssh_rule(security_group_id, ip_address):
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[{
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': f'{ip_address}/32', 'Description': 'Temporary SSH'}]
        }]
    )
    print(f"Added SSH access for {ip_address} to {security_group_id}")

# Example: Allow SSH from a specific IP
add_ssh_rule('sg-1234567890abcdef0', '203.0.113.10')