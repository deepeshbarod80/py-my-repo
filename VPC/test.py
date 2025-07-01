
import boto3
from botocore.exceptions import ClientError


# Create vpc with 1 pub and 1 pri subnets in us-east-1
# print vpc id, subnet ids and tags in output

ec2_client = boto3.client('ec2', region_name = 'us-east-1')

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
        
        # Create VPC
        vpc_response = ec2_client.create_vpc(CidrBlock = '10.0.0.0/16')
        vpc_id = vpc_response['Vpc']['VpcId']
        ec2_client.modify_vpc_attribute(VpcId = vpc_id, EnableDnsSupport = {'Value': True})
        ec2_client.modify_vpc_attribute(VpcId = vpc_id, EnableDnsHostnames = {'Value': True})
        ec2_client.create_tags(Resources = [vpc_id], Tags = [{'Key': 'Name', 'Value': 'Test-VPC-001'}])
        
        # Create subnets and store their responses
        subnet1_response = ec2_client.create_subnet(
            CidrBlock = '10.0.1.0/24', 
            VpcId = vpc_id, 
            Tags = [{'Key': 'Name', 'Value': 'Test-Subnet-001'}]
        )
        
        subnet2_response = ec2_client.create_subnet(
            CidrBlock = '10.0.2.0/24', 
            VpcId = vpc_id, 
            Tags = [{'Key': 'Name', 'Value': 'Test-Subnet-002'}]
        )
        
        # Get subnet IDs
        subnet1_id = subnet1_response['Subnet']['SubnetId']
        subnet2_id = subnet2_response['Subnet']['SubnetId']
        
        # Print results
        print('VPC created successfully')
        print('VPC ID:', vpc_id)
        print('Subnet IDs:', subnet1_id, subnet2_id)
        print('VPC Tags:', vpc_response['Vpc'].get('Tags', [{'Key': 'Name', 'Value': 'Test-VPC-001'}]))

    except ClientError as e:
        print(e)

# First list existing VPCs, then create a new one if possible
list_vpcs()
create_vpc()
