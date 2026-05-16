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
        # Đánh thẳng vào URL của trang Text Box, bỏ qua trang chủ
        target_url = "https://demoqa.com/text-box"
        wait = WebDriverWait(driver, 15)

        with allure.step(f"1. Truy cập trực tiếp vào: {target_url}"):
            driver.get(target_url)
            time.sleep(2)  # Chờ các thành phần form load lên

        with allure.step("2. Xác minh đã vào đúng trang Text Box"):
            header = wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, "main-header")
            ))
            assert header.text == "Text Box", f"Sai tiêu đề trang: {header.text}"

        with allure.step("3. Nhập dữ liệu vào các trường thông tin"):
            # Tìm và điền thông tin vào các ô input
            wait.until(EC.visibility_of_element_located((By.ID, "userName"))).send_keys("Trịnh Huy Hoàng")
            driver.find_element(By.ID, "userEmail").send_keys("hoang.it@example.com")
            driver.find_element(By.ID, "currentAddress").send_keys("Thủ Dầu Một, Bình Dương")
            driver.find_element(By.ID, "permanentAddress").send_keys("Đồng Nai")
            
        with allure.step("4. Cuộn xuống và Click nút Submit"):
            submit_btn = driver.find_element(By.ID, "submit")
            
            # Cuộn trang xuống để nút Submit hiện ra giữa màn hình
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            
            # Xóa các banner quảng cáo hoặc footer chặn nút (rất quan trọng trên DemoQA)
            driver.execute_script("var ad = document.getElementById('fixedban'); if(ad) ad.remove();")
            driver.execute_script("var footer = document.getElementsByTagName('footer')[0]; if(footer) footer.remove();")
            
            # Ưu tiên click JS để đảm bảo ăn 100%
            driver.execute_script("arguments[0].click();", submit_btn)

        with allure.step("5. Xác minh thông tin Output hiển thị chính xác bên dưới"):
            # Sau khi submit, một div có id="output" sẽ xuất hiện
            output_box = wait.until(EC.visibility_of_element_located((By.ID, "output")))
            
            # Kiểm tra xem dữ liệu in ra có chứa thông tin mình vừa nhập không
            assert "Trịnh Huy Hoàng" in output_box.text, "Lỗi: Không hiển thị đúng tên!"
            assert "hoang.it@example.com" in output_box.text, "Lỗi: Không hiển thị đúng email!"
            assert "Thủ Dầu Một" in output_box.text, "Lỗi: Không hiển thị đúng địa chỉ!"

        with allure.step("6. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="DemoQA_TextBox_Success",
                attachment_type=AttachmentType.PNG
            )