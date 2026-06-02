import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

# =====================================================================
# PHẦN: UI AUTOMATION TESTING (TEST GIAO DIỆN DEMOQA TEXT BOX)
# =====================================================================
@allure.epic("Cross-Project Testing")
@allure.feature("DemoQA Text Box Form")
class TestDemoQA:

    @allure.title("TC_01: Điền thông tin và Submit thành công form Text Box")
    def test_fill_text_box(self, driver):
        target_url = "https://demoqa.com/text-box"
        wait = WebDriverWait(driver, 15)

        with allure.step(f"1. Truy cập trực tiếp vào: {target_url}"):
            driver.get(target_url)
            time.sleep(2)

        with allure.step("2. Xác minh đã vào đúng trang Text Box"):
            header = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//h1[text()='Text Box']")
            ))
            assert "Text Box" in header.text, f"Sai tiêu đề trang: {header.text}"

        with allure.step("3. Nhập dữ liệu vào các trường thông tin"):
            wait.until(EC.visibility_of_element_located((By.ID, "userName"))).send_keys("Mai Thanh Tâm")
            driver.find_element(By.ID, "userEmail").send_keys("Tam.it@example.com")
            driver.find_element(By.ID, "currentAddress").send_keys("Hà Nội")
            driver.find_element(By.ID, "permanentAddress").send_keys("Hà Nội")
            
        with allure.step("4. Cuộn xuống và Click nút Submit"):
            submit_btn = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            
            driver.execute_script("var ad = document.getElementById('fixedban'); if(ad) ad.remove();")
            driver.execute_script("var footer = document.getElementsByTagName('footer')[0]; if(footer) footer.remove();")
            driver.execute_script("arguments[0].click();", submit_btn)

        with allure.step("5. Xác minh thông tin Output hiển thị chính xác bên dưới"):
            output_box = wait.until(EC.visibility_of_element_located((By.ID, "output")))
            assert "Mai Thanh Tâm" in output_box.text, "Lỗi: Không hiển thị đúng tên!"
            assert "Tam.it@example.com" in output_box.text, "Lỗi: Không hiển thị đúng email!"
            assert "Hà Nội" in output_box.text, "Lỗi: Không hiển thị đúng địa chỉ!"

        with allure.step("6. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="DemoQA_TextBox_Success",
                attachment_type=AttachmentType.PNG
            )

    # =====================================================================
    # --------- BỔ SUNG: CÁC TEST CASE CỐ TÌNH FAIL ---------
    # =====================================================================

    @allure.title("TC_02: [CỐ TÌNH FAIL] Lỗi giao diện - Không tìm thấy phần tử")
    def test_intentional_fail_missing_element(self, driver):
        target_url = "https://demoqa.com/text-box"
        wait = WebDriverWait(driver, 5) # Set thời gian chờ ngắn để fail nhanh

        with allure.step("1. Truy cập trang Text Box"):
            driver.get(target_url)
            time.sleep(2)

        with allure.step("2. Tìm kiếm phần tử ảo để ép lỗi UI"):
            # Nút này hoàn toàn không có thật trên DemoQA, Selenium sẽ không thể tìm thấy
            fake_button = wait.until(EC.presence_of_element_located((By.ID, "nut-submit-ao-khong-ton-tai")))
            fake_button.click()

    @allure.title("TC_03: [CỐ TÌNH FAIL] Lỗi logic - Sai thông tin Output")
    def test_intentional_fail_logic_assert(self, driver):
        target_url = "https://demoqa.com/text-box"
        wait = WebDriverWait(driver, 10)

        with allure.step("1. Truy cập trang Text Box"):
            driver.get(target_url)
            time.sleep(2)

        with allure.step("2. Nhập thông tin người dùng và Submit"):
            wait.until(EC.visibility_of_element_located((By.ID, "userName"))).send_keys("Mai Thanh Tâm")
            
            submit_btn = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", submit_btn)

        with allure.step("3. Kiểm tra Output nhưng cố tình tạo Assert sai lệch"):
            output_box = wait.until(EC.visibility_of_element_located((By.ID, "output")))
            
            # Người dùng nhập "Mai Thanh Tâm", nhưng bộ test lại kỳ vọng là một người khác
            # Lệnh assert này sẽ lập tức báo lỗi Failed trên Allure Report
            assert "Trịnh Huy Hoàng" in output_box.text, "LỖI LOGIC NGHIỆP VỤ: Tên hiển thị trên Output không khớp với dữ liệu kỳ vọng!"
            
        with allure.step("4. Chụp ảnh màn hình lúc xảy ra lỗi (Sẽ không chạy tới đây do Assert đã chặn lại)"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="DemoQA_TextBox_Fail_Logic",
                attachment_type=AttachmentType.PNG
            )