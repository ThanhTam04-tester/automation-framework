import pytest
import allure
import time
import random
import os
import tempfile
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

    @allure.title("UI_05 & 06: Cảnh báo điền thiếu và Chạy lặp Đặt toàn bộ phòng trống")
    def test_05_06_booking_flow(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        
        # 1. Tìm tất cả các link của các phòng đang "Trống"
        empty_room_links = []
        room_areas = driver.find_elements(By.CLASS_NAME, "single-rooms-area")
        for area in room_areas:
            if "Trống" in area.text:
                link = area.find_element(By.CSS_SELECTOR, "a.book-room-btn").get_attribute("href")
                empty_room_links.append(link)
                
        if not empty_room_links:
            pytest.skip("Database hiện không có phòng nào Trống. Hãy reset database!")
            
        # 2. Vô phòng trống đầu tiên để Test cảnh báo điền thiếu thông tin
        driver.get(empty_room_links[0])
        wait_for_preloader(driver)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "detailCustName")))
        
        driver.execute_script("document.getElementById('detailCustName').value = 'Khách Test Thiếu';")
        driver.execute_script("document.getElementById('detailCustPhone').value = '';") # Bỏ trống sdt
        driver.execute_script("submitDetailBooking();")
        
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        assert "Vui lòng điền đủ" in alert.text
        alert.accept()
        time.sleep(1)
        
        # 3. Lặp qua tất cả các phòng trống và Đặt thành công
        for index, link in enumerate(empty_room_links):
            driver.get(link)
            wait_for_preloader(driver)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "detailCustName")))
            
            driver.execute_script(f"document.getElementById('detailCustName').value = 'Khách Hàng {index}';")
            driver.execute_script("document.getElementById('detailCustPhone').value = '0999888777';")
            driver.execute_script("document.getElementById('detailCheckIn').value = '2026-10-10';")
            driver.execute_script("document.getElementById('detailCheckOut').value = '2026-10-15';")
            
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[onclick='submitDetailBooking()']")
            driver.execute_script("arguments[0].click();", submit_btn)
            
            success_alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert "THÀNH CÔNG" in success_alert.text.upper()
            success_alert.accept()
            time.sleep(1)


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

    @allure.title("UI_08: Admin thêm phòng mới (Tự động giả lập ảnh upload)")
    def test_08_admin_add_new_room(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        # ÉP MỞ TAB PHÒNG BẰNG JQUERY
        driver.execute_script("$('#room-tab').tab('show');")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "name")))
        
        driver.find_element(By.NAME, "name").send_keys("Phòng Thử Nghiệm Tự Động")
        driver.find_element(By.NAME, "type").send_keys("Super VIP")
        driver.find_element(By.NAME, "price").send_keys("5000000")
        driver.find_element(By.NAME, "capacity_adults").send_keys("2")
        driver.find_element(By.NAME, "capacity_children").send_keys("1")
        
        # Tự động tạo 1 file ảnh ảo để upload qua Jenkins không bị lỗi
        fd, temp_img_path = tempfile.mkstemp(suffix=".jpg")
        with open(temp_img_path, 'wb') as f:
            f.write(b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01') # Header chuẩn của file JPG
        os.close(fd)
        
        driver.find_element(By.NAME, "image").send_keys(temp_img_path)
            
        btn_save = driver.find_elements(By.CSS_SELECTOR, "form[action*='add'] button[type='submit']")[0]
        driver.execute_script("arguments[0].click();", btn_save)
        time.sleep(2)
        assert "thành công" in driver.page_source.lower()

    @allure.title("UI_09: Admin sửa thông tin phòng (Cập nhật qua Modal)")
    def test_09_admin_edit_room(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        # ÉP MỞ TAB PHÒNG
        driver.execute_script("$('#room-tab').tab('show');")
        time.sleep(1)
        
        edit_btns = driver.find_elements(By.CSS_SELECTOR, "button[data-target^='#editRoomModal']")
        if edit_btns:
            # Chọn sửa phòng cuối cùng (phòng vừa thêm)
            driver.execute_script("arguments[0].click();", edit_btns[-1])
            time.sleep(1) 
            
            price_input = driver.find_element(By.CSS_SELECTOR, ".modal.show input[name='price']")
            price_input.clear()
            price_input.send_keys("999999")
            
            save_edit_btn = driver.find_element(By.CSS_SELECTOR, ".modal.show button[type='submit']")
            driver.execute_script("arguments[0].click();", save_edit_btn)
            time.sleep(2)

    @allure.title("UI_10: Admin duyệt đơn đặt phòng & Reset Phòng")
    def test_10_admin_manage_bookings_and_reset(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        # Tab mặc định là tab Booking, duyệt đơn hàng nếu có
        approve_btns = driver.find_elements(By.CSS_SELECTOR, "button[value='approve']")
        if len(approve_btns) > 0:
            driver.execute_script("arguments[0].click();", approve_btns[0])
            time.sleep(2)
            
        # ÉP MỞ TAB PHÒNG
        driver.execute_script("$('#room-tab').tab('show');")
        time.sleep(1)
        
        reset_btns = driver.find_elements(By.CSS_SELECTOR, "form[action*='/reset/'] button")
        if reset_btns:
            driver.execute_script("arguments[0].click();", reset_btns[0])
            WebDriverWait(driver, 3).until(EC.alert_is_present()).accept()
            time.sleep(2)

    @allure.title("UI_11: Admin xóa phòng")
    def test_11_admin_delete_room(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        # ÉP MỞ TAB PHÒNG
        driver.execute_script("$('#room-tab').tab('show');")
        time.sleep(1)
        
        delete_btns = driver.find_elements(By.CSS_SELECTOR, "form[action*='/delete/'] button")
        if delete_btns:
            driver.execute_script("arguments[0].click();", delete_btns[-1])
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert.accept()
            time.sleep(2)