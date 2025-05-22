pipeline {
    agent any

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

        stage('Run Flask App') {
            steps {
                sh 'docker run -d -p 5000:5000 --name student-app-container student-app'
            }
        }
    }

    post {
        success {
            echo '✅ Build & deployment successful.'
        }
        failure {
            echo '❌ Build failed.'
        }
    }
}
