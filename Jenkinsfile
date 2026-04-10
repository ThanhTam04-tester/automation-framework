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
                // Cài đặt đủ thư viện cho test UI
                sh 'venv/bin/pip install pytest pytest-html selenium allure-pytest'
            }
        }

        stage('Run UI Tests') {
            steps {
                // Đã xóa '|| true' để Jenkins báo ĐỎ (FAIL) nếu test có lỗi.
                // Thêm '--clean-alluredir' để dọn dẹp báo cáo cũ của lần chạy trước
                sh 'venv/bin/pytest tests/ui/ --alluredir=reports/allure-results --clean-alluredir'
            }
        }

        stage('Run API Tests') {
            steps {
                sh 'venv/bin/pytest tests/api/ --alluredir=reports/allure-results || true'
            }
        }
    }
    
    post {
        always {
            // Khối always này sẽ luôn chạy để xuất báo cáo, bất kể bước UI Tests ở trên Xanh hay Đỏ
            allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
        }
    }
}