import paramiko
import os
import boto3
import smtplib
import ssl
import json

# Fetch environment variables for email username and password
username = os.environ['username']
epassword = os.environ['epassword']

# Subject for the email notification
subject = "Your build has commissioned"

# Email sending code block
def send_email(user, pwd, recipient, email_subject, email_body):
    """
    Sends an email notification using SMTP.
    
    Parameters:
    - user: Sender email address (Gmail)
    - pwd: Password for the sender's email account
    - recipient: Recipient email address
    - email_subject: Subject of the email
    - email_body: Body of the email
    """
    SMTP_SERVER = "smtp.gmail.com"
    PORT = 587
    print(user, pwd)

    # Create SSL context to secure the email connection
    context = ssl.create_default_context()

    # Establish connection to SMTP server
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls(context=context)  # Enable TLS encryption
        server.login(user, pwd)  # Login to the email account
        # Format and send the email
        message = f"Subject: {email_subject}\n\n{email_body}"
        server.sendmail(user, recipient, message)

# Main Lambda handler function
def lambda_handler(event, context):
    """
    AWS Lambda function to trigger Tomcat instance deployment and send an email notification.
    
    This function connects to an EC2 instance via SSH, runs an Ansible playbook to deploy Tomcat instances, 
    and sends an email confirmation with instance details.
    """
    # Print incoming event for debugging purposes
    print(event)

    # Parse and load the SNS message from the event
    message = event['Records'][0]['Sns']['Message']
    message = message.replace("\'", "\"")  # Replace single quotes with double quotes
    message = json.loads(message)  # Convert JSON string to a dictionary

    # Extract details from the SNS message
    ip = message['ip']
    parameters = message['instance_names']

    # Fetch additional environment variables for SSH
    ip_address = os.environ['ip_address']
    password = os.environ['entrence']

    # Establish SSH connection using Paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add the host key
    ssh.connect(ip_address, port=22, username='ansible', password=password, timeout=10)  # Connect to the instance

    # Prepare parameters for Ansible playbook execution
    print(parameters)
    tomcat_instances = f'{{"tomcat_instances":{parameters}}}'

    # Execute the Ansible playbook on the EC2 instance
    print(
        f"sudo nohup ansible-playbook -i {ip}, tomcat_installer.yml -e '{tomcat_instances}' --private_key=/ansible/tomcatkey.pem > tomcat_output.log 2>&1 &")
    stdin, stdout, stderr = ssh.exec_command(
        f"nohup ansible-playbook -i {ip}, tomcat_installer.yml -e '{tomcat_instances}' --private-key=tomcatkey.pem > tomcat_output.log 2>&1 &")

    # Print the output of the command for debugging
    print(stdout.read().decode())
    print(stderr.read().decode())

    # Email body with instance details for the recipient
    body = f"""
    Dear Member,

    We are pleased to inform you that the Integrated Web Server Build Automation (IWBA) process for Tomcat instance deployment has been commissioned for build. Below are the key details for the setup and access:

    Project Details:

    Allocated Server: RHEL server as per the AWS instance specifications
    Server IP Address: {ip}
    Tomcat Instances: {','.join(parameters)}
    Instance Type : {message['instance_type']}

    Automation Process:

    The build automation uses Ansible to deploy and configure the Tomcat instances in parallel.
    This process is expected to complete within 15 minutes, depending on the number of Tomcat instances.

    Access and Instructions:

    A readme.txt file with detailed setup instructions and usage notes has been generated at /local/apps folder. This file provides essential information to guide you through the instance setup and verification steps.
    To access the EC2 instance, please ensure you have the AWS key associated with this deployment.

    If you have any questions or need further assistance, please don't hesitate to reach out to iwbaproject@gmail.com.

    IWBA Tool
    """

    # Fetch recipient's email from the message and send notification
    to_email = message['email']
    send_email(username, epassword, to_email, subject, body)
