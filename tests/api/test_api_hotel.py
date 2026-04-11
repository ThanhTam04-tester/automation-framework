import pytest
import requests
import allure

BASE_URL = "http://host.docker.internal:5000" 

@allure.epic("API & Backend Testing")
@allure.feature("Backend Endpoints Validation")
class TestBackendAPI:

    @allure.title("API_01: Đăng nhập Admin qua Form Request")
    def test_api_admin_login(self):
        client = requests.Session()
        payload = {"email": "admin@gmail.com", "password": "123"}
        response = client.post(f"{BASE_URL}/login", data=payload, allow_redirects=False)
        with allure.step("Xác minh chuyển hướng đến trang dashboard"):
            assert response.status_code == 302
            assert "/admin/dashboard" in response.headers.get("Location", "")

    @allure.title("API_02: Kiểm tra bảo mật (Chặn truy cập Admin khi chưa login)")
    def test_api_security_admin_route(self):
        response = requests.get(f"{BASE_URL}/admin/dashboard", allow_redirects=False)
        with allure.step("Xác minh bị đẩy về trang đăng nhập"):
            assert response.status_code == 302
            assert "/login" in response.headers.get("Location", "")

    @allure.title("API_03: Đặt phòng thành công (Gửi đầy đủ thông tin & Ngày tháng)")
    def test_api_book_room_success(self):
        with allure.step("Setup: Đăng nhập Admin và Reset phòng số 1 về Trống"):
            client = requests.Session()
            client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
            client.post(f"{BASE_URL}/admin/rooms/reset/1")

        payload = {
            "room_id": 1, 
            "customer_name": "API Tester",
            "phone": "0999888777",
            "check_in": "2026-10-10",
            "check_out": "2026-10-15"
        }
        with allure.step("Gửi request POST /api/book dạng JSON"):
            response = requests.post(f"{BASE_URL}/api/book", json=payload)
            
        with allure.step("Kiểm tra phản hồi 201 Thành công"):
            assert response.status_code == 201
            assert "thành công" in response.json().get("message", "").lower()

    @allure.title("API_04: Đặt phòng thất bại (Phòng đang giữ/đã đặt)")
    def test_api_book_room_fail_already_booked(self):
        # Phòng 1 vừa được đặt ở API_03, nên giờ đặt lại sẽ lỗi
        payload = {
            "room_id": 1, 
            "customer_name": "Ghost User",
            "phone": "000",
            "check_in": "2026-11-01",
            "check_out": "2026-11-05"
        }
        response = requests.post(f"{BASE_URL}/api/book", json=payload)
        with allure.step("Xác minh API báo lỗi 400"):
            assert response.status_code == 400
            assert "đã có người đặt" in response.json().get("error", "").lower()

    @allure.title("API_05: Đặt phòng thất bại (Gửi ID phòng không tồn tại)")
    def test_api_book_room_fail_not_exist(self):
        payload = {"room_id": 99999, "customer_name": "Ghost", "phone": "000", "check_in": "2026-01-01", "check_out": "2026-01-02"}
        response = requests.post(f"{BASE_URL}/api/book", json=payload)
        with allure.step("Xác minh API chặn lại"):
            assert response.status_code == 400

    @allure.title("API_06: Admin duyệt đơn đặt phòng")
    def test_api_admin_approve_booking(self):
        client = requests.Session()
        client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
        
        with allure.step("Admin gửi request duyệt đơn số 1"):
            response = client.post(f"{BASE_URL}/admin/bookings/action/1", data={"action": "approve"}, allow_redirects=False)
            assert response.status_code == 302 # redirect về dashboard

    @allure.title("API_07: Admin cập nhật trạng thái phòng")
    def test_api_admin_update_room_status(self):
        client = requests.Session()
        client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
        
        with allure.step("Đổi trạng thái phòng 2 thành Bảo trì"):
            response = client.post(f"{BASE_URL}/admin/rooms/status/2", data={"status": "Bảo trì"}, allow_redirects=False)
            assert response.status_code == 302

    @allure.title("API_08: Admin Reset phòng về Trống")
    def test_api_admin_reset_room(self):
        client = requests.Session()
        client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
        
        with allure.step("Reset phòng số 2"):
            response = client.post(f"{BASE_URL}/admin/rooms/reset/2", allow_redirects=False)
            assert response.status_code == 302

    @allure.title("API_09: Admin xóa tài khoản người dùng")
    def test_api_admin_delete_user(self):
        client = requests.Session()
        client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
        
        with allure.step("Giả lập xóa user ID 9999 (có thể không tồn tại nhưng endpoint phải phản hồi đúng)"):
            response = client.post(f"{BASE_URL}/admin/users/delete/9999", allow_redirects=False)
            assert response.status_code == 302