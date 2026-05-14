import pytest
import allure
import time

from selenium.webdriver.common.by import By

@allure.epic("Cross-Project Testing")
@allure.feature("DemoQA Practice Form")

class TestDemoQA:

    @allure.title("TC_01: Truy cập thành công trang DemoQA")

    def test_open_demoqa(self, driver):

        target_url = "https://demoqa.com/"

        with allure.step(f"1. Truy cập website: {target_url}"):

            driver.get(target_url)
            time.sleep(2)

        with allure.step("2. Xác minh website mở thành công"):

            # Kiểm tra URL hiện tại
            assert "demoqa.com" in driver.current_url

            # Kiểm tra logo/trang chủ tồn tại
            logo = driver.find_elements(By.CLASS_NAME, "home-banner")

            assert len(logo) > 0, "Không tìm thấy banner trang chủ DemoQA!"

        with allure.step("3. Click vào mục Elements"):

            elements_card = driver.find_element(
                By.XPATH,
                "//h5[text()='Elements']"
            )

            # Scroll tới element
            driver.execute_script(
                "arguments[0].scrollIntoView();",
                elements_card
            )

            time.sleep(1)

            # Click bằng JavaScript
            driver.execute_script(
                "arguments[0].click();",
                elements_card
            )

            time.sleep(2)

        with allure.step("4. Xác minh đã chuyển sang trang Elements"):

            assert "elements" in driver.current_url

            header = driver.find_element(
                By.CLASS_NAME,
                "main-header"
            )

            assert header.text == "Elements"

        with allure.step("5. Chụp ảnh màn hình minh chứng"):

            allure.attach(
                driver.get_screenshot_as_png(),
                name="DemoQA_Elements_Page",
                attachment_type=allure.attachment_type.PNG
            )