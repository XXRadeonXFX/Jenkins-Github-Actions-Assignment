# Jenkins CI/CD Pipeline for Flask Application

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://jenkins.example.com)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.0%2B-red)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/docker-enabled-blue)](https://www.docker.com/)

## 📋 Project Description

This project demonstrates a complete **Jenkins CI/CD pipeline** for a Python Flask web application. The pipeline automates testing, building, and deployment processes with comprehensive error handling and email notifications.

### 🎯 Objectives
- Set up automated CI/CD pipeline using Jenkins
- Implement testing, building, and deployment stages
- Configure email notifications for build status
- Deploy Flask application to EC2 using Docker
- Demonstrate best practices for DevOps automation

## ✨ Features

- **🔄 Automated CI/CD Pipeline**: Complete automation from code commit to deployment
- **🧪 Automated Testing**: Unit tests with pytest integration
- **🐳 Docker Containerization**: Consistent deployment environment
- **☁️ EC2 Deployment**: Cloud-based application hosting
- **📧 Email Notifications**: Attractive HTML email alerts for build status
- **🔍 Health Checks**: Automated application health monitoring
- **🛠️ Self-Healing**: Automatic dependency installation and error recovery
- **📊 Comprehensive Logging**: Detailed build and deployment logs

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│   Jenkins CI    │───▶│   EC2 Server    │
│                 │    │                 │    │                 │
│ • Flask App     │    │ • Build         │    │ • Docker        │
│ • Dockerfile    │    │ • Test          │    │ • Application   │
│ • Jenkinsfile   │    │ • Deploy        │    │ • Health Check  │
│ • Requirements  │    │ • Notify        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

### System Requirements
- **Jenkins Server**: Version 2.400+ with following plugins:
  - Pipeline Plugin
  - SSH Agent Plugin
  - Email Extension Plugin
  - Docker Pipeline Plugin
- **Python**: Version 3.8 or higher
- **Docker**: Version 20.10 or higher
- **AWS EC2**: Ubuntu 20.04+ instance with SSH access

### Required Tools
```bash
# On Jenkins Server
sudo apt update
sudo apt install -y python3 python3-pip python3-venv docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker jenkins

# On EC2 Server
sudo apt update
sudo apt install -y docker.io curl
sudo systemctl start docker
sudo systemctl enable docker
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/flask-jenkins-pipeline.git
cd flask-jenkins-pipeline
```

### 2. Configure Jenkins
1. **Install Jenkins** on your server
2. **Install required plugins**:
   - Navigate to `Manage Jenkins` → `Manage Plugins`
   - Install: Pipeline, SSH Agent, Email Extension, Docker Pipeline
3. **Configure SSH credentials**:
   - Go to `Manage Jenkins` → `Manage Credentials`
   - Add SSH private key for EC2 access
4. **Setup email notifications**:
   - Configure SMTP settings in `Manage Jenkins` → `Configure System`

### 3. Create Jenkins Pipeline
1. **New Item** → **Pipeline**
2. **Pipeline Script from SCM**:
   - SCM: Git
   - Repository URL: `https://github.com/yourusername/flask-jenkins-pipeline.git`
   - Script Path: `Jenkinsfile`

### 4. Configure Environment Variables
Update the following in your `Jenkinsfile`:
```groovy
environment {
    SSH_CREDENTIALS_ID = "your-ssh-credential-id"
    EC2_USER = "ubuntu"
    EC2_HOST = "your-ec2-ip-address"
    NOTIFICATION_EMAIL = "your-email@domain.com"
}
```

## 📁 Project Structure

```
flask-jenkins-pipeline/
├── 📄 README.md                 # Project documentation
├── 📄 Jenkinsfile              # Jenkins pipeline configuration
├── 📄 Dockerfile               # Docker container configuration
├── 📄 requirements.txt         # Python dependencies
├── 🐍 app.py                   # Flask application
├── 🧪 test_app.py              # Unit tests
├── 📸 screenshots/             # Pipeline execution screenshots
│   ├── pipeline-overview.png
│   ├── build-success.png
│   ├── deployment-logs.png
│   └── email-notifications.png
└── 📚 docs/                    # Additional documentation
    ├── setup-guide.md
    └── troubleshooting.md
```

## 🔄 Pipeline Stages

### Stage 1: 🔍 Environment Validation
- Validates build environment
- Installs Docker if missing
- Checks required files existence
- Ensures all dependencies are available

### Stage 2: 📦 Install Dependencies
- Creates Python virtual environment
- Installs required packages from `requirements.txt`
- Upgrades pip to latest version

### Stage 3: 🧪 Run Tests
- Executes unit tests using pytest
- Generates test reports
- Continues on test failures with warnings

### Stage 4: 🐳 Build Docker Image
- Builds Docker image for the application
- Implements retry logic for failed builds
- Verifies image creation success

### Stage 5: 🚀 Deploy to EC2
- Tests SSH connectivity to EC2
- Sets up EC2 environment (installs Docker if needed)
- Copies application files
- Deploys containerized application
- Configures container with restart policies

### Stage 6: 🏥 Health Check
- Performs application health verification
- Tests HTTP endpoints
- Implements retry logic with 5 attempts
- Collects debug information on failures

## 📧 Email Notifications

The pipeline sends beautifully formatted emails for different build statuses:

### ✅ Success Notifications
- **Professional ASCII borders**
- **Complete build details and timestamps**
- **Direct application links**
- **Quick access links to Jenkins**

### ❌ Failure Notifications
- **Detailed troubleshooting guide**
- **Common failure points checklist**
- **Step-by-step debug instructions**
- **Multiple investigation links**

### ⚠️ Unstable Notifications
- **Test failure warnings**
- **Application status verification**
- **Review requirements**

## 🛠️ Configuration

### Jenkins Pipeline Configuration
```groovy
// Essential environment variables
environment {
    SSH_CREDENTIALS_ID = "ec2-ssh-key"           # SSH credential ID
    EC2_USER = "ubuntu"                          # EC2 username
    EC2_HOST = "3.110.222.41"                   # EC2 IP address
    APP_DIR = "/home/ubuntu/student-app"         # Application directory
    DOCKER_IMAGE = "student-app"                 # Docker image name
    CONTAINER_NAME = "student-app-container"     # Container name
    APP_PORT = "5000"                           # Application port
    NOTIFICATION_EMAIL = "your-email@gmail.com"  # Notification email
}
```

### EC2 Security Group Settings
Ensure your EC2 security group allows:
- **SSH (Port 22)**: For Jenkins deployment access
- **HTTP (Port 5000)**: For application access
- **HTTPS (Port 443)**: Optional, for secure access

### Email SMTP Configuration
Configure in Jenkins → Manage Jenkins → Configure System:
```
SMTP Server: smtp.gmail.com
SMTP Port: 587
Use SMTP Authentication: ✓
Username: your-email@gmail.com
Password: your-app-password
Use SSL: ✓
```

## 🧪 Testing

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_app.py -v

# Run application locally
python app.py
```

### Pipeline Testing
1. **Push changes** to trigger pipeline
2. **Monitor Jenkins console** for real-time logs
3. **Check email notifications** for build status
4. **Verify application** at `http://your-ec2-ip:5000`

## 📸 Screenshots

### Pipeline Overview
![Pipeline Overview](screenshots/pipeline-overview.png)

### Successful Build
![Build Success](screenshots/build-success.png)

### Deployment Logs
![Deployment Logs](screenshots/deployment-logs.png)

### Email Notifications
![Email Notifications](screenshots/email-notifications.png)

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 🚨 SSH Connection Failed
```bash
# Check SSH connectivity
ssh -i your-key.pem ubuntu@your-ec2-ip

# Verify security group settings
# Ensure port 22 is open for your IP
```

#### 🚨 Docker Build Failed
```bash
# Check Docker service
sudo systemctl status docker

# Free up disk space
docker system prune -f

# Check Dockerfile syntax
docker build -t test-image .
```

#### 🚨 Application Not Responding
```bash
# Check container status
docker ps -a

# View container logs
docker logs student-app-container

# Check port availability
sudo netstat -tlnp | grep :5000
```

#### 🚨 Email Notifications Not Working
1. **Verify SMTP settings** in Jenkins configuration
2. **Check email credentials** and app passwords
3. **Test email configuration** using Jenkins built-in test
4. **Review firewall settings** for SMTP ports

### Debug Commands
```bash
# Jenkins server debugging
sudo systemctl status jenkins
sudo tail -f /var/log/jenkins/jenkins.log

# EC2 server debugging
docker ps -a
docker logs student-app-container
sudo df -h
sudo free -h

# Network debugging
curl -I http://your-ec2-ip:5000
telnet your-ec2-ip 5000
```

## 📈 Monitoring and Maintenance

### Regular Maintenance Tasks
- **Monitor disk space** on Jenkins and EC2 servers
- **Update Docker images** regularly for security patches
- **Review and rotate SSH keys** periodically
- **Clean up old Jenkins builds** to save space
- **Update Python dependencies** for security fixes

### Performance Optimization
- **Use Docker multi-stage builds** to reduce image size
- **Implement caching strategies** for faster builds
- **Optimize test execution** with parallel testing
- **Monitor resource usage** and scale as needed

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines
- Follow **PEP 8** for Python code style
- Add **unit tests** for new features
- Update **documentation** for any changes
- Test the **complete pipeline** before submitting

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- **Jenkins Community** for excellent documentation
- **Flask Team** for the amazing web framework
- **Docker** for containerization technology
- **AWS** for cloud infrastructure

## 📞 Support

For support and questions:
- **Email**: your-email@domain.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/flask-jenkins-pipeline/issues)
- **Documentation**: [Project Wiki](https://github.com/yourusername/flask-jenkins-pipeline/wiki)

---

⭐ **Star this repository** if you found it helpful!

🐛 **Found a bug?** [Report it here](https://github.com/yourusername/flask-jenkins-pipeline/issues)

💡 **Have suggestions?** [Start a discussion](https://github.com/yourusername/flask-jenkins-pipeline/discussions)
