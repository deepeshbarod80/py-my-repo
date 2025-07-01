import boto3
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def lambda_handler(event, context):
    """
    Lambda function to monitor EC2 instances and send a daily report via email.
    """
    # Initialize boto3 clients
    ec2_client = boto3.client('ec2')
    ses_client = boto3.client('ses')
    
    # Get all EC2 instances
    response = ec2_client.describe_instances()
    
    # Prepare the email content
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    email_subject = f"EC2 Monitoring Report - {current_date}"
    
    # HTML for better email formatting
    html_content = f"""
    <html>
    <head>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
        </style>
    </head>
    <body>
        <h2>EC2 Instance Monitoring Report - {current_date}</h2>
        <table>
            <tr>
                <th>Instance ID</th>
                <th>Instance Type</th>
                <th>State</th>
                <th>Private IP</th>
                <th>Public IP</th>
                <th>Launch Time</th>
            </tr>
    """
    
    # Process each reservation and instance
    instance_count = 0
    running_count = 0
    stopped_count = 0
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_count += 1
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            state = instance['State']['Name']
            
            if state == 'running':
                running_count += 1
            elif state == 'stopped':
                stopped_count += 1
            
            # Get IP addresses (if available)
            private_ip = instance.get('PrivateIpAddress', 'N/A')
            public_ip = instance.get('PublicIpAddress', 'N/A')
            
            # Format launch time
            launch_time = instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')
            
            # Add row to table
            html_content += f"""
            <tr>
                <td>{instance_id}</td>
                <td>{instance_type}</td>
                <td>{state}</td>
                <td>{private_ip}</td>
                <td>{public_ip}</td>
                <td>{launch_time}</td>
            </tr>
            """
    
    # Add summary and close HTML
    html_content += f"""
        </table>
        <h3>Summary:</h3>
        <p>Total Instances: {instance_count}</p>
        <p>Running Instances: {running_count}</p>
        <p>Stopped Instances: {stopped_count}</p>
    </body>
    </html>
    """
    
    # Create plain text version as well
    text_content = f"""
    EC2 Instance Monitoring Report - {current_date}
    
    Summary:
    Total Instances: {instance_count}
    Running Instances: {running_count}
    Stopped Instances: {stopped_count}
    """
    
    # Create the email message
    message = MIMEMultipart('alternative')
    message['Subject'] = email_subject
    message['From'] = 'your-verified-email@example.com'  # Replace with your SES verified email
    message['To'] = 'recipient@example.com'  # Replace with recipient email
    
    # Attach parts
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    message.attach(part1)
    message.attach(part2)
    
    # Send the email
    try:
        response = ses_client.send_raw_email(
            Source='your-verified-email@example.com',  # Replace with your SES verified email
            Destinations=['recipient@example.com'],  # Replace with recipient email
            RawMessage={'Data': message.as_string()}
        )
        print(f"Email sent! Message ID: {response['MessageId']}")
        return {
            'statusCode': 200,
            'body': f"Email sent successfully! Message ID: {response['MessageId']}"
        }
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error sending email: {str(e)}"
        }