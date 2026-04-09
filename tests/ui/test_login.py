import pytest
import allure
from selenium.webdriver.common.by import By

# Thêm các thẻ này để Allure phân loại báo cáo cho đẹp
@allure.epic("Web UI Testing")
@allure.feature("Chức năng Đăng nhập")
@allure.title("Test Đăng nhập thất bại để bắt lỗi chụp ảnh")
def test_dang_nhap_that_bai(driver):
    
    with allure.step("Bước 1: Mở trang web đăng nhập"):
        driver.get("http://localhost:5000/login") # URL trang web của bạn
        
    with allure.step("Bước 2: Nhập Username và Password sai"):
        # Thay "user" và "pass" bằng ID thật trên giao diện của bạn
        driver.find_element(By.ID, "user").send_keys("admin")
        driver.find_element(By.ID, "pass").send_keys("sai_mat_khau")
        
    with allure.step("Bước 3: Bấm nút Đăng nhập"):
        driver.find_element(By.ID, "login-btn").click()
        
    with allure.step("Bước 4: Xác minh thông báo lỗi"):
        # Dòng assert này cố tình kiểm tra sai để ép Pytest báo FAILED.
        # Khi báo FAILED, hook trong conftest.py sẽ tự động chụp màn hình!
        assert "Đăng nhập thành công" in driver.page_source, "Test Fail: Hệ thống không cho đăng nhập!"