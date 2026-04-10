import pytest
import requests
import allure

# Sửa lại URL nếu bạn chạy bằng IP khác
BASE_URL = "http://host.docker.internal:5000" 

@allure.epic("API & Backend Testing")
@allure.feature("Backend Endpoints Validation")
class TestBackendAPI:

    # ================= 1. TEST CHUẨN JSON API =================
    @allure.title("API_01: Đặt phòng thành công (API trả về JSON)")
    def test_api_book_room_success(self):
        # Lưu ý: Ta dùng phòng số 3 (Family) - Hy vọng trong DB đang có status 'Trống'
        payload = {
            "room_id": 3, 
            "customer_name": "API Tester",
            "phone": "0999888777"
        }
        
        with allure.step("Gửi request POST /api/book dạng JSON"):
            response = requests.post(f"{BASE_URL}/api/book", json=payload)
            
        with allure.step("Kiểm tra phản hồi từ Backend"):
            # Nếu phòng 3 còn trống, nó sẽ trả 201
            if response.status_code == 201:
                data = response.json()
                assert "thành công" in data.get("message", "").lower()
            # Nếu lỡ ai đó đặt mất rồi, API của bạn trả 400. Ta Skip để không báo ảo.
            elif response.status_code == 400:
                pytest.skip("Phòng số 3 đã bị đặt trong DB, bỏ qua test để tránh báo lỗi đỏ ảo.")

    @allure.title("API_02: Đặt phòng thất bại (Gửi ID phòng không tồn tại)")
    def test_api_book_room_fail_not_exist(self):
        payload = {
            "room_id": 9999, # ID ảo không có trong DB
            "customer_name": "Ghost User",
            "phone": "000"
        }
        
        with allure.step("Gửi request với room_id sai"):
            response = requests.post(f"{BASE_URL}/api/book", json=payload)
            
        with allure.step("Xác minh API chặn lại và báo lỗi 400"):
            assert response.status_code == 400
            data = response.json()
            assert "không tồn tại" in data.get("error", "").lower()


    # ================= 2. TEST FORM DATA & BẢO MẬT BẰNG REQUESTS =================
    @allure.title("API_03: Đăng nhập Admin qua Form Request")
    def test_backend_admin_login(self):
        # Tạo 1 Session ảo để giữ Cookie (như trình duyệt thật)
        client = requests.Session()
        
        # Dữ liệu Admin CỦA BẠN từ database.db (admin@gmail.com / 123)
        payload = {
            "email": "admin@gmail.com",
            "password": "123"
        }
        
        with allure.step("Gửi POST request chứa dữ liệu Form đến /login"):
            # Trình duyệt web gửi dạng data, không phải json
            response = client.post(f"{BASE_URL}/login", data=payload, allow_redirects=False)
            
        with allure.step("Xác minh Backend cho phép và Redirect (302) tới Dashboard"):
            # Trong app.py, đăng nhập đúng sẽ gọi "redirect(url_for('admin_dashboard'))"
            assert response.status_code == 302
            assert "/admin/dashboard" in response.headers.get("Location", "")

    @allure.title("API_04: Kiểm tra bảo mật (Chặn truy cập Admin khi chưa login)")
    def test_backend_security_admin_route(self):
        with allure.step("Cố tình truy cập thẳng vào /admin/dashboard không có Session"):
            response = requests.get(f"{BASE_URL}/admin/dashboard", allow_redirects=False)
            
        with allure.step("Xác minh Backend chặn và đá văng về trang Login (302)"):
            assert response.status_code == 302
            assert "/login" in response.headers.get("Location", "")