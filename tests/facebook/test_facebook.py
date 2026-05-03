import pytest
import allure
import time
from selenium.webdriver.common.by import By

@allure.epic("Cross-Project Testing")
@allure.feature("Facebook Default Functions")
class TestFacebook:
    @allure.title("TC_01: Kiểm tra các thành phần mặc định trên trang chủ Facebook")
    def test_facebook_basic_ui(self, driver):
        target_url = "https://www.facebook.com"
        
        with allure.step(f"1. Truy cập vào trang chủ Facebook: {target_url}"):
            driver.get(target_url)
            time.sleep(2) # Chờ load trang
            
        with allure.step("2. Xác minh tiêu đề trang"):
            # Đảm bảo robot đã thực sự vào đúng trang Facebook
            assert "Facebook" in driver.title
            
        with allure.step("3. Kiểm tra các form đăng nhập mặc định"):
            # Facebook luôn cố định ID của 2 ô này, nên rất an toàn để test
            email_box = driver.find_elements(By.ID, "email")
            pass_box = driver.find_elements(By.ID, "pass")
            login_btn = driver.find_elements(By.NAME, "login")
            
            assert len(email_box) > 0, "Lỗi: Không tìm thấy ô nhập Email"
            assert len(pass_box) > 0, "Lỗi: Không tìm thấy ô nhập Mật khẩu"
            assert len(login_btn) > 0, "Lỗi: Không tìm thấy nút Đăng nhập"
            
        with allure.step("4. Kiểm tra nút 'Tạo tài khoản mới' có tồn tại"):
            # Tìm nút tạo tài khoản bằng thuộc tính đặc biệt của Facebook
            create_acc_btn = driver.find_elements(By.XPATH, "//a[@data-testid='open-registration-form-button']")
            assert len(create_acc_btn) > 0, "Lỗi: Không tìm thấy nút Tạo tài khoản mới"
            
        with allure.step("5. Chụp ảnh màn hình làm bằng chứng"):
            # Chụp lại cái giao diện Facebook lúc robot đang quét để show lên Allure Report
            allure.attach(driver.get_screenshot_as_png(), name="Facebook_Homepage", attachment_type=allure.attachment_type.PNG)