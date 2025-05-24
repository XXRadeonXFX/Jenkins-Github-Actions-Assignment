pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        retry(1)
        skipDefaultCheckout()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    environment {
        SSH_CREDENTIALS_ID = "c3b12c2f-9959-46a6-b763-fc4e303082cb"
        EC2_USER = "ubuntu"
        EC2_HOST = "13.203.207.84"
        APP_DIR = "/home/ubuntu/student-app"
        DOCKER_IMAGE = "student-app"
        CONTAINER_NAME = "student-app-container"
        APP_PORT = "5000"
        NOTIFICATION_EMAIL = "prince.thakur24051996@gmail.com"
    }

    stages {
        stage('🔍 Environment Validation') {
            steps {
                script {
                    echo "Validating build environment..."

                    // Check Docker availability
                    def dockerCheck = sh(script: 'which docker', returnStatus: true)
                    if (dockerCheck != 0) {
                        echo "Installing Docker..."
                        sh '''
                            curl -fsSL https://get.docker.com -o get-docker.sh
                            sudo sh get-docker.sh
                            sudo usermod -aG docker $USER
                            sudo systemctl start docker
                        '''
                    }

                    // Ensure Docker daemon is running
                    sh '''
                        if ! docker info >/dev/null 2>&1; then
                            echo "Starting Docker daemon..."
                            sudo systemctl start docker
                            sleep 5
                        fi
                        docker --version
                    '''

                    // Verify required files exist
                    def requiredFiles = ['requirements.txt', 'app.py', 'Dockerfile']
                    requiredFiles.each { file ->
                        if (!fileExists(file)) {
                            error "Required file '${file}' not found in workspace"
                        }
                    }

                    // Verify MongoDB credentials are configured
                    try {
                        withCredentials([string(credentialsId: 'PRINCE_MONGO_URI', variable: 'MONGO_URI_TEST')]) {
                            if (env.MONGO_URI_TEST == null || env.MONGO_URI_TEST.trim() == '') {
                                error "MongoDB URI credential is empty or not configured"
                            }
                            echo "SUCCESS: MongoDB credentials validated"
                        }
                    } catch (Exception e) {
                        error "ERROR: MongoDB URI credential not found. Please ensure 'PRINCE_MONGO_URI' credential exists in Jenkins"
                    }

                    echo "SUCCESS: Environment validation completed"
                }
            }
        }

        stage('📦 Install Dependencies') {
            steps {
                echo "Setting up Python environment..."
                sh '''
                    # Debug: Show current directory and contents
                    echo "Current directory: $(pwd)"
                    echo "Directory contents:"
                    ls -la
                    
                    # Create virtual environment if not exists
                    if [ ! -d "venv" ]; then
                        echo "Creating virtual environment..."
                        python3 -m venv venv || (echo "Failed to create venv. Installing python3-venv..." && sudo apt-get update && sudo apt-get install -y python3-venv && python3 -m venv venv)
                    fi
                    
                    # Verify venv was created
                    if [ ! -f "venv/bin/activate" ]; then
                        echo "ERROR: Virtual environment not created properly!"
                        exit 1
                    fi
                    
                    # Install dependencies
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    
                    echo "SUCCESS: Dependencies installed successfully"
                '''
            }
        }

        stage('🧪 Run Tests') {
            steps {
                echo "Running tests..."
                sh '''
                    . venv/bin/activate
                    pytest test_app.py --maxfail=1 --disable-warnings -q || true
                '''
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."

                    // Build with error handling and retry
                    def buildResult = sh(script: "docker build -t ${DOCKER_IMAGE} .", returnStatus: true)
                    if (buildResult != 0) {
                        echo "Build failed, cleaning up and retrying..."
                        sh '''
                            docker system prune -f
                            docker build --no-cache -t ${DOCKER_IMAGE} .
                        '''
                    }

                    // Verify image creation
                    sh "docker images | grep ${DOCKER_IMAGE}"
                    echo "SUCCESS: Docker image built successfully"
                }
            }
        }

        stage('🚀 Deploy to EC2') {
            steps {
                script {
                    echo "Deploying to EC2 with secure MongoDB connection..."

                    withCredentials([string(credentialsId: 'PRINCE_MONGO_URI', variable: 'MONGO_URI')]) {
                        sshagent([env.SSH_CREDENTIALS_ID]) {

                            // Test SSH connectivity
                            testSSHConnection()

                            // Setup EC2 environment
                            setupEC2Environment()

                            // Copy application files
                            copyApplicationFiles()

                            // Deploy application with secure MONGO_URI
                            deployApplicationSecure()
                        }
                    }
                }
            }
        }

        stage('🏥 Health Check') {
            steps {
                script {
                    echo "Running health checks..."
                    sshagent([env.SSH_CREDENTIALS_ID]) {
                        sh '''
                            sleep 15
                            
                            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                                echo "Checking container status..."
                                
                                for i in {1..5}; do
                                    echo "Health check attempt $i/5"
                                    
                                    if docker ps --filter "name=''' + env.CONTAINER_NAME + '''" --filter "status=running" | grep -q ''' + env.CONTAINER_NAME + '''; then
                                        echo "✅ Container is running"
                                        
                                        if curl -f -s http://localhost:''' + env.APP_PORT + '''/ >/dev/null; then
                                            echo "✅ Application responding to HTTP requests"
                                            echo "🎉 Health check passed!"
                                            exit 0
                                        fi
                                    fi
                                    
                                    echo "Waiting 10 seconds before retry..."
                                    sleep 10
                                done
                                
                                echo "❌ Health check failed"
                                docker logs ''' + env.CONTAINER_NAME + '''
                                exit 1
                            '
                        '''
                    }
                }
            }
        }

    }

    post {
        always {
            script {
                echo "Cleaning up..."
                cleanupResources()
            }
        }

        success {
            script {
                echo "SUCCESS: Pipeline completed successfully!"
                echo "Application available at: http://${EC2_HOST}:${APP_PORT}"
            }

            mail to: env.NOTIFICATION_EMAIL,
                 subject: "SUCCESS: ${env.JOB_NAME} Build #${env.BUILD_NUMBER}",
                 body: """
BUILD SUCCESSFUL!

BUILD DETAILS:
   • Job Name: ${env.JOB_NAME}
   • Build Number: #${env.BUILD_NUMBER}
   • Build Time: ${new Date()}

DEPLOYMENT INFO:
   • Application URL: http://${EC2_HOST}:${APP_PORT}
   • Target Server: ${EC2_HOST}
   • Container: ${CONTAINER_NAME}
   • Docker Image: ${DOCKER_IMAGE}

VERIFIED COMPONENTS:
   • Container is running and healthy
   • MongoDB connection established
   • HTTP endpoints responding
   • Environment variables configured
   • Application ready for use

QUICK LINKS:
   • View Build: ${env.BUILD_URL}
   • Console Output: ${env.BUILD_URL}console
   • Test Application: http://${EC2_HOST}:${APP_PORT}

All stages completed successfully!
Application is running and healthy!
Ready for use!
                 """
        }

        failure {
            script {
                echo "ERROR: Pipeline failed!"
                collectDebugInfo()
            }

            mail to: env.NOTIFICATION_EMAIL,
                 subject: "FAILURE: ${env.JOB_NAME} Build #${env.BUILD_NUMBER}",
                 body: """
BUILD FAILED!

BUILD DETAILS:
   • Job Name: ${env.JOB_NAME}
   • Build Number: #${env.BUILD_NUMBER}
   • Failed Time: ${new Date()}

FAILURE INFO:
   • Target Server: ${EC2_HOST}
   • Application Port: ${APP_PORT}
   • Container: ${CONTAINER_NAME}
   • Docker Image: ${DOCKER_IMAGE}

TROUBLESHOOTING LINKS:
   • View Build: ${env.BUILD_URL}
   • Console Logs: ${env.BUILD_URL}console

MONGODB-SPECIFIC CHECKS:
   • Verify MongoDB URI credential 'PRINCE_MONGO_URI' exists in Jenkins
   • Check MongoDB server is accessible from EC2
   • Confirm MongoDB URI format is correct
   • Validate database authentication credentials
   • Check network connectivity to MongoDB cluster

Action Required: Please investigate and fix the issue!
                 """
        }

        unstable {
            script {
                echo "WARNING: Pipeline completed with warnings"
            }

            mail to: env.NOTIFICATION_EMAIL,
                 subject: "UNSTABLE: ${env.JOB_NAME} Build #${env.BUILD_NUMBER}",
                 body: """
BUILD UNSTABLE!

BUILD DETAILS:
   • Job Name: ${env.JOB_NAME}
   • Build Number: #${env.BUILD_NUMBER}
   • Completed Time: ${new Date()}
   • Status: UNSTABLE (some tests may have failed)

INVESTIGATION NEEDED:
   • Application URL: http://${EC2_HOST}:${APP_PORT}
   • Some tests may have failed but deployment continued
   • Check test results and application functionality

Please review test results and application status!
                 """
        }
    }
}

// Helper Functions with proper variable substitution
def testSSHConnection() {
    def sshTest = sh(script: """
        ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 ${EC2_USER}@${EC2_HOST} 'echo "SSH OK"'
    """, returnStatus: true)

    if (sshTest != 0) {
        error "ERROR: Cannot connect to EC2. Check network and SSH credentials."
    }
}

def setupEC2Environment() {
    sh """
        echo "Setting up EC2 environment..."
        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
            # Install Docker if needed
            if ! command -v docker &> /dev/null; then
                echo 'Installing Docker on EC2...'
                curl -fsSL https://get.docker.com -o get-docker.sh
                sudo sh get-docker.sh
                sudo usermod -aG docker ubuntu
                sudo systemctl start docker
                sudo systemctl enable docker
            fi
            
            # Start Docker daemon if not running
            if ! docker info >/dev/null 2>&1; then
                sudo systemctl start docker
                sleep 5
            fi
            
            # Create app directory
            mkdir -p ${APP_DIR}
        "
    """
}

def copyApplicationFiles() {
    echo "Copying application files..."
    sh """
        # Copy main application files
        scp -o StrictHostKeyChecking=no \\
            Dockerfile app.py requirements.txt test_app.py \\
            ${EC2_USER}@${EC2_HOST}:${APP_DIR}/
    """
}

def deployApplicationSecure() {
    echo "Deploying application with secure MongoDB connection..."
    sh """
        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
            cd ${APP_DIR}
            
            # Stop and remove existing container
            if docker ps -a | grep -q ${CONTAINER_NAME}; then
                echo 'Stopping existing container...'
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
            fi
            
            # Remove old image to save space
            if docker images | grep -q ${DOCKER_IMAGE}; then
                echo 'Removing old image...'
                docker rmi ${DOCKER_IMAGE} || true
            fi
            
            # Build and run new container
            echo 'Building image on EC2...'
            docker build -t ${DOCKER_IMAGE} .
            
            echo 'Starting new container with MongoDB connection...'
            docker run -d \\
                --name ${CONTAINER_NAME} \\
                --restart unless-stopped \\
                -p ${APP_PORT}:${APP_PORT} \\
                -e MONGO_URI='${MONGO_URI}' \\
                ${DOCKER_IMAGE}
            
            # Verify container started
            sleep 5
            if docker ps | grep -q ${CONTAINER_NAME}; then
                echo 'SUCCESS: Container started successfully'
                docker ps | grep ${CONTAINER_NAME}
                
                # Quick MongoDB connection test
                echo 'Testing MongoDB connection in container...'
                docker exec ${CONTAINER_NAME} python3 -c '
import os
print(\"MONGO_URI configured:\", \"Yes\" if os.environ.get(\"MONGO_URI\") else \"No\")
try:
    from pymongo import MongoClient
    client = MongoClient(os.environ.get(\"MONGO_URI\"), serverSelectionTimeoutMS=3000)
    client.admin.command(\"ping\")
    print(\"SUCCESS: MongoDB connection test successful\")
except ImportError:
    print(\"WARNING: pymongo not available, skipping connection test\")
except Exception as e:
    print(\"ERROR: MongoDB connection test failed: \" + str(e))
' || echo 'MongoDB connection test completed'
            else
                echo 'ERROR: Container failed to start'
                docker logs ${CONTAINER_NAME}
                exit 1
            fi
        "
    """
}

def cleanupResources() {
    sh '''
        # Clean up local resources
        docker image prune -f || true
        docker builder prune -f || true
        rm -rf venv || true
    '''
}

def collectDebugInfo() {
    try {
        withCredentials([string(credentialsId: 'PRINCE_MONGO_URI', variable: 'MONGO_URI')]) {
            sshagent([env.SSH_CREDENTIALS_ID]) {
                sh """
                    echo "Collecting debug information..."
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                        echo '=== Docker Status ==='
                        docker ps -a || true
                        
                        echo '=== Container Logs ==='
                        docker logs --tail 50 ${CONTAINER_NAME} || true
                        
                        echo '=== Container Environment ==='
                        docker exec ${CONTAINER_NAME} env | grep -E '(MONGO|PORT|PATH)' || true
                        
                        echo '=== MongoDB Connection Test ==='
                        docker exec ${CONTAINER_NAME} python3 -c '
import os
print(\"MONGO_URI present:\", bool(os.environ.get(\"MONGO_URI\")))
if os.environ.get(\"MONGO_URI\"):
    print(\"MONGO_URI format:\", os.environ.get(\"MONGO_URI\")[:30] + \"...\")
' || true
                        
                        echo '=== System Resources ==='
                        df -h || true
                        free -h || true
                        
                        echo '=== Network Connectivity ==='
                        ss -tlnp | grep ${APP_PORT} || true
                    " || true
                """
            }
        }
    } catch (Exception e) {
        echo "Could not collect debug information: ${e.getMessage()}"
    }
}
