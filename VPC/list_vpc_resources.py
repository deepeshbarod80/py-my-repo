import boto3
from botocore.exceptions import ClientError

# Initialize clients
ec2_client = boto3.client('ec2', region_name='us-east-1')
ec2_resource = boto3.resource('ec2', region_name='us-east-1')

def get_tag_name(tags):
    """Extract Name tag from resource tags"""
    if not tags:
        return "No Name"
    for tag in tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return "No Name"

def list_vpc_resources():
    """List all VPCs and their associated resources"""
    try:
        # Get all VPCs
        vpcs = ec2_client.describe_vpcs()
        
        if not vpcs['Vpcs']:
            print("No VPCs found in this region")
            return
            
        print(f"\n{'='*80}\nFound {len(vpcs['Vpcs'])} VPCs in us-east-1\n{'='*80}")
        
        # Iterate through each VPC
        for vpc in vpcs['Vpcs']:
            vpc_id = vpc['VpcId']
            vpc_cidr = vpc['CidrBlock']
            vpc_name = get_tag_name(vpc.get('Tags', []))
            
            print(f"\nVPC: {vpc_id} | Name: {vpc_name} | CIDR: {vpc_cidr}")
            print("-" * 80)
            
            # List Subnets
            subnets = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            print(f"\n  Subnets ({len(subnets['Subnets'])}):")
            for subnet in subnets['Subnets']:
                subnet_name = get_tag_name(subnet.get('Tags', []))
                print(f"    - {subnet['SubnetId']} | {subnet_name} | {subnet['CidrBlock']} | {subnet['AvailabilityZone']}")
            
            # List Route Tables
            route_tables = ec2_client.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            print(f"\n  Route Tables ({len(route_tables['RouteTables'])}):")
            for rt in route_tables['RouteTables']:
                rt_name = get_tag_name(rt.get('Tags', []))
                print(f"    - {rt['RouteTableId']} | {rt_name}")
                # List associations
                for assoc in rt.get('Associations', []):
                    if assoc.get('SubnetId'):
                        print(f"      Associated with Subnet: {assoc['SubnetId']}")
                    elif assoc.get('GatewayId'):
                        print(f"      Associated with Gateway: {assoc['GatewayId']}")
                    elif assoc.get('Main', False):
                        print(f"      Main Route Table")
            
            # List Internet Gateways
            igws = ec2_client.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}])
            print(f"\n  Internet Gateways ({len(igws['InternetGateways'])}):")
            for igw in igws['InternetGateways']:
                igw_name = get_tag_name(igw.get('Tags', []))
                print(f"    - {igw['InternetGatewayId']} | {igw_name}")
            
            # List NAT Gateways
            nat_gateways = ec2_client.describe_nat_gateways(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            print(f"\n  NAT Gateways ({len(nat_gateways.get('NatGateways', []))}):")
            for nat in nat_gateways.get('NatGateways', []):
                nat_name = get_tag_name(nat.get('Tags', []))
                print(f"    - {nat['NatGatewayId']} | {nat_name} | {nat['State']}")
            
            # List Security Groups
            sgs = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            print(f"\n  Security Groups ({len(sgs['SecurityGroups'])}):")
            for sg in sgs['SecurityGroups']:
                print(f"    - {sg['GroupId']} | {sg['GroupName']}")
            
            # List Network ACLs
            acls = ec2_client.describe_network_acls(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            print(f"\n  Network ACLs ({len(acls['NetworkAcls'])}):")
            for acl in acls['NetworkAcls']:
                acl_name = get_tag_name(acl.get('Tags', []))
                print(f"    - {acl['NetworkAclId']} | {acl_name}")
            
            # List VPC Endpoints
            endpoints = ec2_client.describe_vpc_endpoints(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            print(f"\n  VPC Endpoints ({len(endpoints.get('VpcEndpoints', []))}):")
            for endpoint in endpoints.get('VpcEndpoints', []):
                print(f"    - {endpoint['VpcEndpointId']} | {endpoint['ServiceName']} | {endpoint['State']}")
            
            # List EC2 Instances in this VPC
            instances = ec2_client.describe_instances(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            instance_count = sum(len(reservation['Instances']) for reservation in instances['Reservations'])
            print(f"\n  EC2 Instances ({instance_count}):")
            
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    instance_name = get_tag_name(instance.get('Tags', []))
                    print(f"    - {instance['InstanceId']} | {instance_name} | {instance['InstanceType']} | {instance['State']['Name']}")
                    
                    # List attached resources for this instance
                    print(f"      * Subnet: {instance.get('SubnetId', 'N/A')}")
                    print(f"      * Private IP: {instance.get('PrivateIpAddress', 'N/A')}")
                    print(f"      * Public IP: {instance.get('PublicIpAddress', 'N/A')}")
                    
                    # Security Groups
                    if instance.get('SecurityGroups'):
                        sg_list = ", ".join([sg['GroupId'] for sg in instance['SecurityGroups']])
                        print(f"      * Security Groups: {sg_list}")
                    
                    # EBS Volumes
                    volumes = [vol['Ebs']['VolumeId'] for vol in instance.get('BlockDeviceMappings', [])]
                    if volumes:
                        print(f"      * EBS Volumes: {', '.join(volumes)}")
                    
                    # Elastic IPs
                    if instance.get('PublicIpAddress'):
                        addresses = ec2_client.describe_addresses(Filters=[
                            {'Name': 'instance-id', 'Values': [instance['InstanceId']]}
                        ])
                        if addresses.get('Addresses'):
                            eip_list = ", ".join([addr['AllocationId'] for addr in addresses['Addresses']])
                            print(f"      * Elastic IPs: {eip_list}")
                    
                    # IAM Role
                    if instance.get('IamInstanceProfile'):
                        print(f"      * IAM Role: {instance['IamInstanceProfile']['Arn'].split('/')[-1]}")
            
            print("\n" + "=" * 80)

    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_vpc_resources()