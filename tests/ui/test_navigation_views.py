import pytest
import allure
import time
from selenium.webdriver.common.by import By

@allure.epic("UI Automation Testing")
@allure.feature("Navigation & Views")
class TestNavigation:

    @allure.title("TC_08: Kiểm tra điều hướng sang trang Danh Sách Phòng")
    def test_nav_to_rooms(self, driver, config):
        driver.get(config["base_url"])
        with allure.step("Click vào menu Phòng"):
            # Tìm link có href chứa 'rooms'
            nav_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Phòng')]")
            driver.execute_script("arguments[0].click();", nav_link)
            time.sleep(1)
        with allure.step("Xác minh URL trang Phòng"):
            assert "rooms" in driver.current_url

    @allure.title("TC_09: Kiểm tra điều hướng sang trang Liên Hệ")
    def test_nav_to_contact(self, driver, config):
        driver.get(config["base_url"])
        nav_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Liên Hệ')]")
        driver.execute_script("arguments[0].click();", nav_link)
        time.sleep(1)
        assert "contact" in driver.current_url

    @allure.title("TC_10: Kiểm tra hiển thị giá phòng trên trang chủ")
    def test_check_room_prices(self, driver, config):
        driver.get(config["base_url"])
        page_source = driver.page_source
        with allure.step("Xác minh các mức giá được hiển thị đầy đủ"):
            assert "500,000 VNĐ" in page_source
            assert "1,200,000 VNĐ" in page_source
            assert "850,000 VNĐ" in page_source

    @allure.title("TC_11: Kiểm tra trang Lịch sử Đặt phòng (My Bookings)")
    def test_my_bookings_table(self, driver, config):
        # Mở trang my_bookings
        driver.get(config["base_url"] + "/my_bookings")
        with allure.step("Xác minh bảng danh sách đơn hàng tồn tại"):
            # Kiểm tra xem table có class 'table-bordered' tồn tại không
            table = driver.find_elements(By.CSS_SELECTOR, "table.table-bordered")
            assert len(table) > 0, "Không tìm thấy bảng danh sách đặt phòng!"