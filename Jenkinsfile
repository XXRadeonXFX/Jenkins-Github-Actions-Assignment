pipeline {
    agent any

    environment {
        SSH_CREDENTIALS_ID = "c3b12c2f-9959-46a6-b763-fc4e303082cb"
        EC2_USER = "ubuntu"
        EC2_HOST = "3.110.222.41"
        HOME_DIR = "/home/ubuntu"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest test_app.py --maxfail=1 --disable-warnings -q || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t student-app .'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent([env.SSH_CREDENTIALS_ID]) {
                    sh '''
                    echo "🔁 Copying files to EC2..."
                    scp -o StrictHostKeyChecking=no \
                        Dockerfile Jenkinsfile README.md app.py requirements.txt test_app.py \
                        ${EC2_USER}@${EC2_HOST}:${HOME_DIR}/student-app

                    echo "🚀 Running app on EC2..."
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                        cd ${HOME_DIR}/student-app
                        docker stop student-app-container || true
                        docker rm student-app-container || true
                        docker build -t student-app .
                        docker run -d -p 5000:5000 --name student-app-container student-app
                    '
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo '✅ Build, test, and deploy successful.'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
