# Student Management System - CI/CD Pipeline

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://jenkins.example.com)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.3%2B-red)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/docker-enabled-blue)](https://www.docker.com/)
[![MongoDB](https://img.shields.io/badge/mongodb-supported-green)](https://www.mongodb.com/)

## 📋 Project Overview

This project demonstrates **complete CI/CD pipelines** for a Python Flask Student Management System using both **Jenkins** and **GitHub Actions**. The application securely connects to MongoDB using environment secrets and includes comprehensive testing, deployment automation, and monitoring.

### 🎯 Assignment Objectives
- **Jenkins CI/CD Pipeline**: Automated testing and deployment with email notifications
- **GitHub Actions Workflow**: Multi-environment deployment using GitHub Secrets  
- **Security**: Secure handling of MongoDB connection strings via secrets
- **Documentation**: Complete setup and usage instructions

## ✨ Key Features

- **🔐 Secure Secret Management**: MongoDB URI handled via GitHub/Jenkins secrets
- **🧪 Comprehensive Testing**: Unit tests with fallback support
- **🐳 Docker Containerization**: Consistent deployment environment
- **☁️ Multi-Environment Deployment**: Staging and Production environments
- **📧 Email Notifications**: Build status alerts (Jenkins)
- **🏥 Health Monitoring**: Automated health checks and monitoring
- **📊 Code Coverage**: Test coverage reporting
- **🔒 Security Scanning**: Vulnerability detection

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│ Jenkins/Actions │───▶│   Deployment    │
│                 │    │                 │    │                 │
│ • Flask App     │    │ • Build         │    │ • Staging       │
│ • Tests         │    │ • Test          │    │ • Production    │
│ • Secrets       │    │ • Security Scan │    │ • Health Check  │
│ • Pipelines     │    │ • Deploy        │    │ • Monitoring    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

# 📧 Configuring Gmail SMTP in Jenkins with App Password

When using Gmail to send email notifications from Jenkins, standard username/password authentication often fails due to Google’s security restrictions. This guide walks you through setting up **App Passwords** to enable secure SMTP access in Jenkins.

---

## 🔐 Step-by-Step Setup Using Gmail App Password

### ✅ 1. Enable 2-Step Verification

To use App Passwords, **2-Step Verification** must be enabled for your Gmail account.

* Visit: [Google Account Security Settings](https://myaccount.google.com/security)
* Under **"Signing in to Google"**, enable **2-Step Verification**
* Complete the verification process with your phone

---

### 🔑 2. Generate an App Password

1. Go to: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Log in with your Gmail account (if prompted)
3. Under **"Select app"**, choose **Mail**
4. Under **"Select device"**, choose **Other (Custom name)** and enter `Jenkins`
5. Click **Generate**
6. Google will display a **16-character app password**, e.g.,
   `abcd efgh ijkl mnop`
   **Copy this — you will use it in Jenkins**

---

### ⚙️ 3. Configure SMTP in Jenkins

In your Jenkins dashboard:

1. Go to:
   **Manage Jenkins → Configure System**

2. Scroll to **E-mail Notification** section.

3. Configure the following:

   * **SMTP Server**: `smtp.gmail.com`
   * ✅ **Use SMTP Authentication**
   * **Username**: `yourname@gmail.com`
   * **Password**: *Paste the App Password from Step 2*
   * ✅ **Use SSL** (if using port 465) or ✅ **Use TLS** (if using port 587)
   * **SMTP Port**:

     * `465` for SSL
     * `587` for TLS

4. Click the **“Test configuration by sending test e-mail”** button to verify everything works.

![Email Configuration Test](screenshots/email-test.png)
*Test Show SMTP is working fine*

---


## 🔐 Secret Configuration

### **GitHub Secrets Setup**

1. **Navigate to Repository Settings:**
   ```
   Your Repo → Settings → Secrets and variables → Actions
   ```

2. **Add Required Secrets:**
   ```
   MONGO_URI              = mongodb+srv://username:password@cluster.mongodb.net/student_db
   STAGING_HOST           = your-staging-server-ip
   STAGING_USER           = ubuntu
   STAGING_SSH_KEY        = -----BEGIN OPENSSH PRIVATE KEY-----...
   PRODUCTION_HOST        = your-production-server-ip  
   PRODUCTION_USER        = ubuntu
   PRODUCTION_SSH_KEY     = -----BEGIN OPENSSH PRIVATE KEY-----...

### **Jenkins Credentials Setup**

1. **Navigate to Jenkins Credentials:**
   ```
   Jenkins → Manage Jenkins → Manage Credentials
   ```

2. **Add Secret Text Credentials:**
   ```
   PRINCE_MONGO_URI       = mongodb+srv://username:password@cluster.mongodb.net/student_db
   SSH_CREDENTIALS_ID     = "c3b12c2f-9959-46a6-b763-fc4e303082cb"
   ```

## 📁 Project Structure

```
student-management-cicd/
├── 📄 README.md                    # This documentation
├── 📄 app.py                       # Flask application with secret handling
├── 📄 test_app.py                  # Comprehensive unit tests  
├── 📄 requirements.txt             # Python dependencies
├── 📄 Dockerfile                   # Container configuration
├── 📄 Jenkinsfile                  # Jenkins pipeline definition
├── 📄 sample_data.json             # Jenkins pipeline definition
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 ci-cd.yml            # GitHub Actions workflow
└── 📁 screenshots/                 # Pipeline execution screenshots
    ├── jenkins-pipeline.png
    ├── github-actions.png
    └── deployment-success.png
    └── email-test.png
```

## 🚀 Getting Started

### **Prerequisites**
- Python 3.8+
- Docker 20.10+
- MongoDB Atlas account (or local MongoDB)
- Jenkins server (for Jenkins pipeline)
- GitHub repository (for GitHub Actions)

### **Local Development Setup**

1. **Clone Repository:**
   ```bash
   git clone https://github.com/XXRadeonXFX/Jenkins-Github-Actions-Assignment.git
   cd Jenkins-Github-Actions-Assignment
   ```

2. **Set Environment Variable:**
   ```bash
   export MONGO_URI="mongodb://localhost:27017/"
   # Or for MongoDB Atlas:
   export MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/student_db"
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Tests:**
   ```bash
   pytest test_app.py -v
   ```

5. **Start Application:**
   ```bash
   python app.py
   ```

6. **Visit Application:**
   ```
   http://localhost:5000
   ```

## 🔄 Jenkins CI/CD Pipeline
![Jenkins Pipeline Execution](screenshots/jenkins-pipeline.png)
*Jenkins pipeline showing all stages executing successfully*

### **Pipeline Stages:**

1. **🔍 Environment Validation**
   - Validates build environment
   - Installs missing dependencies
   - Checks required files

2. **📦 Install Dependencies**
   - Creates Python virtual environment
   - Installs packages from requirements.txt

3. **🧪 Run Tests**
   - Executes pytest with coverage
   - Uses MongoDB secret from Jenkins credentials

4. **🐳 Build Docker Image**
   - Builds containerized application
   - Implements build retry logic

5. **🚀 Deploy to EC2**
   - Secure SSH deployment
   - Uses Jenkins credentials for secrets
   - Container deployment with health checks

6. **🏥 Health Check**
   - Application health verification
   - HTTP endpoint testing
   - Failure diagnostics

### **Jenkins Configuration:**

1. **Create Pipeline Job:**
   ```
   New Item → Pipeline → Pipeline script from SCM
   ```

2. **Configure Repository:**
   ```
   SCM: Git
   Repository URL: https://github.com/yourusername/student-management-cicd.git
   Script Path: Jenkinsfile
   ```

3. **Set Build Triggers:**
   ```
   ✓ GitHub hook trigger for GITScm polling
   ✓ Poll SCM: H/5 * * * *
   ```

## ⚡ GitHub Actions Workflow
![GitHub Actions Workflow](screenshots/github-actions.png)
*GitHub Actions workflow with parallel jobs and secret management*

### **Workflow Jobs:**

1. **🧪 Build & Test**
   - Multi-Python version testing (3.9, 3.10, 3.11)
   - Uses `${{ secrets.MONGO_URI }}` for secure database access
   - Code coverage reporting

2. **🔒 Security Scan**
   - Bandit security analysis
   - Dependency vulnerability checking
   - SARIF report generation

3. **🚀 Deploy to Staging**
   - Triggered on `staging` branch push
   - Uses GitHub secrets for secure deployment
   - Automated health verification

4. **🌟 Deploy to Production**
   - Triggered on release publication
   - Production-grade deployment
   - Comprehensive monitoring setup

### **Workflow Features:**

- **Secret Integration**: All sensitive data via GitHub Secrets
- **Multi-Environment**: Separate staging and production deployments
- **Security First**: Vulnerability scanning and secure SSH
- **Health Monitoring**: Automated health checks with retries
- **Artifact Management**: Test reports and coverage data

## 🧪 Testing Strategy

### **Test Categories:**

1. **Unit Tests**
   - Flask endpoint testing
   - Database operation validation
   - Error handling verification

2. **Integration Tests**
   - MongoDB connection testing
   - Secret configuration validation
   - Health endpoint verification

3. **Security Tests**
   - Bandit static analysis
   - Dependency vulnerability scanning

### **Running Tests:**

```bash
# Run all tests
pytest test_app.py -v

# Run with coverage
pytest test_app.py --cov=app --cov-report=html

# Run specific test
pytest test_app.py::test_health_check -v
```

## 🚀 Deployment Environments

### **Staging Environment**
- **Purpose**: Pre-production testing
- **Trigger**: Push to `staging` branch  
- **URL**: `${{ secrets.STAGING_URL }}`
- **Database**: Staging MongoDB instance

### **Production Environment**
- **Purpose**: Live application
- **Trigger**: Release publication
- **URL**: `${{ secrets.PRODUCTION_URL }}`
- **Database**: Production MongoDB cluster

## 🔧 API Endpoints

### **Core Endpoints:**
```
GET  /                     # Welcome message and system info
GET  /health              # Health check for monitoring
GET  /students            # Get all students
POST /students            # Add new student
GET  /students/{id}       # Get student by ID
DELETE /students/{id}     # Delete student
GET  /students/name/{name} # Search students by name
```

### **Example Usage:**
```bash
# Health check
curl http://localhost:5000/health

# Add student
curl -X POST http://localhost:5000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "age": 25}'

# Get all students  
curl http://localhost:5000/students
```

## 📧 Notifications

### **Jenkins Email Notifications:**
- **Success**: Build completion with deployment URL
- **Failure**: Detailed troubleshooting information  
- **Unstable**: Test warnings and review requirements

### **GitHub Actions Notifications:**
- **Built-in**: GitHub UI notifications
- **Optional**: Slack/Teams integration via webhooks

## 🔧 Troubleshooting

### **Common Issues:**

#### **MongoDB Connection Failed**
```bash
# Check secret configuration
echo $MONGO_URI

# Test connection manually
python -c "from pymongo import MongoClient; MongoClient('$MONGO_URI').admin.command('ping')"
```

#### **Jenkins Pipeline Fails**
```bash
# Check Jenkins logs
sudo tail -f /var/log/jenkins/jenkins.log

# Verify credentials
Jenkins → Manage Jenkins → Manage Credentials
```

#### **GitHub Actions Secret Issues**
```bash
# Verify secrets are set
Repository → Settings → Secrets and variables → Actions

# Check workflow logs
Actions tab → Select failed workflow → View logs
```

### **Debug Commands:**
```bash
# Application health
curl -v http://localhost:5000/health

# Container logs
docker logs student-app-container

# Database connection test
python -c "import os; from app import connect_to_mongodb; print(connect_to_mongodb())"
```

## 📊 Monitoring & Maintenance

### **Health Monitoring:**
- **Endpoint**: `/health` returns system status
- **Database**: Connection status reporting
- **Secrets**: Configuration validation

### **Log Management:**
- **Application**: Structured logging with timestamps
- **Pipeline**: Build and deployment logs
- **Security**: Audit trails for secret access

### **Regular Maintenance:**
- **Dependencies**: Monthly security updates
- **Secrets**: Quarterly rotation
- **Backups**: Daily automated backups
- **Monitoring**: Performance metrics review

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Add tests** for new functionality
4. **Commit** changes: `git commit -m 'Add amazing feature'`
5. **Push** to branch: `git push origin feature/amazing-feature`
6. **Open** Pull Request

### **Contribution Guidelines:**
- Follow PEP 8 Python style guide
- Add unit tests for all new features
- Update documentation for changes
- Test both Jenkins and GitHub Actions pipelines

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- **Flask Team** - Web framework
- **MongoDB** - Database platform  
- **Jenkins Community** - CI/CD platform
- **GitHub** - Repository and Actions platform
- **Docker** - Containerization platform

## 📞 Support

For questions and support:
- **Email**: your-email@domain.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/student-management-cicd/issues)
- **Documentation**: [Project Wiki](https://github.com/yourusername/student-management-cicd/wiki)

---

⭐ **Star this repository** if it helped you with your CI/CD learning!

🐛 **Found a bug?** [Report it here](https://github.com/yourusername/student-management-cicd/issues)

💡 **Have suggestions?** [Start a discussion](https://github.com/yourusername/student-management-cicd/discussions)
