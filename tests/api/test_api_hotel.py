import pytest
import requests
import allure

BASE_URL = "http://host.docker.internal:5000" 

@allure.epic("API & Backend Testing")
@allure.feature("Backend Endpoints Validation")
class TestBackendAPI:

    @allure.title("API_01: Đặt phòng thành công (API trả về JSON)")
    def test_api_book_room_success(self):
        with allure.step("Setup: Đăng nhập Admin và ép Reset phòng số 3 về Trống"):
            client = requests.Session()
            client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
            # Ép trạng thái phòng 3 thành Trống
            client.post(f"{BASE_URL}/admin/rooms/status/3", data={"status": "Trống"})

        payload = {
            "room_id": 3, 
            "customer_name": "API Tester",
            "phone": "0999888777"
        }
        
        with allure.step("Gửi request POST /api/book dạng JSON"):
            response = requests.post(f"{BASE_URL}/api/book", json=payload)
            
        with allure.step("Kiểm tra phản hồi 201 Thành công"):
            assert response.status_code == 201
            assert "thành công" in response.json().get("message", "").lower()

    @allure.title("API_02: Đặt phòng thất bại (Gửi ID phòng không tồn tại)")
    def test_api_book_room_fail_not_exist(self):
        payload = {"room_id": 9999, "customer_name": "Ghost User", "phone": "000"}
        response = requests.post(f"{BASE_URL}/api/book", json=payload)
        
        with allure.step("Xác minh API chặn lại và báo lỗi 400"):
            assert response.status_code == 400
            assert "không tồn tại" in response.json().get("error", "").lower()

    @allure.title("API_03: Đăng nhập Admin qua Form Request")
    def test_backend_admin_login(self):
        client = requests.Session()
        payload = {"email": "admin@gmail.com", "password": "123"}
        response = client.post(f"{BASE_URL}/login", data=payload, allow_redirects=False)
        assert response.status_code == 302
        assert "/admin/dashboard" in response.headers.get("Location", "")

    @allure.title("API_04: Kiểm tra bảo mật (Chặn truy cập Admin khi chưa login)")
    def test_backend_security_admin_route(self):
        response = requests.get(f"{BASE_URL}/admin/dashboard", allow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers.get("Location", "")