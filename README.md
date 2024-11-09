#Intagarated Webserver build automation using Ansible, Flask, and Lambda

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

---

## Directory Structure
```plaintext
project-root/
│
├── ansible/                       # Ansible playbooks and configuration files
├── flask_app/                     # Flask web interface files
│   ├── app.py                     # Main Flask application
│   ├── templates/                 # HTML templates for the form interface
│   └── static/                    # Static files (CSS, JS)
├── lambda_functions/              # AWS Lambda functions for EC2 and Ansible orchestration
├── README.md                      # Project overview and setup instructions
└── requirements.txt               # Dependencies
```

---

## Prerequisites

- **AWS Account**: Access to AWS Lambda, EC2, DynamoDB, and SNS services.
- **Azure Account**: Ansible playbook storage and execution environment.
- **IAM Roles**: Ensure necessary permissions are configured for AWS services.
- **Python 3.x**: Required for running the Flask web interface locally.

---

## Deployment Steps

1. **Clone Repository**: 
   ```bash
   git clone <repository-url>
   ```

2. **Set Up Flask Web Interface**:
   - Navigate to the `flask_app` directory and install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the Flask application locally:
     ```bash
     python app.py
     ```

3. **Deploy Lambda Functions**:
   - Configure the Lambda functions for EC2 provisioning and SNS communication.
   - Update Lambda permissions to connect to Azure using Paramiko.

4. **Configure Ansible Playbook**:
   - Store the Ansible playbook on the Azure server, ensuring SSH access.
   - Customize any variables as needed within `ansible/playbook.yml`.

5. **Testing**:
   - Fill in the form on the Flask web interface.
   - Submit a test request to initiate the deployment process.
   - Verify the EC2 instance is set up and the README.txt file is generated with the correct details.

---

## License
This project is licensed under the MIT License.

---

This README provides a structured overview of the project, including setup and deployment steps. Let me know if you'd like any adjustments or additional sections.
