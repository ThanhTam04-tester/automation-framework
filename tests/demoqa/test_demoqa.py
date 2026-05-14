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
    def test_open_demoqa(self, driver):

        target_url = "https://demoqa.com/"

        with allure.step(f"1. Truy cập website: {target_url}"):

            driver.get(target_url)

        with allure.step("2. Xác minh website mở thành công"):

            # Kiểm tra URL hiện tại
            assert "demoqa.com" in driver.current_url

            # Kiểm tra banner trang chủ tồn tại
            logo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "home-banner")
                )
            )

            assert logo.is_displayed()

        with allure.step("3. Click vào mục Elements"):

            elements_card = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h5[text()='Elements']")
                )
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

        with allure.step("4. Xác minh đã chuyển sang trang Elements"):

            # Đợi header xuất hiện
            header = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "main-header")
                )
            )

            assert "elements" in driver.current_url
            assert header.text == "Elements"

        with allure.step("5. Chụp ảnh màn hình minh chứng"):

            allure.attach(
                driver.get_screenshot_as_png(),
                name="DemoQA_Elements_Page",
                attachment_type=allure.attachment_type.PNG
            )