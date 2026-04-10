import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.epic("UI Automation Testing")
@allure.feature("Room Booking")
class TestBooking:

    @allure.title("TC_04: Đặt phòng thành công (Điền đầy đủ thông tin)")
    def test_booking_happy_path(self, driver, config):
        driver.get(config["base_url"])
        with allure.step("Điền thông tin và ngày nhận"):
            driver.find_element(By.ID, "custName").send_keys("Khách Hàng VIP")
            driver.find_element(By.ID, "custPhone").send_keys("0988888888")
            driver.execute_script("document.getElementById('roomSelect').value = '2';") # Phòng VIP
            driver.find_element(By.ID, "checkInDate").send_keys("20-10-2026")
            
        with allure.step("Bấm nút Đặt Phòng"):
            btn = driver.find_element(By.ID, "btnBook")
            driver.execute_script("arguments[0].click();", btn)
            
        with allure.step("Xác minh Alert THÀNH CÔNG"):
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            assert "THÀNH CÔNG" in alert.text
            alert.accept()

    @allure.title("TC_05: Đặt phòng thất bại (Bỏ trống Tên)")
    def test_booking_empty_name(self, driver, config):
        driver.get(config["base_url"])
        # Cố tình không điền custName
        driver.find_element(By.ID, "custPhone").send_keys("0988888888")
        driver.execute_script("document.getElementById('roomSelect').value = '1';")
        
        btn = driver.find_element(By.ID, "btnBook")
        driver.execute_script("arguments[0].click();", btn)
        
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        assert "Vui lòng điền đủ" in alert.text
        alert.accept()

    @allure.title("TC_06: Đặt phòng thất bại (Bỏ trống SĐT)")
    def test_booking_empty_phone(self, driver, config):
        driver.get(config["base_url"])
        driver.find_element(By.ID, "custName").send_keys("Khách Hàng")
        # Cố tình không điền custPhone
        driver.execute_script("document.getElementById('roomSelect').value = '3';")
        
        btn = driver.find_element(By.ID, "btnBook")
        driver.execute_script("arguments[0].click();", btn)
        
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        assert "Vui lòng điền đủ" in alert.text
        alert.accept()

    @allure.title("TC_07: Đặt phòng thất bại (Bỏ trống Chọn phòng)")
    def test_booking_empty_room(self, driver, config):
        driver.get(config["base_url"])
        driver.find_element(By.ID, "custName").send_keys("Khách Hàng")
        driver.find_element(By.ID, "custPhone").send_keys("0988888888")
        # Gán value rỗng cho roomSelect
        driver.execute_script("document.getElementById('roomSelect').value = '';")
        
        btn = driver.find_element(By.ID, "btnBook")
        driver.execute_script("arguments[0].click();", btn)
        
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        assert "Vui lòng điền đủ" in alert.text
        alert.accept()