# Integrated Webserver build automation using Ansible, Flask, and Lambda

## Project Overview

This project automates the deployment and configuration of Tomcat instances on AWS EC2 using Ansible, AWS Lambda, and a Flask-based web interface. It streamlines server builds by allowing users to configure Tomcat server environments dynamically, specifying instance types, custom ports, and more. This solution is designed to reduce manual configuration time, ensure consistency, and enhance scalability for Tomcat-based deployments.

### Key Features
- **Flask Web Interface:** Users can fill out a web form to set build parameters, such as EC2 instance type and Tomcat instance details.
- **AWS Lambda Functions:** Orchestrates the EC2 provisioning and triggers Ansible playbooks hosted on a remote Azure server.
- **AWS SNS Notifications:** Coordinates communication between Lambda functions and sends build status notifications.
- **DynamoDB Integration:** Stores build metadata for easy tracking and auditing.
- **Ansible Playbooks:** Automates server setup, including OpenJDK installation, Tomcat configuration, and custom port assignments.
- **Automated Documentation:** Outputs deployment details in a README.txt file within the deployed server environment.

---

## Workflow

1. **User Request**: The user submits a request via the Flask web interface, specifying parameters for the Tomcat server instance.
2. **Lambda - EC2 Provisioning**: The first Lambda function reads the parameters, provisions the EC2 instance with a Red Hat Linux (RHL) AMI, and logs the configuration in DynamoDB.
3. **SNS Notification**: Once EC2 provisioning is complete, SNS sends a message to trigger the next step.
4. **Lambda - Ansible Execution**: The second Lambda function receives the SNS message, connects to an Azure server hosting the Ansible playbook, and uses Paramiko to execute it with the provided parameters.
5. **Ansible Configuration**:
   - Installs OpenJDK and sets up directories for Tomcat.
   - Creates unique user and group for each Tomcat instance.
   - Configures server.xml files with custom port mappings.
   - Generates a README.txt file with instance details.

