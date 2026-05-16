import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

# =====================================================================
# PHẦN: UI AUTOMATION TESTING (TEST GIAO DIỆN DEMOQA)
# =====================================================================
@allure.epic("Cross-Project Testing")
@allure.feature("DemoQA Practice Form")
class TestDemoQA:

    @allure.title("TC_01: Truy cập thành công trang DemoQA")
    def test_open_demoqa(self, driver):
        # Gán thẳng URL trực tiếp để không bị nhầm
        target_url = "https://demoqa.com"
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
            # SỬA LỖI Ở ĐÂY: Nhắm thẳng vào chữ Elements thay vì thẻ div bọc ngoài
            elements_text = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//h5[text()='Elements']")
            ))
            
            # Cuộn phần tử vào giữa màn hình
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elements_text)
            time.sleep(1) 
            
            # Tuyệt chiêu trị DemoQA: Xóa phần tử quảng cáo / footer hay đè lên nút bấm
            driver.execute_script("var ad = document.getElementById('fixedban'); if(ad) ad.remove();")
            driver.execute_script("var footer = document.getElementsByTagName('footer')[0]; if(footer) footer.remove();")
            
            # Ưu tiên click bằng Selenium chuẩn, nếu fail mới dùng JS backup
            try:
                elements_text.click()
            except:
                driver.execute_script("arguments[0].click();", elements_text)

        with allure.step("4. Xác minh đã chuyển sang trang Elements"):
            # Bắt buộc chờ URL trên trình duyệt thay đổi thành "elements" rồi mới check
            wait.until(EC.url_contains("elements"))
            
            header = wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, "main-header")
            ))
            assert "elements" in driver.current_url, f"URL sai: {driver.current_url}"
            assert header.text == "Elements", f"Header sai: {header.text}"

        with allure.step("5. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="DemoQA_Elements_Page",
                attachment_type=AttachmentType.PNG
            )