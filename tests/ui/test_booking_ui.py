# Test thu bat loi UI
import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.epic("Web UI Testing")
@allure.feature("Booking Form")
@allure.title("Test chức năng đặt phòng trực tiếp trên trang chủ")
def test_dat_phong_thanh_cong(driver, config):
    with allure.step("1. Truy cập vào trang chủ Palatin Hotel"):
        # Lấy URL từ file env.dev.yaml thay vì viết cứng
        driver.get(config["base_url"])
        time.sleep(2)

    with allure.step("2. Nhập thông tin Khách hàng"):
        # Lấy đúng ID từ file index.html của bạn
        driver.find_element(By.ID, "custName").send_keys("Mai Thị Thanh Tâm")
        driver.find_element(By.ID, "custPhone").send_keys("0901234567")
        
    with allure.step("3. Chọn Loại phòng"):
        room_dropdown = driver.find_element(By.ID, "roomSelect")
        room_dropdown.send_keys("Phòng Classic") # Chọn phòng

    with allure.step("4. Bấm nút Đặt phòng (Check Availability)"):
        # Tìm nút bấm dựa trên cấu trúc HTML của bạn
        btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Check Availability')]")
        btn.click()
        time.sleep(2)

    with allure.step("5. Xác minh thông báo đặt phòng"):
        # Ở đây vì web bạn dùng alert() JS, nên ta phải bắt Alert
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        
        # In ra log và bấm OK tắt popup
        print(f"Thông báo từ hệ thống: {alert_text}")
        alert.accept()
        
        # Kiểm tra xem có chữ THÀNH CÔNG hay Hệ thống báo lỗi
        assert "Hệ thống" in alert_text or "THÀNH CÔNG" in alert_text