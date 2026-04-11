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
    time.sleep(1)

@allure.epic("UI Automation Testing")
@allure.feature("End-to-End Hotel System Flow")
class TestPalatinUI:

    # ================= NHÓM 1: KHÁCH VÃNG LAI & TÀI KHOẢN =================

    @allure.title("UI_01: Khách xem danh sách phòng")
    def test_01_view_room_list(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        rooms = driver.find_elements(By.CLASS_NAME, "single-rooms-area")
        assert len(rooms) > 0, "Không hiển thị phòng nào trên giao diện!"

    @allure.title("UI_02: Khách xem chi tiết phòng")
    def test_02_view_room_detail(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        btn_details = driver.find_elements(By.CSS_SELECTOR, "a.book-room-btn")
        driver.execute_script("arguments[0].click();", btn_details[0])
        time.sleep(2)
        assert "/room/" in driver.current_url

    @allure.title("UI_03: Đăng ký tài khoản khách hàng mới")
    def test_03_register_new_user(self, driver, config):
        driver.get(config["base_url"] + "/register")
        wait_for_preloader(driver)
        rand_email = f"guest{random.randint(1000, 99999)}@gmail.com"
        driver.find_element(By.NAME, "full_name").send_keys("Nguyễn Văn Khách")
        driver.find_element(By.NAME, "email").send_keys(rand_email)
        driver.find_element(By.NAME, "phone").send_keys("0911222333")
        driver.find_element(By.NAME, "password").send_keys("123456")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)
        assert "login" in driver.current_url

    @allure.title("UI_04: Đăng nhập sai tài khoản")
    def test_04_login_fail(self, driver, config):
        driver.get(config["base_url"] + "/login")
        wait_for_preloader(driver)
        driver.find_element(By.NAME, "email").send_keys("saibettnhe@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("123")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)
        assert "sai email hoặc mật khẩu" in driver.find_element(By.CSS_SELECTOR, ".alert-danger").text.lower()

    @allure.title("UI_05: Đặt phòng thiếu thông tin (Bỏ trống ngày tháng)")
    def test_05_booking_missing_info(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        # Tìm phòng trống đầu tiên để đặt
        room_areas = driver.find_elements(By.CLASS_NAME, "single-rooms-area")
        for area in room_areas:
            if "Trống" in area.text:
                driver.execute_script("arguments[0].click();", area.find_element(By.CSS_SELECTOR, "a.book-room-btn"))
                break
        time.sleep(2)
        # Điền tên và sđt nhưng KHÔNG điền ngày tháng
        driver.execute_script("document.getElementById('detailCustName').value = 'Test User';")
        driver.execute_script("document.getElementById('detailCustPhone').value = '0901234567';")
        driver.execute_script("submitDetailBooking();")
        
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        assert "Vui lòng điền đủ" in alert.text
        alert.accept()

    @allure.title("UI_06: Đặt phòng thành công (Điền đầy đủ Check-in / Check-out)")
    def test_06_booking_success(self, driver, config):
        # Dùng JS để gán giá trị cho input Date
        driver.execute_script("document.getElementById('detailCustName').value = 'Nguyễn VIP';")
        driver.execute_script("document.getElementById('detailCustPhone').value = '0999000111';")
        driver.execute_script("document.getElementById('detailCheckIn').value = '2026-05-10';")
        driver.execute_script("document.getElementById('detailCheckOut').value = '2026-05-15';")
        driver.execute_script("submitDetailBooking();")
        
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        assert "THÀNH CÔNG" in alert.text.upper()
        alert.accept()
        time.sleep(2)


    # ================= NHÓM 2: QUẢN TRỊ VIÊN (ADMIN) =================

    @allure.title("UI_07: Admin đăng nhập thành công")
    def test_07_admin_login_success(self, driver, config):
        driver.get(config["base_url"] + "/login")
        wait_for_preloader(driver)
        driver.find_element(By.NAME, "email").send_keys("admin@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("123")
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        time.sleep(2)
        assert "admin" in driver.current_url

    @allure.title("UI_08: Admin thêm phòng mới (Upload ảnh từ máy)")
    def test_08_admin_add_new_room(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard#room")
        wait_for_preloader(driver)
        
        driver.find_element(By.NAME, "name").send_keys("Phòng Vô Cực")
        driver.find_element(By.NAME, "type").send_keys("Super VIP")
        driver.find_element(By.NAME, "price").send_keys("5000000")
        driver.find_element(By.NAME, "capacity_adults").send_keys("2")
        driver.find_element(By.NAME, "capacity_children").send_keys("1")
        
        # Upload file ảnh từ đường dẫn thật trên máy bạn
        try:
            driver.find_element(By.NAME, "image").send_keys(r"D:\z\ht3.jpg")
        except:
            print("Lưu ý: Không tìm thấy ảnh D:\\z\\ht3.jpg, bỏ qua ảnh")
            
        btn_save = driver.find_elements(By.CSS_SELECTOR, "form[action*='add'] button[type='submit']")[0]
        driver.execute_script("arguments[0].click();", btn_save)
        time.sleep(2)
        assert "thành công" in driver.page_source.lower()

    @allure.title("UI_09: Admin sửa thông tin phòng (Cập nhật qua Modal)")
    def test_09_admin_edit_room(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard#room")
        wait_for_preloader(driver)
        
        # Bấm vào nút Sửa (icon cây bút) của phòng đầu tiên
        edit_btns = driver.find_elements(By.CSS_SELECTOR, "button[data-target^='#editRoomModal']")
        if edit_btns:
            driver.execute_script("arguments[0].click();", edit_btns[0])
            time.sleep(1) # Chờ Modal mở lên
            
            # Đổi giá phòng
            price_input = driver.find_element(By.CSS_SELECTOR, ".modal.show input[name='price']")
            price_input.clear()
            price_input.send_keys("999999")
            
            # Lưu thay đổi
            save_edit_btn = driver.find_element(By.CSS_SELECTOR, ".modal.show button[type='submit']")
            driver.execute_script("arguments[0].click();", save_edit_btn)
            time.sleep(2)

    @allure.title("UI_10: Admin duyệt đơn đặt phòng & Reset Phòng")
    def test_10_admin_manage_bookings_and_reset(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard#booking")
        wait_for_preloader(driver)
        
        # Duyệt đơn hàng (nếu có)
        approve_btns = driver.find_elements(By.CSS_SELECTOR, "button[value='approve']")
        if len(approve_btns) > 0:
            driver.execute_script("arguments[0].click();", approve_btns[0])
            time.sleep(2)
            
        # Sang Tab Phòng và bấm Nút Reset (Làm trống phòng)
        driver.get(config["base_url"] + "/admin/dashboard#room")
        time.sleep(1)
        reset_btns = driver.find_elements(By.CSS_SELECTOR, "form[action*='/reset/'] button")
        if reset_btns:
            driver.execute_script("arguments[0].click();", reset_btns[0])
            WebDriverWait(driver, 3).until(EC.alert_is_present()).accept()
            time.sleep(2)

    @allure.title("UI_11: Admin xóa phòng")
    def test_11_admin_delete_room(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard#room")
        wait_for_preloader(driver)
        
        delete_btns = driver.find_elements(By.CSS_SELECTOR, "form[action*='/delete/'] button")
        if delete_btns:
            # Click nút Xóa phòng cuối cùng (thường là phòng vừa tạo ở Test 8)
            driver.execute_script("arguments[0].click();", delete_btns[-1])
            # Chấp nhận cảnh báo Confirm
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert.accept()
            time.sleep(2)