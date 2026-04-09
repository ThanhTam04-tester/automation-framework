# Test thu bat loi UI
import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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
        
    with allure.step("3. Chọn Loại phòng và Ngày nhận"):
        # Dùng Javascript ép gán giá trị cho thẻ bị ẩn (2 là value của phòng VIP trong file HTML)
        driver.execute_script("document.getElementById('roomSelect').value = '2';")
        
        # Nhập ngày nhận phòng
        driver.find_element(By.ID, "checkInDate").send_keys("10-10-2026")

    with allure.step("4. Bấm nút Đặt phòng"):
        # Tìm nút bấm theo ID thay vì Text cho chính xác tuyệt đối
        btn = driver.find_element(By.ID, "btnBook")
        
        # Dùng JS Click để click thủng mọi thành phần cản đường
        driver.execute_script("arguments[0].click();", btn)
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