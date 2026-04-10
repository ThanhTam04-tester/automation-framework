import pytest
import requests
import allure

# Đọc URL từ file config, ở đây tôi viết thẳng để bạn dễ hình dung
BASE_URL = "http://host.docker.internal:5000/api"

@allure.epic("API Automation Testing")
@allure.feature("Room Management & Booking API")
class TestHotelAPI:

    # ================= NHÓM 1: ROOMS (Phòng) =================
    @allure.title("API_01: Lấy danh sách toàn bộ phòng")
    def test_get_all_rooms(self):
        with allure.step("Gửi request GET /api/rooms"):
            response = requests.get(f"{BASE_URL}/rooms")
        
        with allure.step("Kiểm tra Status Code là 200 và kiểu dữ liệu trả về là List"):
            assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
            assert isinstance(response.json(), list), "Dữ liệu trả về không phải là một mảng JSON"

    @allure.title("API_02: Lấy chi tiết một phòng tồn tại")
    def test_get_room_detail_valid(self):
        with allure.step("Gửi request GET /api/rooms/1"):
            response = requests.get(f"{BASE_URL}/rooms/1")
            
        with allure.step("Kiểm tra Status Code là 200 và có thông tin phòng"):
            assert response.status_code == 200
            data = response.json()
            assert "id" in data
            assert data["id"] == 1

    @allure.title("API_03: Lấy chi tiết phòng không tồn tại")
    def test_get_room_detail_invalid(self):
        with allure.step("Gửi request GET /api/rooms/9999"):
            response = requests.get(f"{BASE_URL}/rooms/9999")
            
        with allure.step("Kiểm tra Status Code là 404 và thông báo lỗi"):
            assert response.status_code == 404
            assert "không tồn tại" in response.text

    # ================= NHÓM 2: BOOKING (Đặt phòng) =================
    @allure.title("API_04: Tạo mới đơn đặt phòng (Hợp lệ)")
    def test_create_booking_valid(self):
        payload = {"room_id": 1, "name": "Test API", "phone": "0912345678"}
        
        with allure.step("Gửi request POST /api/book với dữ liệu hợp lệ"):
            response = requests.post(f"{BASE_URL}/book", json=payload)
            
        with allure.step("Kiểm tra Status Code là 201 (hoặc 200) và có thông báo thành công"):
            # Lưu ý: Theo bảng là 201 Created, nhưng tuỳ dev cấu hình có thể là 200 OK
            assert response.status_code in [200, 201]
            assert "message" in response.json()

    @allure.title("API_05: Tạo đơn đặt phòng (Thiếu Body)")
    def test_create_booking_missing_fields(self):
        payload = {"room_id": 1} # Cố tình gửi thiếu name và phone
        
        with allure.step("Gửi request POST /api/book thiếu trường bắt buộc"):
            response = requests.post(f"{BASE_URL}/book", json=payload)
            
        with allure.step("Kiểm tra Status Code là 400 Bad Request"):
            assert response.status_code == 400
            assert "Thiếu" in response.text or "error" in response.json()

    @allure.title("API_06: Đặt phòng đã bị khóa/đã có người đặt")
    def test_create_booking_room_locked(self):
        # Đầu tiên đặt phòng số 2
        requests.post(f"{BASE_URL}/book", json={"room_id": 2, "name": "User 1", "phone": "0123"})
        
        # Đặt lại chính phòng số 2 đó
        payload = {"room_id": 2, "name": "User 2", "phone": "0999"}
        with allure.step("Cố gắng đặt lại phòng đã có người đặt"):
            response = requests.post(f"{BASE_URL}/book", json=payload)
            
        with allure.step("Kiểm tra hệ thống chặn (Status 409 hoặc 400)"):
            assert response.status_code in [400, 409]
            assert "đã" in response.text.lower() # Phải có chữ "đã" (đã đặt, đã có người...)

    # ================= NHÓM 3: ADMIN & AUTHORIZATION =================
    @allure.title("API_07: Đăng nhập Admin thành công")
    def test_admin_login_success(self):
        payload = {"username": "admin", "password": "123"}
        
        with allure.step("Gửi request POST /api/admin/login"):
            response = requests.post(f"{BASE_URL}/admin/login", json=payload)
            
        with allure.step("Kiểm tra Status Code là 200 và có Token"):
            assert response.status_code == 200
            assert "token" in response.json() or "session" in response.text.lower()

    @allure.title("API_08: Đăng nhập Admin sai mật khẩu")
    def test_admin_login_fail(self):
        payload = {"username": "admin", "password": "abc"} # Sai pass
        response = requests.post(f"{BASE_URL}/admin/login", json=payload)
        
        with allure.step("Kiểm tra Status Code là 401 Unauthorized"):
            assert response.status_code == 401
            assert "thất bại" in response.text.lower() or "sai" in response.text.lower()

    @allure.title("API_09: Thêm phòng mới (Có quyền Admin)")
    def test_create_room_with_admin(self):
        # Giả lập header có token (Tùy thuộc vào thiết kế thực tế của bạn)
        headers = {"Authorization": "Bearer admin_token_hop_le_123"}
        payload = {"name": "Phòng 301", "price": 500000}
        
        response = requests.post(f"{BASE_URL}/rooms", json=payload, headers=headers)
        
        with allure.step("Kiểm tra Status Code là 201 Created"):
            assert response.status_code == 201

    @allure.title("API_10: Thêm phòng mới (Không có quyền)")
    def test_create_room_without_auth(self):
        payload = {"name": "Phòng 301", "price": 500000}
        
        with allure.step("Gửi request thêm phòng nhưng không kèm Token"):
            response = requests.post(f"{BASE_URL}/rooms", json=payload)
            
        with allure.step("Kiểm tra hệ thống từ chối truy cập (401 hoặc 403)"):
            assert response.status_code in [401, 403]