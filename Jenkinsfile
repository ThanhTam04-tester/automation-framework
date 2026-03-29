pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                // Lệnh này giúp Jenkins tự động lấy đúng repo và mật khẩu bạn đã cấu hình trên web
                checkout scm
            }
        }

        stage('Install Python') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install --upgrade pip'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
                bat 'venv\\Scripts\\pip install pytest pytest-html selenium'
            }
        }

        stage('Run API Tests') {
            steps {
                bat 'venv\\Scripts\\pytest -m api -v'
            }
        }

        stage('Run UI Tests') {
            steps {
                bat 'venv\\Scripts\\pytest -m ui -v'
            }
        }

        stage('Report') {
            steps {
                bat 'venv\\Scripts\\pytest --html=report.html'
            }
        }
    }
}