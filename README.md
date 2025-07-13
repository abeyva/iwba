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
  
# 🚀 Integrated Webserver Build Automation (IWBA) using Ansible, AWS & Azure

![IWBA Banner](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiBxeBu3nnHuK6LFFIOKaiIBoNAOFbQmcD1L58Mm7_Z2vPZVNbPfxHY454tXhPV3GnwSIEolHLbq_6DBNCQ0g4fTPqJccK0QMBTrc-k4C_RUK2ry4-Na5yj6KTPCowfVeVe7vihnuM-qxbF1lxY83BiFbFphUblpZXzfherp6bmO2aNHtcHmmfPv3wmS1E/s1370/iwba2.png)

## 📌 Description

**IWBA (Integrated Webserver Build Automation)** is a cloud-native automation solution to deploy and configure **Apache Tomcat servers** using:
- **AWS Lambda**
- **Azure-hosted Ansible**
- **Python (Paramiko)**
- **DynamoDB & EC2**

It streamlines the server setup process based on user-submitted parameters through a web form. Ideal for developers, DevOps engineers, and cloud administrators aiming to reduce manual intervention and improve deployment reliability.

---

## 🧠 Architecture Overview

![Architecture Diagram](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgPeQbxOfab_dG3C4Xabi5W-4LV7Fw0rXgrwyiDqfOK5_RJGG7txzi0lmZmFGcI8yPcmh3yt7mnua9S8fQNiiIRqBZqFhdg14Gor6P6jFdywyyMjchtVtK0A4rogA5MqElnaNig10DSkfsEd-hQiF9gMPHvUyMP5hzowsZu3IlHkB-n2Eu_QyDr2w2__EU/s1359/iwba.png)

---

## 🏗️ Workflow Breakdown

### Step 1: User Input
- User fills out a **Flask-based web form** with:
  - Tomcat instance name
  - AWS EC2 instance type
  - Email address

### Step 2: AWS Lambda #1
- Stores data in **DynamoDB**
- Provisions a **Red Hat Linux EC2** instance using parameters

### Step 3: AWS Lambda #2 (SNS Trigger)
- Uses **Python Paramiko** to SSH into an **Azure-hosted Ansible server**
- Passes all build parameters to Ansible

### Step 4: Ansible Automation
- Logs into EC2 instance
- Creates `/local/apps` and necessary directories
- Sets up users and groups
- Installs **OpenJDK** and downloads Tomcat
- Modifies `server.xml` with user-defined ports
- Writes deployment details to `README.txt`

---

## 💻 Technologies Used

- **AWS Lambda**
- **Amazon EC2 (Red Hat Linux)**
- **DynamoDB**
- **Azure Virtual Machine (CentOS 8.5)**
- **Python** (for both Lambda and Paramiko)
- **Ansible** (Playbook automation)
- **Apache Tomcat**
- **OpenJDK**

---

## 📦 Infrastructure Requirements

- **Ansible Master**: Azure-hosted CentOS 8.5 with 4 GB RAM
- **Target Server**: AWS EC2 with RHEL
- **Test Environment**: VirtualBox with CentOS Stream 9

---

## 📋 Outputs

- EC2 instance created with user parameters
- Entry recorded in DynamoDB
- Multiple Tomcat instances running on custom ports
- `README.txt` file generated with instance details, startup commands

---

## ✅ Features & Benefits

- ⚙️ **Fully Automated Tomcat Deployment**
- 🔐 **User-defined Configurations via Web UI**
- 📤 **Email Notification with Build Summary**
- 🚀 **Zero Manual Server Login**
- 📝 **Readable and Reusable Setup Summary**
- 🧱 **Supports Multi-Instance Tomcat Configuration**

---

## 🔭 Future Scope

- 💡 Support for WebLogic, JBoss, and WebSphere
- 🔌 REST API for 3rd-party integration
- 🔁 Self-healing EC2 automation
- 🕵️ Drift detection for config integrity

---

## 📬 Connect

If this project helps you or inspires you, feel free to contribute or drop a star on the repo.

👉 GitHub: [github.com/abeyva/iwba](https://github.com/abeyva/iwba)

---



