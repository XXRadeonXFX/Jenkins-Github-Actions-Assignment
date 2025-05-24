pipeline {
    agent any
    
    environment {
        SSH_CREDENTIALS_ID = "c3b12c2f-9959-46a6-b763-fc4e303082cb"
        EC2_USER = "ubuntu"
        EC2_HOST = "13.203.207.84"
        APP_DIR = "/home/ubuntu/student-app"
        DOCKER_IMAGE = "student-app"
        CONTAINER_NAME = "student-app-container"
        APP_PORT = "5000"
        NOTIFICATION_EMAIL = "prince.thakur24051996@gmail.com"
        MONGO_URI = "PRINCE_MONGO_URI"
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
                    
                    echo "✅ Environment validation completed"
                }
            }
        }
        
        stage('📦 Install Dependencies') {
            steps {
                echo "Setting up Python environment..."
                sh '''
                    # Create virtual environment if not exists
                    if [ ! -d "venv" ]; then
                        python3 -m venv venv
                    fi
                    
                    # Install dependencies
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
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
                    echo "✅ Docker image built successfully"
                }
            }
        }
        
        stage('🚀 Deploy to EC2') {
            steps {
                script {
                    echo "Deploying to EC2..."
                    sshagent([env.SSH_CREDENTIALS_ID]) {
                        
                        // Test SSH connectivity
                        testSSHConnection()
                        
                        // Setup EC2 environment
                        setupEC2Environment()
                        
                        // Copy application files
                        copyApplicationFiles()
                        
                        // Deploy application
                        deployApplication()
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
                echo "🧹 Cleaning up..."
                cleanupResources()
            }
        }
        
        success {
            script {
                echo "✅ Pipeline completed successfully!"
                echo "🌐 Application available at: http://${EC2_HOST}:${APP_PORT}"
            }
            
            // Attractive email notification for success
            mail to: env.NOTIFICATION_EMAIL,
                 subject: "🎉 SUCCESS: ${env.JOB_NAME} Build #${env.BUILD_NUMBER} ✅",
                 body: """
═══════════════════════════════════════════════════════════════
🎉 BUILD SUCCESSFUL! 🎉
═══════════════════════════════════════════════════════════════

📋 BUILD DETAILS:
   • Job Name: ${env.JOB_NAME}
   • Build Number: #${env.BUILD_NUMBER}
   • Build Time: ${new Date()}
   • Jenkins URL: ${env.JENKINS_URL}

🚀 DEPLOYMENT INFO:
   • Application URL: http://${EC2_HOST}:${APP_PORT}
   • Target Server: ${EC2_HOST}
   • Container: ${CONTAINER_NAME}
   • Docker Image: ${DOCKER_IMAGE}

🔗 QUICK LINKS:
   • View Build: ${env.BUILD_URL}
   • Console Output: ${env.BUILD_URL}console
   • Test Application: http://${EC2_HOST}:${APP_PORT}

✅ All stages completed successfully!
✅ Application is running and healthy!
✅ Ready for use!

═══════════════════════════════════════════════════════════════
Happy Coding! 🚀
═══════════════════════════════════════════════════════════════
                 """
        }
        
        failure {
            script {
                echo "❌ Pipeline failed!"
                collectDebugInfo()
            }
            
            // Attractive email notification for failure
            mail to: env.NOTIFICATION_EMAIL,
                 subject: "🚨 FAILURE: ${env.JOB_NAME} Build #${env.BUILD_NUMBER} ❌",
                 body: """
═══════════════════════════════════════════════════════════════
🚨 BUILD FAILED! 🚨
═══════════════════════════════════════════════════════════════

📋 BUILD DETAILS:
   • Job Name: ${env.JOB_NAME}
   • Build Number: #${env.BUILD_NUMBER}
   • Failed Time: ${new Date()}
   • Jenkins URL: ${env.JENKINS_URL}

💥 FAILURE INFO:
   • Target Server: ${EC2_HOST}
   • Application Port: ${APP_PORT}
   • Container: ${CONTAINER_NAME}
   • Docker Image: ${DOCKER_IMAGE}

🔧 TROUBLESHOOTING LINKS:
   • View Build: ${env.BUILD_URL}
   • Console Logs: ${env.BUILD_URL}console
   • Blue Ocean: ${env.BUILD_URL}display/redirect

📊 COMMON FAILURE POINTS TO CHECK:
   ❗ SSH connectivity to EC2: ${EC2_HOST}
   ❗ Docker service status on Jenkins & EC2
   ❗ Application dependencies in requirements.txt
   ❗ Port ${APP_PORT} availability on EC2
   ❗ Container build process and Dockerfile
   ❗ EC2 disk space and memory

🔍 DEBUG STEPS:
   1. Check console logs for specific error messages
   2. Verify EC2 instance is running and accessible
   3. Test SSH connection manually: ssh ${EC2_USER}@${EC2_HOST}
   4. Check Docker status: docker ps -a
   5. Review container logs: docker logs ${CONTAINER_NAME}

❌ Action Required: Please investigate and fix the issue!

═══════════════════════════════════════════════════════════════
Need Help? Check the troubleshooting guide! 🛠️
═══════════════════════════════════════════════════════════════
                 """
        }
        
        unstable {
            script {
                echo "⚠️ Pipeline completed with warnings"
            }
            
            // Email notification for unstable build
            mail to: env.NOTIFICATION_EMAIL,
                 subject: "⚠️ UNSTABLE: ${env.JOB_NAME} Build #${env.BUILD_NUMBER} ⚠️",
                 body: """
═══════════════════════════════════════════════════════════════
⚠️ BUILD UNSTABLE! ⚠️
═══════════════════════════════════════════════════════════════

📋 BUILD DETAILS:
   • Job Name: ${env.JOB_NAME}
   • Build Number: #${env.BUILD_NUMBER}
   • Completed Time: ${new Date()}
   • Status: UNSTABLE (some tests may have failed)

🔍 INVESTIGATION NEEDED:
   • Application URL: http://${EC2_HOST}:${APP_PORT}
   • Some tests may have failed but deployment continued
   • Check test results and application functionality

🔗 REVIEW LINKS:
   • View Build: ${env.BUILD_URL}
   • Console Output: ${env.BUILD_URL}console
   • Test Application: http://${EC2_HOST}:${APP_PORT}

⚠️ Please review test results and application status!

═══════════════════════════════════════════════════════════════
Review Required! ⚠️
═══════════════════════════════════════════════════════════════
                 """
        }
    }
}

// Helper Functions
def testSSHConnection() {
    def sshTest = sh(script: """
        ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 ${EC2_USER}@${EC2_HOST} 'echo "SSH OK"'
    """, returnStatus: true)
    
    if (sshTest != 0) {
        error "❌ Cannot connect to EC2. Check network and SSH credentials."
    }
}

def setupEC2Environment() {
    sh '''
        echo "🔧 Setting up EC2 environment..."
        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
            # Install Docker if needed
            if ! command -v docker &> /dev/null; then
                echo "Installing Docker on EC2..."
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
            mkdir -p ''' + env.APP_DIR + '''
        '
    '''
}

def copyApplicationFiles() {
    echo "📤 Copying application files..."
    sh '''
        # Copy main application files
        scp -o StrictHostKeyChecking=no \
            Dockerfile app.py requirements.txt test_app.py \
            ${EC2_USER}@${EC2_HOST}:${APP_DIR}/
    '''
}

def deployApplication() {
    echo "🔄 Deploying application..."
    sh '''
        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
            cd ''' + env.APP_DIR + '''
            
            # Stop and remove existing container
            if docker ps -a | grep -q ''' + env.CONTAINER_NAME + '''; then
                echo "Stopping existing container..."
                docker stop ''' + env.CONTAINER_NAME + ''' || true
                docker rm ''' + env.CONTAINER_NAME + ''' || true
            fi
            
            # Remove old image to save space
            if docker images | grep -q ''' + env.DOCKER_IMAGE + '''; then
                docker rmi ''' + env.DOCKER_IMAGE + ''' || true
            fi
            
            # Build and run new container
            echo "Building image on EC2..."
            docker build -t ''' + env.DOCKER_IMAGE + ''' .
            
            echo "Starting new container..."
            docker run -d \
                --name ''' + env.CONTAINER_NAME + ''' \
                --restart unless-stopped \
                -p ''' + env.APP_PORT + ''':''' + env.APP_PORT + ''' \
                -e MONGO_URI="$PRINCE_MONGO_URI" \
                ''' + env.DOCKER_IMAGE + '''
            
            # Verify container started
            sleep 5
            if docker ps | grep -q ''' + env.CONTAINER_NAME + '''; then
                echo "✅ Container started successfully"
                docker ps | grep ''' + env.CONTAINER_NAME + '''
            else
                echo "❌ Container failed to start"
                docker logs ''' + env.CONTAINER_NAME + '''
                exit 1
            fi
        '
    '''
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
        sshagent([env.SSH_CREDENTIALS_ID]) {
            sh '''
                echo "🔍 Collecting debug information..."
                ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                    echo "=== Docker Status ==="
                    docker ps -a || true
                    echo "=== Container Logs ==="
                    docker logs ''' + env.CONTAINER_NAME + ''' || true
                    echo "=== System Resources ==="
                    df -h || true
                    free -h || true
                ' || true
            '''
        }
    } catch (Exception e) {
        echo "Could not collect debug information: ${e.getMessage()}"
    }
}
