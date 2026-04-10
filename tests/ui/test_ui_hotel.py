import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =====================================================================
# NHÓM 1: CÁC TÍNH NĂNG CỦA KHÁCH VÃNG LAI (Tìm phòng, Đặt phòng, Đăng ký)
# =====================================================================
@allure.epic("UI Automation Testing")
@allure.feature("Guest Features")
class TestGuest:

    @allure.title("UI_01: Khách xem danh sách phòng")
    def test_view_room_list(self, driver, config):
        driver.get(config["base_url"])
        time.sleep(2) # Chờ preloader tắt
        
        with allure.step("1. Truy cập trang Danh sách phòng"):
            driver.get(config["base_url"] + "/rooms")
            time.sleep(1)
            
        with allure.step("2. Xác minh hiển thị danh sách phòng"):
            rooms = driver.find_elements(By.CLASS_NAME, "single-rooms-area")
            assert len(rooms) > 0, "Không hiển thị phòng nào trên trang!"

    @allure.title("UI_02: Khách xem chi tiết phòng")
    def test_view_room_detail(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        time.sleep(2)
        
        with allure.step("1. Click nút Xem chi tiết phòng đầu tiên"):
            # Lấy nút "Xem chi tiết" đầu tiên tìm thấy
            btn_detail = driver.find_element(By.XPATH, "(//a[contains(text(), 'Xem chi tiết')])[1]")
            driver.execute_script("arguments[0].click();", btn_detail)
            time.sleep(2)
            
        with allure.step("2. Xác minh chuyển hướng đúng trang chi tiết"):
            assert "/room/" in driver.current_url
            assert len(driver.find_elements(By.ID, "detailCustName")) > 0 # Có form đặt phòng chi tiết

    @allure.title("UI_03: Đặt phòng thành công (Happy Path)")
    def test_booking_happy_path(self, driver, config):
        driver.get(config["base_url"])
        time.sleep(2)
        
        with allure.step("1. Điền Form Tên, SĐT, Ngày nhận và Chọn phòng"):
            driver.find_element(By.ID, "custName").send_keys("Nguyen Van A")
            driver.find_element(By.ID, "custPhone").send_keys("0901234567")
            driver.execute_script("document.getElementById('roomSelect').value = '2';") # Chọn phòng ID 2
            
        with allure.step("2. Bấm nút Đặt Phòng"):
            btn = driver.find_element(By.ID, "btnBook")
            driver.execute_script("arguments[0].click();", btn)
            
        with allure.step("3. Xác minh hiển thị Popup Thành Công"):
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert_text = alert.text
            assert "THÀNH CÔNG" in alert_text
            alert.accept()

    @allure.title("UI_04: Đặt phòng thiếu thông tin bắt buộc")
    def test_booking_missing_info(self, driver, config):
        driver.get(config["base_url"])
        time.sleep(2)
        
        with allure.step("1. Chỉ điền Tên, cố tình bỏ trống SĐT"):
            driver.find_element(By.ID, "custName").send_keys("Nguyen Van B")
            # Bỏ trống custPhone
            driver.execute_script("document.getElementById('roomSelect').value = '1';")
            
        with allure.step("2. Bấm nút Đặt Phòng"):
            btn = driver.find_element(By.ID, "btnBook")
            driver.execute_script("arguments[0].click();", btn)
            
        with allure.step("3. Xác minh hệ thống báo lỗi không cho đặt"):
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            assert "Vui lòng điền đủ" in alert.text
            alert.accept()

    @allure.title("UI_05: Đăng ký tài khoản Khách hàng mới")
    def test_register_new_user(self, driver, config):
        driver.get(config["base_url"] + "/register")
        time.sleep(2)
        
        with allure.step("1. Điền thông tin đăng ký hợp lệ"):
            # Tạo email random để test không bị trùng khi chạy nhiều lần
            import random
            rand_email = f"khachmoi{random.randint(1000, 9999)}@gmail.com"
            
            driver.find_element(By.NAME, "full_name").send_keys("Khách Hàng Mới")
            driver.find_element(By.NAME, "email").send_keys(rand_email)
            driver.find_element(By.NAME, "phone").send_keys("0911222333")
            driver.find_element(By.NAME, "password").send_keys("123456")
            
        with allure.step("2. Bấm nút Đăng Ký"):
            btn_submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", btn_submit)
            time.sleep(2)
            
        with allure.step("3. Xác minh chuyển hướng về Login và có thông báo"):
            assert "login" in driver.current_url
            success_msg = driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            assert "Đăng ký thành công" in success_msg


# =====================================================================
# NHÓM 2: TÍNH NĂNG CỦA KHÁCH HÀNG ĐÃ ĐĂNG NHẬP
# =====================================================================
@allure.epic("UI Automation Testing")
@allure.feature("Customer Features")
class TestCustomer:

    @allure.title("UI_07: Đăng nhập sai tài khoản")
    def test_login_fail(self, driver, config):
        driver.get(config["base_url"] + "/login")
        time.sleep(2)
        
        with allure.step("1. Nhập sai thông tin đăng nhập"):
            driver.find_element(By.NAME, "email").send_keys("khachkhongtontai@gmail.com")
            driver.find_element(By.NAME, "password").send_keys("matkhausai")
            btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)
            
        with allure.step("2. Xác minh thông báo lỗi hiển thị"):
            error_msg = driver.find_element(By.CSS_SELECTOR, ".alert-danger").text
            assert "không đúng" in error_msg.lower() or "tồn tại" in error_msg.lower()

    @allure.title("UI_06: Khách kiểm tra Lịch sử đặt phòng (My Bookings)")
    def test_check_my_bookings(self, driver, config):
        # 1. Cần đăng nhập trước (Dùng tài khoản test mặc định mà bạn tạo sẵn hoặc Admin)
        driver.get(config["base_url"] + "/login")
        time.sleep(2)
        driver.find_element(By.NAME, "email").send_keys("admin@palatin.com") # Ở app.py, admin cũng xem được
        driver.find_element(By.NAME, "password").send_keys("123456")
        btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)

        with allure.step("1. Truy cập trang Đơn của tôi"):
            driver.get(config["base_url"] + "/my-bookings")
            time.sleep(1)
            
        with allure.step("2. Xác minh hiển thị bảng lịch sử"):
            tables = driver.find_elements(By.TAG_NAME, "table")
            assert len(tables) > 0, "Không có bảng hiển thị lịch sử"


# =====================================================================
# NHÓM 3: TÍNH NĂNG CỦA QUẢN TRỊ VIÊN (ADMIN)
# =====================================================================
@allure.epic("UI Automation Testing")
@allure.feature("Admin Features")
class TestAdmin:

    @allure.title("UI_08: Admin đăng nhập thành công")
    def test_admin_login_success(self, driver, config):
        driver.get(config["base_url"] + "/login")
        time.sleep(2)
        
        with allure.step("1. Nhập tài khoản Admin"):
            driver.find_element(By.NAME, "email").send_keys("admin@palatin.com")
            driver.find_element(By.NAME, "password").send_keys("123456")
            
        with allure.step("2. Bấm Đăng Nhập"):
            btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(2)
            
        with allure.step("3. Xác minh vào được Dashboard Admin"):
            assert "/admin" in driver.current_url

    @allure.title("UI_10: Admin từ chối đơn đặt phòng")
    def test_admin_reject_booking(self, driver, config):
        # Yêu cầu Admin đã đăng nhập (Giữ session từ test trước hoặc login lại)
        driver.get(config["base_url"] + "/login")
        driver.find_element(By.NAME, "email").send_keys("admin@palatin.com")
        driver.find_element(By.NAME, "password").send_keys("123456")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)
        
        with allure.step("1. Tìm đơn hàng đang Chờ duyệt và bấm Từ chối"):
            # Lấy tất cả các nút "Từ chối" trên màn hình
            reject_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Từ chối')]")
            if len(reject_buttons) > 0:
                driver.execute_script("arguments[0].click();", reject_buttons[0])
                time.sleep(2)
                with allure.step("2. Xác minh thông báo Thành công"):
                    success_msg = driver.find_element(By.CSS_SELECTOR, ".alert").text
                    assert "từ chối" in success_msg.lower()
            else:
                pytest.skip("Không có đơn hàng nào đang ở trạng thái 'Chờ duyệt' để từ chối.")

    @allure.title("UI_11: Admin duyệt đơn đặt phòng")
    def test_admin_approve_booking(self, driver, config):
        driver.get(config["base_url"] + "/login")
        driver.find_element(By.NAME, "email").send_keys("admin@palatin.com")
        driver.find_element(By.NAME, "password").send_keys("123456")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)
        
        with allure.step("1. Tìm đơn hàng đang Chờ duyệt và bấm Duyệt"):
            # Lấy tất cả các nút "Duyệt" trên màn hình
            approve_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Duyệt')]")
            if len(approve_buttons) > 0:
                driver.execute_script("arguments[0].click();", approve_buttons[0])
                time.sleep(2)
                with allure.step("2. Xác minh thông báo Thành công"):
                    success_msg = driver.find_element(By.CSS_SELECTOR, ".alert").text
                    assert "duyệt" in success_msg.lower()
            else:
                pytest.skip("Không có đơn hàng nào đang ở trạng thái 'Chờ duyệt' để duyệt.")