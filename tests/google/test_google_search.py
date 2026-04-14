import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.epic("Cross-Project Testing")
@allure.feature("Google Search Engine")
class TestGoogle:

    @allure.title("TC_01: Tìm kiếm trên Google thành công")
    def test_google_search_basic(self, driver):
        # 1. Bỏ qua config base_url của Hotel, đi thẳng tới Google
        target_url = "https://www.google.com"
        
        with allure.step(f"Truy cập vào {target_url}"):
            driver.get(target_url)
            time.sleep(2) # Chờ load trang
            
        with allure.step("Nhập từ khóa và tìm kiếm"):
            # Ô tìm kiếm của Google luôn có name="q"
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys("Automation Test with Selenium and Pytest")
            search_box.send_keys(Keys.RETURN) # Bấm Enter
            time.sleep(3) # Chờ kết quả tải về
            
        with allure.step("Xác minh kết quả tìm kiếm"):
            # Kiểm tra tiêu đề tab trình duyệt có chứa chữ "Automation Test" không
            assert "Automation Test" in driver.title
            
            # Kiểm tra xem có khối kết quả tìm kiếm (id="search") xuất hiện không
            search_results = driver.find_elements(By.ID, "search")
            assert len(search_results) > 0, "Không tìm thấy kết quả nào!"