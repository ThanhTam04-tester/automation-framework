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
                // Đảm bảo cài thêm thư viện requests cho API
                sh 'venv/bin/pip install pytest pytest-html selenium allure-pytest requests'
            }
        }

        stage('Run All Tests (UI & API)') {
            steps {
                // Trỏ thẳng vào thư mục 'tests/' để Pytest tự gom cả UI và API chạy cùng 1 lúc
                sh 'venv/bin/pytest tests/ --alluredir=reports/allure-results --clean-alluredir'
            }
        }
    }
    
    post {
        always {
            script {
                // Sửa lại path thành 'reports/allure-results' cho khớp với lệnh pytest bên trên
                allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
            }
        }
    }
}
