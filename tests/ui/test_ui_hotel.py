import pytest
import allure
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

def wait_for_preloader(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "preloader"))
        )
    except: pass
    time.sleep(2)

# ================= NHÓM 1: QUẢN TRỊ VIÊN (CHẠY TRƯỚC ĐỂ RESET PHÒNG) =================
@allure.epic("UI Automation Testing")
@allure.feature("Admin Features")
class TestAdmin:

    @allure.title("UI_08: Admin đăng nhập thành công")
    def test_01_admin_login_success(self, driver, config):
        driver.get(config["base_url"] + "/login")
        wait_for_preloader(driver)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("admin@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("123")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)
        assert "admin" in driver.current_url

    @allure.title("UI_09: Admin reset trạng thái phòng về Trống")
    def test_02_admin_reset_rooms(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        with allure.step("Sang tab Quản lý phòng và Set phòng 1 thành Trống"):
            driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "room-tab"))
            time.sleep(1)
            
            selects = driver.find_elements(By.NAME, "status")
            if len(selects) > 0:
                Select(selects[0]).select_by_value("Trống")
                save_btn = driver.find_elements(By.CSS_SELECTOR, "form[action*='/admin/rooms/status'] button")[0]
                driver.execute_script("arguments[0].click();", save_btn)
                time.sleep(2)

    @allure.title("UI_10 & 11: Admin quản lý đơn (Duyệt/Từ chối)")
    def test_03_admin_manage_booking(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        with allure.step("Tìm đơn hàng và bấm Duyệt"):
            approve_btns = driver.find_elements(By.CSS_SELECTOR, "button[value='approve']")
            if len(approve_btns) > 0:
                driver.execute_script("arguments[0].click();", approve_btns[0])
                time.sleep(2)
                assert "duyệt" in driver.page_source.lower()
            else:
                pytest.skip("Không có đơn hàng nào đang chờ duyệt.")


# ================= NHÓM 2: KHÁCH VÃNG LAI (CHẠY SAU KHI CÓ PHÒNG TRỐNG) =================
@allure.epic("UI Automation Testing")
@allure.feature("Guest Features")
class TestGuest:

    @allure.title("UI_01: Khách xem danh sách phòng")
    def test_04_view_room_list(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        rooms = driver.find_elements(By.CLASS_NAME, "single-rooms-area")
        assert len(rooms) > 0

    @allure.title("UI_02: Khách xem chi tiết phòng")
    def test_05_view_room_detail(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        btn_details = driver.find_elements(By.CSS_SELECTOR, "a.book-room-btn")
        driver.execute_script("arguments[0].click();", btn_details[0])
        time.sleep(2)
        assert "/room/" in driver.current_url

    @allure.title("UI_03: Đặt phòng thành công (Happy Path)")
    def test_06_booking_happy_path(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        
        # Nhờ Admin đã reset ở trên, chắc chắn sẽ có phòng Trống
        room_areas = driver.find_elements(By.CLASS_NAME, "single-rooms-area")
        for area in room_areas:
            if "Trống" in area.text:
                driver.execute_script("arguments[0].click();", area.find_element(By.CSS_SELECTOR, "a.book-room-btn"))
                break
        time.sleep(3)
        
        driver.execute_script("document.getElementById('detailCustName').value = 'Nguyen Van A';")
        driver.execute_script("document.getElementById('detailCustPhone').value = '0901234567';")
        driver.execute_script("submitDetailBooking();")
        
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        assert "THÀNH CÔNG" in alert.text.upper()
        alert.accept()

    @allure.title("UI_04: Đặt phòng thiếu thông tin bắt buộc")
    def test_07_booking_missing_info(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        
        room_areas = driver.find_elements(By.CLASS_NAME, "single-rooms-area")
        for area in room_areas:
            if "Trống" in area.text:
                driver.execute_script("arguments[0].click();", area.find_element(By.CSS_SELECTOR, "a.book-room-btn"))
                break
        time.sleep(3)

        driver.execute_script("document.getElementById('detailCustName').value = 'Nguyen Van B';")
        driver.execute_script("document.getElementById('detailCustPhone').value = '';")
        driver.execute_script("submitDetailBooking();")
        
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        assert "Vui lòng điền đủ" in alert.text
        alert.accept()

    @allure.title("UI_05: Đăng ký tài khoản mới")
    def test_08_register_new_user(self, driver, config):
        driver.get(config["base_url"] + "/register")
        wait_for_preloader(driver)
        
        rand_email = f"khach{random.randint(1000, 99999)}@gmail.com"
        driver.find_element(By.NAME, "full_name").send_keys("Khách Hàng")
        driver.find_element(By.NAME, "email").send_keys(rand_email)
        driver.find_element(By.NAME, "phone").send_keys("0911222333")
        driver.find_element(By.NAME, "password").send_keys("123456")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)
        assert "login" in driver.current_url


# ================= NHÓM 3: KHÁCH ĐÃ ĐĂNG NHẬP =================
@allure.epic("UI Automation Testing")
@allure.feature("Customer Features")
class TestCustomer:

    @allure.title("UI_07: Đăng nhập sai tài khoản")
    def test_09_login_fail(self, driver, config):
        driver.get(config["base_url"] + "/login")
        wait_for_preloader(driver)
        driver.find_element(By.NAME, "email").send_keys("sai@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("matkhausai")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)
        assert "sai email hoặc mật khẩu" in driver.find_element(By.CSS_SELECTOR, ".alert-danger").text.lower()

    @allure.title("UI_06: Khách kiểm tra Lịch sử đặt phòng")
    def test_10_check_my_bookings(self, driver, config):
        rand_email = f"user{random.randint(1000,9999)}@gmail.com"
        
        # Tạo nhanh 1 tài khoản và đăng nhập
        driver.get(config["base_url"] + "/register")
        wait_for_preloader(driver)
        driver.find_element(By.NAME, "full_name").send_keys("Khách")
        driver.find_element(By.NAME, "email").send_keys(rand_email)
        driver.find_element(By.NAME, "phone").send_keys("0900")
        driver.find_element(By.NAME, "password").send_keys("123456")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)

        driver.get(config["base_url"] + "/login")
        wait_for_preloader(driver)
        driver.find_element(By.NAME, "email").send_keys(rand_email)
        driver.find_element(By.NAME, "password").send_keys("123456")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)

        driver.get(config["base_url"] + "/my-bookings")
        wait_for_preloader(driver)
        assert len(driver.find_elements(By.TAG_NAME, "table")) > 0