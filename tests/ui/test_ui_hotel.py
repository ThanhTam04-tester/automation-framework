import pytest
import allure
import time
import random
import os
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

    @allure.title("UI_05 & 06: Test kịch bản đặt phòng (Thiếu thông tin -> Cảnh báo -> Đặt thành công)")
    def test_05_06_booking_flow(self, driver, config):
        driver.get(config["base_url"] + "/rooms")
        wait_for_preloader(driver)
        
        # 1. Tìm phòng trống và click Xem Chi Tiết
        room_areas = driver.find_elements(By.CLASS_NAME, "single-rooms-area")
        room_found = False
        for area in room_areas:
            if "Trống" in area.text:
                driver.execute_script("arguments[0].click();", area.find_element(By.CSS_SELECTOR, "a.book-room-btn"))
                room_found = True
                break
                
        if not room_found:
            pytest.skip("Không có phòng nào đang trống để test đặt phòng.")
            
        time.sleep(2)
        
        # 2. Đợi form đặt phòng hiện ra
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "detailCustName")))
        
        # 3. Test Case 05: Cố tình điền thiếu (chỉ điền tên, bỏ trống SDT, ngày)
        name_input = driver.find_element(By.ID, "detailCustName")
        name_input.clear()
        name_input.send_keys("Khách Test Booking")
        
        # Click nút Đặt
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[onclick='submitDetailBooking()']")
        driver.execute_script("arguments[0].click();", submit_btn)
        
        # Bắt alert cảnh báo điền thiếu
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        assert "Vui lòng điền đủ" in alert.text
        alert.accept()
        time.sleep(1)
        
        # 4. Test Case 06: Điền đầy đủ thông tin để đặt thành công
        phone_input = driver.find_element(By.ID, "detailCustPhone")
        phone_input.clear()
        phone_input.send_keys("0999888777")
        
        # Đối với ô type="date", send_keys hoạt động tốt nhất định dạng YYYY-MM-DD
        # Mình dùng hàm JS để gán cho chắc chắn 100% không bị kẹt calendar popup
        driver.execute_script("document.getElementById('detailCheckIn').value = '2026-10-10';")
        driver.execute_script("document.getElementById('detailCheckOut').value = '2026-10-15';")
        
        # Click nút Đặt lần nữa
        driver.execute_script("arguments[0].click();", submit_btn)
        
        # Bắt alert Thành Công
        success_alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        assert "THÀNH CÔNG" in success_alert.text.upper()
        success_alert.accept()
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

    @allure.title("UI_08: Admin thêm phòng mới")
    def test_08_admin_add_new_room(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        # QUAN TRỌNG: Phải click chọn sang tab Quản lý phòng
        room_tab = driver.find_element(By.ID, "room-tab")
        driver.execute_script("arguments[0].click();", room_tab)
        
        # Đợi form thêm phòng hiển thị
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "name")))
        
        driver.find_element(By.NAME, "name").send_keys("Phòng Vô Cực")
        driver.find_element(By.NAME, "type").send_keys("Super VIP")
        driver.find_element(By.NAME, "price").send_keys("5000000")
        driver.find_element(By.NAME, "capacity_adults").send_keys("2")
        driver.find_element(By.NAME, "capacity_children").send_keys("1")
        
        # Xử lý upload file an toàn đa nền tảng
        test_img_path = r"D:\z\ht3.jpg"
        if os.path.exists(test_img_path):
            driver.find_element(By.NAME, "image").send_keys(test_img_path)
        else:
            print("Chạy trên môi trường ảo, bỏ qua bước upload ảnh cục bộ.")
            
        btn_save = driver.find_elements(By.CSS_SELECTOR, "form[action*='add'] button[type='submit']")[0]
        driver.execute_script("arguments[0].click();", btn_save)
        time.sleep(2)
        assert "thành công" in driver.page_source.lower()

    @allure.title("UI_09: Admin sửa thông tin phòng (Cập nhật qua Modal)")
    def test_09_admin_edit_room(self, driver, config):
        driver.get(config["base_url"] + "/admin/dashboard")
        wait_for_preloader(driver)
        
        room_tab = driver.find_element(By.ID, "room-tab")
        driver.execute_script("arguments[0].click();", room_tab)
        time.sleep(1)
        
        edit_btns = driver.find_elements(By.CSS_SELECTOR, "button[data-target^='#editRoomModal']")
        if edit_btns:
            driver.execute_script("arguments[0].click();", edit_btns[0])
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
        
        # Tab mặc định là tab Booking, cứ tìm nút approve
        approve_btns = driver.find_elements(By.CSS_SELECTOR, "button[value='approve']")
        if len(approve_btns) > 0:
            driver.execute_script("arguments[0].click();", approve_btns[0])
            time.sleep(2)
            
        # Sang Tab Phòng và bấm Nút Reset 
        driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "room-tab"))
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
        
        driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "room-tab"))
        time.sleep(1)
        
        delete_btns = driver.find_elements(By.CSS_SELECTOR, "form[action*='/delete/'] button")
        if delete_btns:
            driver.execute_script("arguments[0].click();", delete_btns[-1])
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert.accept()
            time.sleep(2)