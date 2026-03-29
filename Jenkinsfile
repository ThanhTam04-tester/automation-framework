pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Python') {
            steps {
                // Trên Linux dùng lệnh 'sh' thay vì 'bat', và đường dẫn là 'venv/bin/' thay vì 'venv\\Scripts\\'
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install --upgrade pip'
                sh 'venv/bin/pip install -r requirements.txt'
                sh 'venv/bin/pip install pytest pytest-html selenium'
            }
        }

        stage('Run API Tests') {
            steps {
                sh 'venv/bin/pytest -m api -v'
            }
        }

        stage('Run UI Tests') {
            steps {
                sh 'venv/bin/pytest -m ui -v'
            }
        }

        stage('Report') {
            steps {
                sh 'venv/bin/pytest --html=report.html --self-contained-html'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
        }
    }
}