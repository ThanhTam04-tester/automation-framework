import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.epic("Cross-Project Testing")
@allure.feature("DemoQA Practice Form")
class TestDemoQA:
    @allure.title("TC_01: Truy cập thành công trang DemoQA")
    # Thêm config vào đây để đồng bộ với framework của bạn
    def test_open_demoqa(self, driver, config):
        target_url = config['base_url']
        
        with allure.step(f"1. Truy cập vào website: {target_url}"):
            driver.get(target_url)
            
        with allure.step("2. Xác minh website mở thành công"):
            # Chờ cho đến khi logo/banner hiển thị thay vì sleep
            wait = WebDriverWait(driver, 10)
            banner = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "home-banner")))
            assert banner.is_displayed(), "Không tìm thấy banner trang chủ DemoQA!"

        with allure.step("3. Click vào mục Elements"):
            # Tìm thẻ Elements
            elements_card = driver.find_element(By.XPATH, "//h5[text()='Elements']")
            
            # Mẹo: Scroll xuống để tránh bị quảng cáo che mất element trước khi click
            driver.execute_script("arguments[0].scrollIntoView();", elements_card)
            time.sleep(0.5) 
            elements_card.click()

        with allure.step("4. Xác minh đã chuyển sang trang Elements"):
            # Đợi header "Elements" xuất hiện
            header = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "main-header")))
            assert "elements" in driver.current_url
            assert header.text == "Elements"
            
        with allure.step("5. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(), 
                name="DemoQA_Elements_Page", 
                attachment_type=allure.attachment_type.PNG
            )