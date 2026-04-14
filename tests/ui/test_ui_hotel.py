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
from allure_commons.types import AttachmentType

def wait_for_preloader(driver):
    try:
        WebDriverWait(driver, 15).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "preloader"))
        )
    except: pass
    time.sleep(1.5)

def login_as_admin(driver, base_url):
    """Hàm hỗ trợ: Đảm bảo luôn đăng nhập Admin trước khi test các chức năng quản trị"""
    driver.get(base_url + "/login")
    wait_for_preloader(driver)
    
    # Nếu đã ở dashboard thì không cần login nữa
    if "dashboard" in driver.current_url:
        return
        
    driver.find_element(By.NAME, "email").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
    time.sleep(1.5)


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
        # Chụp ảnh danh sách phòng
        allure.attach(driver.get_screenshot_as_png(), name="Anh_Danh_Sach_Phong", attachment_type=AttachmentType.PNG)

    @allure.title("UI_02: Khách xem chi tiết phòng")
    def test_02_view_room_detail(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        btn_details = driver.find_elements(By.CSS_SELECTOR, "a.book-room-btn")
        driver.execute_script("arguments[0].click();", btn_details[0])
        time.sleep(2)
        assert "/room/" in driver.current_url
        # Chụp ảnh chi tiết phòng
        allure.attach(driver.get_screenshot_as_png(), name="Anh_Chi_Tiet_Phong", attachment_type=AttachmentType.PNG)

    @allure.title("UI_03: Đăng ký tài khoản khách hàng mới")
    def test_03_register_new_user(self, driver, config):
        driver.get(config["base_url"] + "/register")
        wait_for_preloader(driver)
        rand_email = f"guest{random.randint(1000, 99999)}@gmail.com"
        driver.find_element(By.NAME, "full_name").send_keys("Nguyễn Văn Khách")
        driver.find_element(By.NAME, "email").send_keys(rand_email)
        driver.find_element(By.NAME, "phone").send_keys("0911222333")
        driver.find_element(By.NAME, "password").send_keys("123456")
        
        # Chụp ảnh form đăng ký trước khi bấm
        allure.attach(driver.get_screenshot_as_png(), name="Anh_Form_Dang_Ky", attachment_type=AttachmentType.PNG)
        
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
        # Chụp ảnh thông báo lỗi
        allure.attach(driver.get_screenshot_as_png(), name="Anh_Loi_Dang_Nhap", attachment_type=AttachmentType.PNG)

    @allure.title("UI_05 & 06: Cảnh báo điền thiếu và Đặt phòng thành công")
    def test_05_06_booking_flow(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        
        empty_room_links = []
        room_areas = driver.find_elements(By.CLASS_NAME, "single-rooms-area")
        for area in room_areas:
            if "Trống" in area.text:
                link = area.find_element(By.CSS_SELECTOR, "a.book-room-btn").get_attribute("href")
                empty_room_links.append(link)
                
        if len(empty_room_links) == 0:
            pytest.skip("Bỏ qua test vì hiện không có phòng nào Trống.")
            
        driver.get(empty_room_links[0])
        wait_for_preloader(driver)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "detailCustName")))
        
        # --- TEST CẢNH BÁO ĐIỀN THIẾU ---
        driver.execute_script("document.getElementById('detailCustName').value = 'Khách Test Thiếu';")
        driver.execute_script("document.getElementById('detailCustPhone').value = '';")
        driver.execute_script("submitDetailBooking();")
        
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        assert "Vui lòng điền đủ" in alert.text
        alert.accept()
        time.sleep(1)
        
        # --- TEST ĐIỀN ĐẦY ĐỦ ---
        driver.execute_script("document.getElementById('detailCustName').value = 'Khách Đặt Full';")
        driver.execute_script("document.getElementById('detailCustPhone').value = '0999888777';")
        driver.execute_script("document.getElementById('detailCheckIn').value = '2026-10-10';")
        driver.execute_script("document.getElementById('detailCheckOut').value = '2026-10-15';")
        
        with allure.step("Chụp ảnh Form Đặt Phòng đã điền đầy đủ"):
            # CHỤP ẢNH TẠI ĐÂY: Form đã có đủ data, trước khi JS Alert hiện ra chặn màn hình
            allure.attach(driver.get_screenshot_as_png(), name="Anh_Form_Dat_Phong_Thanh_Cong", attachment_type=AttachmentType.PNG)
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[onclick='submitDetailBooking()']")
        driver.execute_script("arguments[0].click();", submit_btn)
        
        success_alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        assert "THÀNH CÔNG" in success_alert.text.upper()
        success_alert.accept()
        time.sleep(2)


    # ================= NHÓM 2: QUẢN TRỊ VIÊN (ADMIN) =================

    @allure.title("UI_07: Admin đăng nhập thành công")
    def test_07_admin_login_success(self, driver, config):
        login_as_admin(driver, config["base_url"])
        assert "admin" in driver.current_url
        # Chụp ảnh trang quản trị Dashboard
        allure.attach(driver.get_screenshot_as_png(), name="Anh_Admin_Dashboard", attachment_type=AttachmentType.PNG)

    @allure.title("UI_08: Admin thêm phòng mới (Tự động giả lập ảnh upload)")
    def test_08_admin_add_new_room(self, driver, config):
        login_as_admin(driver, config["base_url"])
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        driver.execute_script("document.getElementById('room-tab').click();")
        time.sleep(2)
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "name")))
        
        driver.find_element(By.NAME, "name").send_keys("Phòng Thử Nghiệm Mới")
        driver.find_element(By.NAME, "type").send_keys("Super VIP")
        driver.find_element(By.NAME, "price").send_keys("5000000")
        driver.find_element(By.NAME, "capacity_adults").send_keys("2")
        driver.find_element(By.NAME, "capacity_children").send_keys("1")
        
        fd, temp_img_path = tempfile.mkstemp(suffix=".jpg")
        with open(temp_img_path, 'wb') as f:
            f.write(b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01')
        os.close(fd)
        
        driver.find_element(By.NAME, "image").send_keys(temp_img_path)
            
        with allure.step("Chụp ảnh form thêm phòng mới"):
            allure.attach(driver.get_screenshot_as_png(), name="Anh_Form_Them_Phong", attachment_type=AttachmentType.PNG)

        btn_save = driver.find_elements(By.CSS_SELECTOR, "form[action*='add'] button[type='submit']")[0]
        driver.execute_script("arguments[0].click();", btn_save)
        time.sleep(3)
        assert "thành công" in driver.page_source.lower()

    @allure.title("UI_09: Admin sửa thông tin phòng (Cập nhật qua Modal)")
    def test_09_admin_edit_room(self, driver, config):
        login_as_admin(driver, config["base_url"])
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        driver.execute_script("document.getElementById('room-tab').click();")
        time.sleep(2)
        
        edit_btns = driver.find_elements(By.CSS_SELECTOR, "button[data-target^='#editRoomModal']")
        if edit_btns:
            driver.execute_script("arguments[0].click();", edit_btns[-1])
            time.sleep(2) 
            
            price_input = driver.find_element(By.CSS_SELECTOR, ".modal.show input[name='price']")
            price_input.clear()
            price_input.send_keys("999999")
            
            with allure.step("Chụp ảnh Modal sửa thông tin"):
                allure.attach(driver.get_screenshot_as_png(), name="Anh_Modal_Sua_Phong", attachment_type=AttachmentType.PNG)
            
            save_edit_btn = driver.find_element(By.CSS_SELECTOR, ".modal.show button[type='submit']")
            driver.execute_script("arguments[0].click();", save_edit_btn)
            time.sleep(3)

    @allure.title("UI_10: Admin duyệt đơn đặt phòng & Reset Phòng")
    def test_10_admin_manage_bookings_and_reset(self, driver, config):
        login_as_admin(driver, config["base_url"])
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        # Duyệt đơn hàng
        approve_btns = driver.find_elements(By.CSS_SELECTOR, "button[value='approve']")
        if len(approve_btns) > 0:
            driver.execute_script("arguments[0].click();", approve_btns[0])
            time.sleep(3)
            
        driver.execute_script("document.getElementById('room-tab').click();")
        time.sleep(2)
        
        reset_btns = driver.find_elements(By.CSS_SELECTOR, "form[action*='/reset/'] button")
        if reset_btns:
            driver.execute_script("arguments[0].click();", reset_btns[0])
            WebDriverWait(driver, 5).until(EC.alert_is_present()).accept()
            time.sleep(3)

    @allure.title("UI_11: Admin xóa phòng")
    def test_11_admin_delete_room(self, driver, config):
        login_as_admin(driver, config["base_url"])
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        driver.execute_script("document.getElementById('room-tab').click();")
        time.sleep(2)
        
        delete_btns = driver.find_elements(By.CSS_SELECTOR, "form[action*='/delete/'] button")
        if delete_btns:
            # Chụp ảnh trước khi bấm xóa
            allure.attach(driver.get_screenshot_as_png(), name="Anh_Truoc_Khi_Xoa_Phong", attachment_type=AttachmentType.PNG)
            
            driver.execute_script("arguments[0].click();", delete_btns[-1])
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert.accept()
            time.sleep(3)