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

       stage('Run Automation Tests') {
            steps {
                // =========================================================================
                 // 🟢 KỊCH BẢN 1: CHỈ TEST ĐỒ ÁN KHÁCH SẠN (UI & API)
                // Dùng khoảng trắng để nối 2 thư mục: tests/ui/ và tests/api/
                // =========================================================================
                sh 'venv/bin/pytest tests/ui/ tests/api/ --alluredir=reports/allure-results --clean-alluredir'
  
                // =========================================================================
                // 🔵 KỊCH BẢN 2: CHỈ TEST GOOGLE SEARCH
                // Bỏ dấu // ở dòng dưới, và thêm // vào dòng Kịch bản 1 ở trên để đổi dự án
                // =========================================================================
<<<<<<< HEAD
                // sh 'venv/bin/pytest tests/google/ --alluredir=reports/allure-results --clean-alluredir'
=======
                 sh 'venv/bin/pytest tests/google/ --alluredir=reports/allure-results --clean-alluredir'
>>>>>>> dc01a064869d263c66baf246a1e97c0796f6e3f7
            }
        }
    }
    
   post {
        always {
            script {
                // Thêm commandline: 'Allure' (Phải khớp chính xác viết hoa/thường với ô Name trong phần Tools)
                allure commandline: 'Allure', includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
            }
        }
    }
}
 