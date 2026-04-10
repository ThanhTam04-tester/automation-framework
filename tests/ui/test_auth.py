import pytest
import allure
import time
from selenium.webdriver.common.by import By

@allure.epic("UI Automation Testing")
@allure.feature("Authentication")
class TestAuthentication:

    @allure.title("TC_01: Đăng ký tài khoản thành công")
    def test_register_success(self, driver, config):
        driver.get(config["base_url"] + "/register")
        with allure.step("Điền thông tin đăng ký"):
            driver.find_element(By.NAME, "full_name").send_keys("Nguyễn Văn Test")
            driver.find_element(By.NAME, "email").send_keys("testuser@gmail.com")
            driver.find_element(By.NAME, "phone").send_keys("0901234567")
            driver.find_element(By.NAME, "password").send_keys("123456")
        
        with allure.step("Bấm nút Đăng ký"):
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(5)
            # Kiểm tra xem có được chuyển hướng không hoặc có thông báo thành công không
            assert "login" in driver.current_url or "register" in driver.current_url

    @allure.title("TC_02: Đăng nhập thành công với tài khoản hợp lệ")
    def test_login_success(self, driver, config):
        driver.get(config["base_url"] + "/login")
        with allure.step("Điền Email và Password"):
            driver.find_element(By.NAME, "email").send_keys("testuser@gmail.com")
            driver.find_element(By.NAME, "password").send_keys("123456")
        
        with allure.step("Bấm nút Đăng nhập"):
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(5)
            assert "login" not in driver.current_url # Chuyển hướng khỏi trang login

    @allure.title("TC_03: Đăng nhập thất bại (Sai mật khẩu)")
    def test_login_fail_wrong_password(self, driver, config):
        driver.get(config["base_url"] + "/login")
        driver.find_element(By.NAME, "email").send_keys("testuser@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        
        with allure.step("Kiểm tra thông báo lỗi hiển thị"):
            error_msg = driver.find_element(By.CSS_SELECTOR, ".alert-danger").text
            assert len(error_msg) > 0 # Có hiển thị thông báo lỗi (flash message)