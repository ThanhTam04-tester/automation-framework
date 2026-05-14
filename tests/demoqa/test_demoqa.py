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
    def test_open_demoqa(self, driver, config):
        # SỬA LẠI Ở ĐÂY: Gọi đúng tên key trong file yaml
        target_url = config['base_url'] 
        wait = WebDriverWait(driver, 15)

        with allure.step(f"1. Truy cập vào website: {target_url}"):
            driver.get(target_url)
            time.sleep(2)  # Chờ quảng cáo load xong

        with allure.step("2. Xác minh website mở thành công"):
            banner = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "home-banner")
            ))
            assert banner.is_displayed(), "Không tìm thấy banner trang chủ DemoQA!"

        with allure.step("3. Click vào mục Elements"):
            elements_card = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//h5[text()='Elements']")
            ))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elements_card)
            time.sleep(0.5)
            # Dùng JS click để tránh bị quảng cáo chặn
            driver.execute_script("arguments[0].click();", elements_card)

        with allure.step("4. Xác minh đã chuyển sang trang Elements"):
            header = wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, "main-header")
            ))
            assert "elements" in driver.current_url, f"URL sai: {driver.current_url}"
            assert header.text == "Elements", f"Header sai: {header.text}"

        with allure.step("5. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="DemoQA_Elements_Page",
                attachment_type=allure.attachment_type.PNG
            )