pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install & Setup') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install --upgrade pip'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Tests & Generate Report') {
            steps {
                // Chạy test và xuất file report html
                bat 'venv\\Scripts\\pytest -v --html=report.html --self-contained-html'
            }
        }
    }
    
    // Khối này tự động lưu lại file báo cáo sau khi chạy xong
    post {
        always {
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
        }
    }
}