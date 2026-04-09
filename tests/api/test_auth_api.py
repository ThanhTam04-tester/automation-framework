import pytest
import allure

@allure.epic("API Testing")
@allure.feature("Authentication API")
@allure.title("Test API Đăng nhập thành công")
def test_api_login_success(api_client):
    payload = {
        "username": "admin",
        "password": "123" # Dữ liệu đúng
    }
    
    with allure.step(f"Gửi POST request đến API login với dữ liệu: {payload}"):
        # Giả sử hàm post của api_client trả về response
        response = api_client.post("/api/login", json=payload)
        
    with allure.step(f"Xác minh Status Code trả về là 200. Thực tế: {response.status_code}"):
        assert response.status_code == 200, f"Lỗi: Status code = {response.status_code}"