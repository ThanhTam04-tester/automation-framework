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
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install --upgrade pip'
                sh 'venv/bin/pip install -r requirements.txt'
                sh 'venv/bin/pip install pytest pytest-html selenium allure-pytest requests'
            }
        }

        stage('Run API Tests') {
            steps {
                // Thêm '|| true' để nếu test API fail thì vẫn chạy tiếp UI
                sh 'venv/bin/pytest tests/api/ --alluredir=reports/allure-results || true'
            }
        }

        stage('Run UI Tests') {
            steps {
                // Thêm '|| true' để Jenkins không đánh dấu Build Failure ngay lập tức
                sh 'venv/bin/pytest tests/ui/ --alluredir=reports/allure-results || true'
            }
        }
    }
    
    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
        }
    }
}