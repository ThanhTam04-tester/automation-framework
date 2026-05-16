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
        target_url = "https://demoqa.com"
        # Tăng thời gian chờ lên 20s cho chắc ăn vì DemoQA dạo này thỉnh thoảng load hơi chậm
        wait = WebDriverWait(driver, 20)

        with allure.step(f"1. Truy cập vào website: {target_url}"):
            driver.get(target_url)
            time.sleep(2)  # Chờ trang load xong

        with allure.step("2. Xác minh website mở thành công"):
            banner = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "home-banner")
            ))
            assert banner.is_displayed(), "Không tìm thấy banner trang chủ DemoQA!"

        with allure.step("3. Click vào mục Elements"):
            # SỬA LỖI Ở ĐÂY: Bắt nguyên thẻ Card (div) bọc ngoài thay vì lấy chữ Elements
            elements_card = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'top-card') and .//h5[text()='Elements']]")
            ))
            
            # Cuộn khối Card vào giữa màn hình
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elements_card)
            time.sleep(1) 
            
            # Tuyệt chiêu: Xóa phần tử quảng cáo và footer hay đè lên thẻ
            driver.execute_script("var ad = document.getElementById('fixedban'); if(ad) ad.remove();")
            driver.execute_script("var footer = document.getElementsByTagName('footer')[0]; if(footer) footer.remove();")
            
            # Click thẳng vào Card bằng Javascript (mạnh nhất, bỏ qua mọi vật cản)
            driver.execute_script("arguments[0].click();", elements_card)

        with allure.step("4. Xác minh đã chuyển sang trang Elements"):
            # Chờ URL trên trình duyệt thay đổi thành "elements"
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