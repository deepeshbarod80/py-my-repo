# Comprehensive List of boto3 Methods and Arguments for VPC and Components
The boto3 library interacts with VPCs primarily through the EC2 client (boto3.client('ec2')) and resource (boto3.resource('ec2')).

1. VPC Management
# create_vpc
* Description: Creates a new VPC.
* Example: `create_vpc.py`
* Arguments:
- `CidrBlock (string, required)`: The IPv4 CIDR block for the VPC (e.g., '10.0.0.0/16').
- `AmazonProvidedIpv6CidrBlock (boolean, optional)`: Requests an IPv6 CIDR block (`default: False`).
- `InstanceTenancy (string, optional)`: Tenancy option (`'default', 'dedicated', 'host'`) (default: 'default').
- `TagSpecifications (list, optional)`: Tags to apply, e.g., `[{'ResourceType': 'vpc', 'Tags': [{'Key': 'Name', 'Value': 'prod-vpc'}]}]`.

# delete_vpc
* Description: Deletes a VPC.
* Example: `delete_vpc.py`
* Arguments:
- `VpcId (string, required)`: The VPC ID (e.g., `'vpc-1234567890abcdef0')`.

# describe_vpcs
* Description: Retrieves information about VPCs.
* Example: `vpc_inventory_tagging.py`
* Arguments:
- `VpcIds (list, optional)`: List of VPC IDs to filter (e.g., ['vpc-1234567890abcdef0']).
- `Filters (list, optional)`: Filters, e.g., `[{'Name': 'tag:Environment', 'Values': ['Production']}]`.
- `NextToken (string, optional)`: Pagination token for large result sets.
- `MaxResults (integer, optional)`: Maximum number of VPCs to `return (5–1000)`.

# modify_vpc_attribute
* Description: Modifies VPC attributes like DNS support.
* Example: `create_vpc.py`
* Arguments:
- `VpcId (string, required)`: The VPC ID.
- `EnableDnsSupport (dict, optional)`: {'Value': True|False} to `enable/disable` DNS resolution.
- `EnableDnsHostnames (dict, optional)`: {'Value': True|False} to `enable/disable` DNS hostnames.


---------------->


2. Subnet Management
# create_subnet
* Description: Creates a subnet in a VPC.
* Example: `configure_private_subnet.py`
* Arguments:
- `VpcId (string, required)`: The VPC ID.
- `CidrBlock (string, required)`: The subnet CIDR (e.g., '10.0.1.0/24').
- `AvailabilityZone (string, optional)`: The Availability Zone (e.g., 'us-east-1a').
- `AvailabilityZoneId (string, optional)`: The AZ ID (e.g., 'use1-az1').
- `Ipv6CidrBlock (string, optional)`: The IPv6 CIDR block.
- `OutpostArn (string, optional)`: ARN of an Outpost for subnet placement.
- `TagSpecifications (list, optional)`: Tags, e.g., [{'ResourceType': 'subnet', 'Tags': [{'Key': 'Name', 'Value': 'public-subnet-1'}]}].

# delete_subnet
* Description: Deletes a subnet.
* Example: `delete_subnet.py`
* Arguments:
- `SubnetId (string, required)`: The subnet ID (e.g., `'subnet-1234567890abcdef0')`.

# describe_subnets
* Description: Retrieves subnet information.
* Example: `vpc_inventory_tagging.py`
* Arguments:
- `SubnetIds (list, optional)`: List of subnet IDs.
- `Filters (list, optional)`: Filters, e.g., `[{'Name': 'vpc-id', 'Values': ['vpc-1234567890abcdef0']}]`.
- `NextToken (string, optional)`: Pagination token.
- `MaxResults (integer, optional)`: Maximum results (5-1000).

# modify_subnet_attribute
* Description: Modifies subnet attributes (e.g., public IP assignment).
* Example: `configure_subnet_for_autoscaling.py`
* Arguments:
- `SubnetId (string, required)`: The subnet ID.
- `MapPublicIpOnLaunch (dict, optional)`: {'Value': True|False} to `enable/disable` auto-assign public IPs.
- `MapCustomerOwnedIpOnLaunch (dict, optional)`: {'Value': True|False} for customer-owned IPs.
- `CustomerOwnedIpv4Pool (string, optional)`: The customer-owned IPv4 pool ID.


--------------------------->


3. Route Table Management
# create_route_table
* Description: Creates a route table in a VPC.
* Example: `create_route_table.py`
* Arguments:
- `VpcId (string, required)`: The VPC ID.
- `TagSpecifications (list, optional)`: Tags, e.g., `[{'ResourceType': 'route-table', 'Tags': [{'Key': 'Name', 'Value': 'public-rt'}]}]`.

# delete_route_table
* Description: Deletes a route table.
* Example: `create_vpc.py, configure_private_subnet.py`
* Arguments:
- `RouteTableId (string, required)`: The route table ID (e.g., `'rtb-1234567890abcdef0')`.

# create_route
* Description: Adds a route to a route table.
* Example: `create_vpc.py, configure_private_subnet.py`
* Arguments:
- `RouteTableId (string, required)`: The route table ID.
- `DestinationCidrBlock (string, optional)`: IPv4 CIDR (e.g., `'0.0.0.0/0'`).
- `DestinationIpv6CidrBlock (string, optional)`: IPv6 CIDR.
- `GatewayId (string, optional)`: Internet gateway ID for the route.
- `NatGatewayId (string, optional)`: NAT gateway ID for the route.
- `TransitGatewayId (string, optional)`: Transit gateway ID.
- `VpcPeeringConnectionId (string, optional)`: Peering connection ID.
- `DryRun (boolean, optional)`: Checks permissions (default: `False`).

# associate_route_table
* Description: Associates a route table with a subnet.
* Example: `create_vpc.py, configure_subnet_for_autoscaling.py`
* Arguments:
- `RouteTableId (string, required)`: The route table ID.
- `SubnetId (string, required)`: The subnet ID.

# describe_route_tables
* Description: Retrieves route table information.
* Example: `vpc_inventory_tagging.py`
* Arguments:
- `RouteTableIds (list, optional)`: List of route table IDs.
- `Filters (list, optional)`: Filters, e.g., `[{'Name': 'vpc-id', 'Values': ['vpc-1234567890abcdef0']}].
- `NextToken (string, optional)`: Pagination token.
- `MaxResults (integer, optional)`: Maximum results (5–1000).


------------------------------>


4. Security Group Management
# create_security_group
* Description: Creates a security group in a VPC.
* Example: `create_security_group.py`
* Arguments:
- `GroupName (string, required)`: Name of the security group (e.g., `'web-sg'`).
- `Description (string, required)`: Description of the security group.
- `VpcId (string, required)`: The VPC ID.
- `TagSpecifications (list, optional)`: Tags, e.g., `[{'ResourceType': 'security-group', 'Tags': [{'Key': 'Name', 'Value': 'web-sg'}]}]`..

# delete_security_group
* Description: Deletes a security group.
* Example: `delete_vpc.py`
* Arguments:
- `GroupId (string, required)`: The security group ID (e.g., `'sg-1234567890abcdef0'`).

# authorize_security_group_ingress
* Description: Adds inbound rules to a security group.
* Example: `create_security_group.py`
* Arguments:
- `GroupId (string, required)`: The security group ID.
- `IpPermissions (list, required)`: List of rules, each with:
  - `IpProtocol (string)`: Protocol ('tcp', 'udp', 'icmp', '-1' for all).
  - `FromPort (integer)`: Start of port range (e.g., `80`).
  - `ToPort (integer)`: End of port range (e.g., `80`).
  - `IpRanges (list)`: List of {'CidrIp': '0.0.0.0/0', 'Description': 'HTTP access'}.
  - `Ipv6Ranges (list, optional)`: IPv6 CIDRs.
  - `PrefixListIds (list, optional)`: Prefix list IDs.
  - `UserIdGroupPairs (list, optional)`: Security group pairs for inter-group access.

# describe_security_groups
* Description: Retrieves security group information.
* Example: `vpc_inventory_tagging.py`
* Arguments:
- `GroupIds (list, optional)`: List of security group IDs.
- `Filters (list, optional)`: Filters, e.g., `[{'Name': 'vpc-id', 'Values': ['vpc-1234567890abcdef0']}]`.
- `NextToken (string, optional)`: Pagination token.
- `MaxResults (integer, optional)`: Maximum results (5–1000).


-------------------------------->


5. Internet Gateway Management
# create_internet_gateway
* Description: Creates an internet gateway.
* Example: `create_vpc.py`
* Arguments:
- `TagSpecifications (list, optional)`: Tags, e.g., `[{'ResourceType': 'internet-gateway', 'Tags': [{'Key': 'Name', 'Value': 'prod-igw'}]}]`.

# delete_internet_gateway
* Description: Deletes an internet gateway.
* Example: `delete_vpc.py`
* Arguments:
- `InternetGatewayId (string, required)`: The internet gateway ID (e.g., `'igw-1234567890abcdef0'`).

# attach_internet_gateway
* Description: Attaches an internet gateway to a VPC.
* Example: `create_vpc.py`
* Arguments:
- `InternetGatewayId (string, required)`: The internet gateway ID (e.g., `'igw-1234567890abcdef0'`).
- `VpcId (string, required):` The VPC ID.

# detach_internet_gateway
* Description: Detaches an internet gateway from a VPC.
* Example: `delete_vpc.py`
* Arguments:
- `InternetGatewayId (string, required)`: The internet gateway ID.
- `VpcId (string, required)`: The VPC ID.

# describe_internet_gateways
* Description: Retrieves internet gateway information.
* Example: `vpc_inventory_tagging.py`
* Arguments:
- `InternetGatewayIds (list, optional)`: List of internet gateway IDs.
- `Filters (list, optional)`: Filters, e.g., `[{'Name': 'attachment.vpc-id', 'Values': ['vpc-1234567890abcdef0']}]`.
- `NextToken (string, optional)`: Pagination token.
- `MaxResults (integer, optional): Maximum results (5–1000).


--------------------------------->


6. NAT Gateway Management
# create_nat_gateway
* Description: Creates a NAT gateway for private subnet internet access.
* Example: `create_nat_gateway.py`
* Arguments:
- `SubnetId (string, required)`: The public subnet ID for the NAT gateway.
- `AllocationId (string, required)`: The Elastic IP allocation ID.
- `TagSpecifications (list, optional)`: Tags, e.g., `[{'ResourceType': 'nategateway', 'Tags': [{'Key': 'Name', 'Value': 'prod-nat-gateway}]`.

# delete_nat_gateway
* Description: Deletes a NAT gateway.
* Example: `delete_vpc.py`
* Arguments:
- `NatGatewayId (string, required)`: The NAT gateway ID (e.g., `'nat-1234567890abcdef0'`).

# describe_nat_gateways
* Description: Retrieves NAT gateways information.
* Example: `vpc_inventory_tagging.py`
* Arguments:
- `NatGatewayIds (list, optional)`: List of NAT gateway IDs.
- `Filters (list, optional)`: Filters, e.g., `[{'Name': 'vpc-id', 'Values': ['vpc-1234567890abcdef0']}]`.
- `NextToken (string, optional)`: Pagination token.
- `MaxResults (integer, optional)`: Maximum results (5–1000).

# allocate_address
* Description: Allocates an Elastic IP for a NAT gateway.
* Example: `create_nat_gateway.py`
* Arguments:
- `Domain (string, optional)`: 'vpc' for VPC scope (required for NAT gateways).
- `Address (string, optional)`: Specific public IP (if importing).
- `DryRun (boolean, optional)`: Checks permissions (default: `False`).


---------------------------------->


7. VPC Endpoint Management
# create_vpc_endpoint
* Description: Creates a VPC endpoint for AWS services.
* Example: `create_vpc_endpoint.py`
* Arguments:
- `VpcId (string, required)`: The VPC ID.
- `ServiceName (string, required)`: The AWS service name (e.g., `'com.amazonaws.us-east-1.s3'`).
- `VpcEndpointType (string, optional)`: 'Gateway' or 'Interface' (default: `'Gateway'`).
- `RouteTableIds (list, optional)`: Route tables for Gateway endpoints.
- `SubnetIds (list, optional)`: Subnets for Interface endpoints.
- `SecurityGroupIds (list, optional)`: Security groups for Interface endpoints.
- `TagSpecifications (list, optional)`: Tags, e.g., `[{'ResourceType': 'vpc-endpoint', 'Tags': [{'Key': 'Name', 'Value': 's3-endpoint'}]}]`.

# delete_vpc_endpoints
* Description: Deletes VPC endpoints.
* Example: `delete_vpc.py`
* Arguments:
- `VpcEndpointIds (list, required)`: List of endpoint IDs (e.g., `['vpce-1234567890abcdef0']`).

# describe_vpc_endpoints
* Description: Retrieves VPC endpoint information.
* Example: `vpc_inventory_tagging.py`
* Arguments:
- `VpcEndpointIds (list, optional)`: List of endpoint IDs.
- `Filters (list, optional)`: Filters, e.g., `[{'Name': 'vpc-id', 'Values': ['vpc-1234567890abcdef0']}]`.
- `NextToken (string, optional)`: Pagination token.
- `MaxResults (integer, optional)`: Maximum results (5–1000).


----------------------------->


8. VPC Peering Management
# create_vpc_peering_connection
* Description: Creates a VPC peering connection.
* Example: `create_vpc_peering.py`
* Arguments:
- `VpcId (string, required)`: The requester VPC ID.
- `PeerVpcId (string, required)`: The accepter VPC ID.
- `PeerOwnerId (string, optional)`: The AWS account ID of the peer VPC (if different).
- `PeerRegion (string, optional)`: The region of the peer VPC (if cross-region).
- `TagSpecifications (list, optional)`: Tags, e.g., `[{'ResourceType': 'vpc-peering-connection', 'Tags': [{'Key': 'Name', 'Value': 'dev-prod-peering'}]}]`.

# accept_vpc_peering_connection
* Description: Accepts a VPC peering connection request.
* Example: `create_vpc_peering.py`
* Arguments:
- `VpcPeeringConnectionId (string, required)`: The peering connection ID (e.g., `'pcx-1234567890abcdef0'`).

# delete_vpc_peering_connection
* Description: Deletes a peering connection.
* Example:
* Arguments:
- `VpcPeeringConnectionId (string, required)`: The peering connection ID (e.g., `'pcx-1234567890abcdef0'`).

# describe_vpc_peering_connections
* Description: Retrieves peering connection information.
* Example: `vpc_inventory_tagging.py`
* Arguments:
- `VpcPeeringConnectionIds (list, optional)`: List of peering connection IDs.
- `Filters (list, optional)`: Filters, e.g., `[{'Name': 'requester-vpc-id', 'Values': ['vpc-1234567890abcdef0']}]`.
- `NextToken (string, optional)`: Pagination token.
- `MaxResults (integer, optional)`: Maximum results (5–1000).


------------------------------->


9. Tagging (Cross-Component)
# create_tags
* Description: Adds tags to VPC resources (VPC, subnet, route table, etc.).
Example: `vpc_inventory_tagging.py`
* Arguments:
- `Resources (list, required)`: List of resource IDs (e.g., `['vpc-1234567890abcdef0', 'subnet-1234567890abcdef0']`).
- `Tags (list, required)`: List of {'Key': string, 'Value': string} (e.g., `[{'Key': 'Environment', 'Value': 'Production'}]`).


-------------------------------->


10. Flow Logs (Monitoring)
# create_flow_logs
* Description: Enables VPC flow logs for monitoring network traffic.
* Example: `monitor_vpc_flow_logs.py`   
* Arguments:
- `ResourceIds (list, required)`: List of resource IDs (e.g., `['vpc-1234567890abcdef0']`).
- `ResourceType (string, required)`: Type ('VPC', 'Subnet', 'NetworkInterface').
- `TrafficType (string, required)`: Traffic to log ('ALL', 'ACCEPT', 'REJECT').
- `LogDestinationType (string, optional)`: 'cloud-watch-logs' or 's3' (default: `'cloud-watch-logs'`).
- `LogDestination (string, optional)`: ARN of CloudWatch log group or S3 bucket.
- `LogGroupName (string, optional)`: Name of CloudWatch log group.
- `DeliverLogsPermissionArn (string, optional)`: ARN of IAM role for log delivery.
- `TagSpecifications (list, optional)`: Tags for the flow log.


# describe_flow_logs
* Description: Retrieves flow log information.
* Example: `monitor_vpc_flow_logs.py`
* Arguments:
- `FlowLogIds (list, optional)`: List of flow log IDs.
- `Filters (list, optional)`: Filters, e.g., `[{'Name': 'resource-id', 'Values': ['vpc-1234567890abcdef0']}]`.
- `NextToken (string, optional)`: Pagination token.
- `MaxResults (integer, optional)`: Maximum results (5–1000).


------------------------------------>


Summary of Usage Across VPC Components
# VPC: 
Use `create_vpc` to define the network (e.g., `CidrBlock` for IP range), `modify_vpc_attribute` for DNS settings, and `describe_vpcs` for inventory. Tagging via `create_tags` is critical for organization (as in `vpc_inventory_tagging.py`).

# Subnets: 
`create_subnet` specifies `CidrBlock` and `AvailabilityZone` for segmentation. `modify_subnet_attribute` enables public IPs for Auto Scaling (as in `configure_subnet_for_autoscaling.py`).

# Route Tables: 
`create_route_table` and `create_route` configure routing (e.g., to `internet` or `NAT gateways`). `associate_route_table` links subnets to routes (as in `create_vpc.py`, `configure_private_subnet.py`).

# Security Groups: 
`create_security_group` and `authorize_security_group_ingress` define access rules (e.g., HTTP/SSH in `create_security_group.py`).

# Internet Gateways: 
`create_internet_gateway` and `attach_internet_gateway` enable public internet access (as in `create_vpc.py`).

# NAT Gateways: 
`create_nat_gateway` with `AllocationId` and `SubnetId` supports private subnet internet access (as in `create_nat_gateway.py`).

# VPC Endpoints: 
`create_vpc_endpoint` with `ServiceName` and `RouteTableIds` enables private AWS service access (as in `create_vpc_endpoint.py`).

# VPC Peering: 
`create_vpc_peering_connection` and `accept_vpc_peering_connection` facilitate cross-VPC communication (as in `create_vpc_peering.py`).

# Flow Logs: 
`create_flow_logs` and `describe_flow_logs` monitor network traffic, integrating with CloudWatch (as in `monitor_vpc_flow_logs.py`).

# Tagging: 
`create_tags applies` metadata across all components for cost tracking and inventory (as in `vpc_inventory_tagging.py`).


------------------------------------->


==> Notes
- Prerequisites: Ensure `AWS credentials` are configured (e.g., via `~/.aws/credentials` or `IAM roles`). Replace placeholders like `'vpc-1234567890abcdef0'` with actual IDs.

- Error Handling: Use `try-except` blocks with `ClientError` for robustness, as shown in previous scripts.

- Security: Use least privilege `IAM policies`. Avoid hardcoding credentials; use `environment variables` or `AWS Secrets Manager`:
python
```py

import os
boto3.client('ec2', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
```

- Pagination: Handle `NextToken` for methods like `describe_vpcs`, `describe_subnets`, etc., in large environments:

```py

import boto3
ec2_client = boto3.client('ec2')

response = ec2_client.describe_vpcs()
while 'NextToken' in response:
    print(response['Vpcs'])

# or,

response = ec2_client.describe_vpcs(NextToken=response.get('NextToken'))

```

- Cost: Be aware of costs for NAT gateways, VPC endpoints, and flow logs. For API pricing, check `https://x.ai/api`.

