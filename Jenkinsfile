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
                // Cài đặt đủ thư viện cho test UI và xuất báo cáo Allure
                sh 'venv/bin/pip install pytest pytest-html selenium allure-pytest'
            }
        }

        // ĐÃ XÓA KHỐI "Run API Tests" GÂY LỖI Ở ĐÂY

        stage('Run UI Tests') {
            steps {
                // Chỉ chạy test UI và tự động xuất dữ liệu báo cáo Allure
                sh 'venv/bin/pytest -m ui'
            }
        }
    }
    
    post {
        always {
            // Lệnh này yêu cầu Jenkins đọc dữ liệu và vẽ ra biểu đồ Allure tuyệt đẹp
            allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
        }
    }
}