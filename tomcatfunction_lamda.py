import json
import time
import boto3

# Function to publish a message to an Amazon SNS topic
def sns_publish(message):
    # Create an SNS client
    client = boto3.client("sns")
    
    # Publish the message to the specified SNS topic
    response = client.publish(
        TopicArn='SNS-Trigger-Job-With-ID',  # The ARN of the SNS topic
        Message=message                      # The message to send
    )
    
    # Print the response from SNS for logging and debugging
    print(f"SNS Response: {response}")
    print("Message sent to triggerjob lambda")

# Main Lambda handler function
def lambda_handler(event, context):
    # Specify the DynamoDB table name where instance details will be stored
    db_name = 'tomcat'

    # Initialize clients for AWS services
    db_client = boto3.client('dynamodb')    # DynamoDB client for database operations
    ec2_resource = boto3.resource('ec2')    # EC2 resource for creating instances
    ec2_client = boto3.client('ec2')        # EC2 client for instance management
    ses_client = boto3.client('ses')        # SES client for email services (unused here)
    ec2_waiter = ec2_client.get_waiter('instance_status_ok')  # Waiter for EC2 instance status

    # Parse the incoming JSON event body
    body = json.loads(event['body'])
    print("BODY", body)
    print("TYPE", type(body))

    # Convert the instance name to a JSON-compliant format
    input_items = str(body['instance_names']).replace("'", "\"")

    # Create an EC2 instance with the provided configuration
    response = ec2_resource.create_instances(
        ImageId='ami-id',                    # Amazon Machine Image (AMI) ID
        InstanceType=body['instance_type'],  # Instance type, e.g., t2.micro
        SecurityGroupIds=['sg-group'],       # Security group for the instance
        SubnetId='subnet-idd0',              # Subnet ID within the VPC
        KeyName='tomcatkey',                 # Key pair name for SSH access
        MaxCount=1,                          # Number of instances to create
        MinCount=1                           # Minimum instances required
    )
    
    # Wait for a short time for the instance to initialize
    time.sleep(10)

    # Retrieve the instance ID of the newly created EC2 instance
    server = response[0].instance_id

    # Describe the instance to obtain its public IP address
    ec2 = ec2_client.describe_instances(
        InstanceIds=[server]
    )
    ip = ec2['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(server, ip)
    ip_dict = {'ip': ip}

    # Add the public IP to the body dictionary
    body.update(ip_dict)
    print("UPDATED BODY", body)
    print(type(body))

    # Wait until the EC2 instance reaches the 'running' state and passes status checks
    ec2_waiter.wait(
        InstanceIds=[
            ec2['Reservations'][0]['Instances'][0]['InstanceId'],
        ],
        WaiterConfig={
            'Delay': 10,         # Delay in seconds between each check
            'MaxAttempts': 60    # Maximum number of attempts
        }
    )

    # Store instance details in DynamoDB
    db_response = db_client.put_item(
        TableName=db_name,
        Item={
            'name': {
                'S': input_items
            },
            'ip': {
                'S': ip
            },
            'type': {
                'S': body['instance_type'] 
            },
            'email': {
                'S': body['email']
            }
        }
    )

    # Publish instance information to SNS to trigger downstream processes
    sns_publish(str(body))

    # Log the instance names and DynamoDB response
    print(input_items, db_response)
