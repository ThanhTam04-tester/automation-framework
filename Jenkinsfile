pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/ThanhTam04-tester/automation-framework.git'
            }
        }

        stage('Install Python') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run API Tests') {
            steps {
                bat 'venv\\Scripts\\pytest -m api'
            }
        }

        stage('Run UI Tests') {
            steps {
                bat 'venv\\Scripts\\pytest -m ui'
            }
        }

        stage('Report') {
            steps {
                bat 'venv\\Scripts\\pytest --html=report.html'
            }
        }
    }
}