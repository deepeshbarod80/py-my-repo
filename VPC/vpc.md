
# Client Methods (boto3.client('ec2')):
`create_vpc(CidrBlock, **kwargs)`: Creates a VPC.
- `CidrBlock`: CIDR block for the VPC (e.g., '10.0.0.0/16').
- `**kwargs`: Optional args like TagSpecifications for tagging.

`create_subnet(VpcId, CidrBlock, AvailabilityZone, **kwargs)`: Creates a subnet.
- `VpcId`: ID of the VPC.
- `CidrBlock`: Subnet CIDR (e.g., '10.0.1.0/24').
- `AvailabilityZone`: AZ for the subnet (e.g., 'us-east-1a').

`create_internet_gateway(**kwargs)`: Creates an internet gateway.
- `**kwargs`: Optional args like TagSpecifications.

`attach_internet_gateway(InternetGatewayId, VpcId)`: Attaches an internet gateway to a VPC.
- `InternetGatewayId`: ID of the internet gateway.
- `VpcId`: ID of the VPC.

`create_route_table(VpcId, **kwargs)`: Creates a route table.
- `VpcId`: ID of the VPC.

`create_route(RouteTableId, DestinationCidrBlock, GatewayId)`: Adds a route to a route table.
- `RouteTableId`: ID of the route table.
- `DestinationCidrBlock`: CIDR for the route (e.g., '0.0.0.0/0').
- `GatewayId`: ID of the gateway (e.g., internet gateway).

`associate_route_table(RouteTableId, SubnetId)`: Associates a route table with a subnet.
- `RouteTableId`: ID of the route table.
- `SubnetId`: ID of the subnet.

`create_security_group(GroupName, Description, VpcId, **kwargs)`: Creates a security group.
- `GroupName`: Name of the security group.
- `Description`: Description of the security group.
- `VpcId`: ID of the VPC.

`authorize_security_group_ingress(GroupId, IpPermissions)`: Adds inbound rules to security group.
- `GroupId`: ID of the security group.
- `IpPermissions`: List of rules (e.g., protocol, port, CIDR).

`describe_vpcs(**kwargs)`: Lists VPCs.
- `**kwargs`: Filters like VpcIds or Filters.

`describe_subnets(**kwargs)`: Lists subnets.
- `**kwargs`: Filters like SubnetIds or Filters.



# Resource Methods (boto3.resource('ec2')):
`Vpc(id)`: Accesses a specific VPC.
- id: VPC ID.
`Subnet(id)`: Accesses a specific subnet.
- id: Subnet ID.
`SecurityGroup(id)`: Accesses a specific security group.
- id: Security group ID.
`create_tags(Resources, Tags)`: Adds tags to resources.
- Resources: List of resource IDs (e.g., VPC, subnet).
- Tags: List of dicts with Key and Value.



1. VPC Creation and Configuration
Scenario: Create a VPC with public and private subnets, an internet gateway, and a route table for a production environment.

```py

import boto3
from botocore.exceptions import ClientError

def create_vpc_with_subnets(vpc_cidr='10.0.0.0/16', subnet_configs=None, region='us-east-1'):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        ec2_resource = boto3.resource('ec2', region_name=region)
        
        # Create VPC
        vpc = ec2_client.create_vpc(CidrBlock=vpc_cidr)
        vpc_id = vpc['Vpc']['VpcId']
        ec2_client.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'prod-vpc'}])
        
        # Enable DNS support
        ec2_client.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
        ec2_client.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
        
        # Create internet gateway
        igw = ec2_client.create_internet_gateway()
        igw_id = igw['InternetGateway']['InternetGatewayId']
        ec2_client.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
        ec2_client.create_tags(Resources=[igw_id], Tags=[{'Key': 'Name', 'Value': 'prod-igw'}])
        
        # Create route table
        route_table = ec2_client.create_route_table(VpcId=vpc_id)
        route_table_id = route_table['RouteTable']['RouteTableId']
        ec2_client.create_route(RouteTableId=route_table_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
        ec2_client.create_tags(Resources=[route_table_id], Tags=[{'Key': 'Name', 'Value': 'prod-public-rt'}])
        
        # Create subnets
        subnet_configs = subnet_configs or [
            {'Cidr': '10.0.1.0/24', 'AZ': f'{region}a', 'Name': 'public-subnet-1', 'Public': True},
            {'Cidr': '10.0.2.0/24', 'AZ': f'{region}b', 'Name': 'private-subnet-1', 'Public': False}
        ]
        subnet_ids = []
        for config in subnet_configs:
            subnet = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=config['Cidr'], AvailabilityZone=config['AZ'])
            subnet_id = subnet['Subnet']['SubnetId']
            ec2_client.create_tags(Resources=[subnet_id], Tags=[{'Key': 'Name', 'Value': config['Name']}])
            if config['Public']:
                ec2_client.associate_route_table(RouteTableId=route_table_id, SubnetId=subnet_id)
            subnet_ids.append(subnet_id)
        
        print(f"Created VPC {vpc_id} with subnets: {subnet_ids}")
        return vpc_id, subnet_ids, igw_id, route_table_id
    except ClientError as e:
        print(f"Error: {e}")
        return None, None, None, None

if __name__ == "__main__":
    create_vpc_with_subnets()

```


---



2. Security Group Management
Scenario: Create a security group for a web application, allowing HTTP/HTTPS inbound traffic and SSH from a specific IP range.

```py

import boto3
from botocore.exceptions import ClientError

def create_web_security_group(vpc_id, group_name='web-sg', allowed_ip='0.0.0.0/0', region='us-east-1'):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        # Create security group
        sg = ec2_client.create_security_group(GroupName=group_name, Description='Security group for web app', VpcId=vpc_id)
        sg_id = sg['GroupId']
        ec2_client.create_tags(Resources=[sg_id], Tags=[{'Key': 'Name', 'Value': group_name}])
        
        # Add inbound rules
        ec2_client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': allowed_ip, 'Description': 'HTTP access'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': allowed_ip, 'Description': 'HTTPS access'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '203.0.113.0/24', 'Description': 'SSH from trusted IP'}]
                }
            ]
        )
        print(f"Created security group {sg_id} with HTTP, HTTPS, and SSH rules")
        return sg_id
    except ClientError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    create_web_security_group(vpc_id='vpc-1234567890abcdef0')

```


---


3. VPC Monitoring and Thresholds
Scenario: Monitor VPC flow logs for unusual traffic (e.g., high data transfer) using CloudWatch and set an alarm.

```py

import boto3
import datetime
from botocore.exceptions import ClientError

def monitor_vpc_flow_logs(vpc_id, threshold_bytes=1_000_000_000, sns_topic_arn=None, region='us-east-1'):
    try:
        cloudwatch = boto3.client('cloudwatch', region_name=region)
        ec2_client = boto3.client('ec2', region_name=region)
        
        # Check if flow logs are enabled
        flow_logs = ec2_client.describe_flow_logs(Filters=[{'Name': 'resource-id', 'Values': [vpc_id]}])
        if not flow_logs['FlowLogs']:
            print(f"No flow logs enabled for VPC {vpc_id}")
            return
        
        # Get bytes transferred (from flow logs stored in CloudWatch)
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/VPC',
            MetricName='Bytes',
            Dimensions=[
                {'Name': 'VPC', 'Value': vpc_id},
                {'Name': 'LogGroupName', 'Value': 'vpc-flow-logs'}
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(hours=1),
            EndTime=datetime.datetime.utcnow(),
            Period=3600,
            Statistics=['Sum']
        )
        total_bytes = response['Datapoints'][0]['Sum'] if response['Datapoints'] else 0
        print(f"VPC {vpc_id} transferred {total_bytes} bytes in last hour")
        
        # Set alarm if threshold exceeded
        if total_bytes > threshold_bytes and sns_topic_arn:
            cloudwatch.put_metric_alarm(
                AlarmName=f"{vpc_id}-HighTrafficAlarm",
                MetricName='Bytes',
                Namespace='AWS/VPC',
                Dimensions=[
                    {'Name': 'VPC', 'Value': vpc_id},
                    {'Name': 'LogGroupName', 'Value': 'vpc-flow-logs'}
                ],
                Threshold=threshold_bytes,
                ComparisonOperator='GreaterThanThreshold',
                Period=3600,
                EvaluationPeriods=1,
                Statistic='Sum',
                AlarmActions=[sns_topic_arn]
            )
            print(f"Alarm set for {vpc_id} at {threshold_bytes} bytes")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    monitor_vpc_flow_logs(vpc_id='vpc-1234567890abcdef0', sns_topic_arn='arn:aws:sns:us-east-1:123456789012:my-topic')

```


---



4. Subnet and Route Table Automation
Scenario: Automate associating subnets with a custom route table for private subnets (e.g., routing via a NAT gateway).

```py

import boto3
from botocore.exceptions import ClientError

def configure_private_subnet(vpc_id, subnet_cidr='10.0.2.0/24', az='us-east-1b', nat_gateway_id=None, region='us-east-1'):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        # Create private subnet
        subnet = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=subnet_cidr, AvailabilityZone=az)
        subnet_id = subnet['Subnet']['SubnetId']
        ec2_client.create_tags(Resources=[subnet_id], Tags=[{'Key': 'Name', 'Value': 'private-subnet-1'}])
        
        # Create route table for private subnet
        route_table = ec2_client.create_route_table(VpcId=vpc_id)
        route_table_id = route_table['RouteTable']['RouteTableId']
        ec2_client.create_tags(Resources=[route_table_id], Tags=[{'Key': 'Name', 'Value': 'private-rt'}])
        
        # Associate route table with subnet
        ec2_client.associate_route_table(RouteTableId=route_table_id, SubnetId=subnet_id)
        
        # Add route to NAT gateway if provided
        if nat_gateway_id:
            ec2_client.create_route(
                RouteTableId=route_table_id,
                DestinationCidrBlock='0.0.0.0/0',
                NatGatewayId=nat_gateway_id
            )
            print(f"Added NAT gateway route to {route_table_id}")
        
        print(f"Configured private subnet {subnet_id} with route table {route_table_id}")
        return subnet_id, route_table_id
    except ClientError as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    configure_private_subnet(vpc_id='vpc-1234567890abcdef0', nat_gateway_id='nat-0abcdef1234567890')

```


---



5. VPC Cleanup Automation
Scenario: Delete a VPC and its associated components (subnets, route tables, internet gateways, security groups) for cleanup after testing.

```py

import boto3
from botocore.exceptions import ClientError

def delete_vpc(vpc_id, region='us-east-1'):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        ec2_resource = boto3.resource('ec2', region_name=region)
        vpc = ec2_resource.Vpc(vpc_id)
        
        # Delete subnets
        for subnet in vpc.subnets.all():
            ec2_client.delete_subnet(SubnetId=subnet.id)
            print(f"Deleted subnet {subnet.id}")
        
        # Delete route tables (except main)
        for rt in vpc.route_tables.all():
            if not rt.associations_attribute or rt.associations_attribute[0].get('Main') is False:
                ec2_client.delete_route_table(RouteTableId=rt.id)
                print(f"Deleted route table {rt.id}")
        
        # Detach and delete internet gateways
        for igw in vpc.internet_gateways.all():
            ec2_client.detach_internet_gateway(InternetGatewayId=igw.id, VpcId=vpc_id)
            ec2_client.delete_internet_gateway(InternetGatewayId=igw.id)
            print(f"Deleted internet gateway {igw.id}")
        
        # Delete security groups (except default)
        for sg in vpc.security_groups.all():
            if sg.group_name != 'default':
                ec2_client.delete_security_group(GroupId=sg.id)
                print(f"Deleted security group {sg.id}")
        
        # Delete VPC
        ec2_client.delete_vpc(VpcId=vpc_id)
        print(f"Deleted VPC {vpc_id}")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    delete_vpc(vpc_id='vpc-1234567890abcdef0')

```


--- 


6. VPC Endpoint Creation for S3 Access
Scenario: Create a VPC endpoint to allow private access to S3 from a VPC, reducing data transfer costs and enhancing security.

```py

import boto3
from botocore.exceptions import ClientError

def create_s3_vpc_endpoint(vpc_id, route_table_id, region='us-east-1'):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        # Create VPC endpoint for S3
        endpoint = ec2_client.create_vpc_endpoint(
            VpcId=vpc_id,
            ServiceName=f'com.amazonaws.{region}.s3',
            RouteTableIds=[route_table_id],
            VpcEndpointType='Gateway',
            TagSpecifications=[
                {
                    'ResourceType': 'vpc-endpoint',
                    'Tags': [{'Key': 'Name', 'Value': 's3-endpoint'}]
                }
            ]
        )
        endpoint_id = endpoint['VpcEndpoint']['VpcEndpointId']
        print(f"Created S3 VPC endpoint {endpoint_id} for VPC {vpc_id}")
        return endpoint_id
    except ClientError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    create_s3_vpc_endpoint(vpc_id='vpc-1234567890abcdef0', route_table_id='rtb-1234567890abcdef0')

```


---


7. NAT Gateway Setup for Private Subnets
Scenario: Set up a NAT gateway in a public subnet to allow private subnets to access the internet (e.g., for software updates) while keeping them isolated.

```py

import boto3
from botocore.exceptions import ClientError

def create_nat_gateway(public_subnet_id, route_table_id, region='us-east-1'):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        # Allocate Elastic IP
        eip = ec2_client.allocate_address(Domain='vpc')
        eip_id = eip['AllocationId']
        # Create NAT gateway
        nat_gateway = ec2_client.create_nat_gateway(SubnetId=public_subnet_id, AllocationId=eip_id)
        nat_gateway_id = nat_gateway['NatGateway']['NatGatewayId']
        ec2_client.create_tags(Resources=[nat_gateway_id], Tags=[{'Key': 'Name', 'Value': 'prod-nat-gateway'}])
        # Wait for NAT gateway to be available
        waiter = ec2_client.get_waiter('nat_gateway_available')
        waiter.wait(NatGatewayIds=[nat_gateway_id])
        # Add route to private route table
        ec2_client.create_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock='0.0.0.0/0',
            NatGatewayId=nat_gateway_id
        )
        print(f"Created NAT gateway {nat_gateway_id} in subnet {public_subnet_id}")
        return nat_gateway_id, eip_id
    except ClientError as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    create_nat_gateway(public_subnet_id='subnet-1234567890abcdef0', route_table_id='rtb-1234567890abcdef0')

```


---



8. VPC Peering for Cross-VPC Communication
Scenario: Establish a VPC peering connection between two VPCs (e.g., dev and prod) to enable resource sharing.

```py

import boto3
from botocore.exceptions import ClientError

def create_vpc_peering(vpc_id, peer_vpc_id, peer_owner_id, region='us-east-1'):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        # Create peering connection
        peering = ec2_client.create_vpc_peering_connection(
            VpcId=vpc_id,
            PeerVpcId=peer_vpc_id,
            PeerOwnerId=peer_owner_id
        )
        peering_id = peering['VpcPeeringConnection']['VpcPeeringConnectionId']
        ec2_client.create_tags(Resources=[peering_id], Tags=[{'Key': 'Name', 'Value': 'dev-prod-peering'}])
        # Accept peering connection (if same account)
        if peer_owner_id == boto3.client('sts').get_caller_identity()['Account']:
            ec2_client.accept_vpc_peering_connection(VpcPeeringConnectionId=peering_id)
        # Update route tables (assumes route table IDs are known)
        for rt_id in ['rtb-1234567890abcdef0', 'rtb-0987654321fedcba0']:
            ec2_client.create_route(
                RouteTableId=rt_id,
                DestinationCidrBlock='10.0.0.0/16' if rt_id == 'rtb-1234567890abcdef0' else '10.1.0.0/16',
                VpcPeeringConnectionId=peering_id
            )
        print(f"Created and configured VPC peering {peering_id}")
        return peering_id
    except ClientError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    create_vpc_peering(vpc_id='vpc-1234567890abcdef0', peer_vpc_id='vpc-0987654321fedcba0', peer_owner_id='123456789012')

```


---



9. Subnet Auto-Configuration for Auto Scaling
Scenario: Configure subnets to support Auto Scaling groups by enabling auto-assign public IPs for public subnets and associating them with a route table.

```py

import boto3
from botocore.exceptions import ClientError

def configure_subnet_for_autoscaling(vpc_id, subnet_cidr='10.0.3.0/24', az='us-east-1c', route_table_id=None, region='us-east-1'):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        # Create subnet
        subnet = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=subnet_cidr, AvailabilityZone=az)
        subnet_id = subnet['Subnet']['SubnetId']
        ec2_client.create_tags(Resources=[subnet_id], Tags=[{'Key': 'Name', 'Value': 'public-subnet-2'}])
        # Enable auto-assign public IP
        ec2_client.modify_subnet_attribute(SubnetId=subnet_id, MapPublicIpOnLaunch={'Value': True})
        # Associate with route table (assumes public route table with internet gateway)
        if route_table_id:
            ec2_client.associate_route_table(RouteTableId=route_table_id, SubnetId=subnet_id)
        print(f"Configured subnet {subnet_id} for Auto Scaling with public IP assignment")
        return subnet_id
    except ClientError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    configure_subnet_for_autoscaling(vpc_id='vpc-1234567890abcdef0', route_table_id='rtb-1234567890abcdef0')

```


---


10. VPC Inventory and Tagging Automation
Scenario: Generate an inventory of all VPCs and their components in an AWS account, and apply standardized tags to ensure consistent naming and cost allocation (e.g., for tracking resources in a multi-team environment).

```py

import boto3
import json
from botocore.exceptions import ClientError

def generate_vpc_inventory_and_tag(region='us-east-1', tag_key='Environment', tag_value='Production'):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        ec2_resource = boto3.resource('ec2', region_name=region)
        inventory = {'VPCs': []}
        
        # Get all VPCs
        vpcs = ec2_client.describe_vpcs()
        for vpc in vpcs['Vpcs']:
            vpc_id = vpc['VpcId']
            vpc_inventory = {
                'VpcId': vpc_id,
                'CidrBlock': vpc['CidrBlock'],
                'Subnets': [],
                'RouteTables': [],
                'SecurityGroups': [],
                'InternetGateways': []
            }
            
            # Get subnets
            subnets = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            for subnet in subnets['Subnets']:
                vpc_inventory['Subnets'].append({
                    'SubnetId': subnet['SubnetId'],
                    'CidrBlock': subnet['CidrBlock'],
                    'AvailabilityZone': subnet['AvailabilityZone']
                })
            
            # Get route tables
            route_tables = ec2_client.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            for rt in route_tables['RouteTables']:
                vpc_inventory['RouteTables'].append({'RouteTableId': rt['RouteTableId']})
            
            # Get security groups
            security_groups = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            for sg in security_groups['SecurityGroups']:
                vpc_inventory['SecurityGroups'].append({
                    'GroupId': sg['GroupId'],
                    'GroupName': sg['GroupName']
                })
            
            # Get internet gateways
            igws = ec2_client.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}])
            for igw in igws['InternetGateways']:
                vpc_inventory['InternetGateways'].append({'InternetGatewayId': igw['InternetGatewayId']})
            
            inventory['VPCs'].append(vpc_inventory)
            
            # Apply tags to VPC and components
            resource_ids = [vpc_id] + [s['SubnetId'] for s in subnets['Subnets']] + \
                           [rt['RouteTableId'] for rt in route_tables['RouteTables']] + \
                           [sg['GroupId'] for sg in security_groups['SecurityGroups']] + \
                           [igw['InternetGatewayId'] for igw in igws['InternetGateways']]
            if resource_ids:
                ec2_client.create_tags(
                    Resources=resource_ids,
                    Tags=[{'Key': tag_key, 'Value': tag_value}]
                )
        
        # Save inventory to a file
        with open('vpc_inventory.json', 'w') as f:
            json.dump(inventory, f, indent=2)
        
        print(f"Generated inventory for {len(vpcs['Vpcs'])} VPCs and tagged resources with {tag_key}={tag_value}")
        print(f"Inventory saved to vpc_inventory.json")
        return inventory
    except ClientError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    generate_vpc_inventory_and_tag()

```


---



# Check the limits of aws account to create VPC

```py

def list_vpcs():
    """List existing VPCs in the account"""
    try:
        response = ec2_client.describe_vpcs()
        print(f"You have {len(response['Vpcs'])} VPCs in your account")
        for vpc in response['Vpcs']:
            vpc_id = vpc['VpcId']
            tags = vpc.get('Tags', [])
            name = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), 'No Name')
            print(f"VPC ID: {vpc_id}, Name: {name}")
        return response['Vpcs']
    except ClientError as e:
        print(e)
        return []

def delete_vpc(vpc_id):
    """Delete a VPC and its dependencies"""
    try:
        # First delete all subnets in the VPC
        subnets = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        for subnet in subnets['Subnets']:
            print(f"Deleting subnet {subnet['SubnetId']}")
            ec2_client.delete_subnet(SubnetId=subnet['SubnetId'])
        
        # Delete the VPC
        ec2_client.delete_vpc(VpcId=vpc_id)
        print(f"VPC {vpc_id} deleted successfully")
        return True
    except ClientError as e:
        print(f"Error deleting VPC {vpc_id}: {e}")
        return False

def create_vpc():
    try:
        # Check existing VPCs first
        vpcs = list_vpcs()
        
        # If we're at the limit, ask to delete one
        if len(vpcs) >= 5:  # AWS default limit is 5 VPCs per region
            print("You've reached the VPC limit. Would you like to delete an existing VPC? (y/n)")
            choice = input()
            if choice.lower() == 'y':
                print("Enter the VPC ID to delete:")
                vpc_to_delete = input()
                if not delete_vpc(vpc_to_delete):
                    print("VPC deletion failed. Exiting.")
                    return
            else:
                print("Operation cancelled. Please delete a VPC manually or request a limit increase.")
                return

create_vpc()