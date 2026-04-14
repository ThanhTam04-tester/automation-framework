import pytest
import allure
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =====================================================================
# PHẦN 1: UI AUTOMATION TESTING (TEST GIAO DIỆN)
# =====================================================================
@allure.epic("Cross-Project Testing")
@allure.feature("Google Web UI")
class TestGoogleUI:

    @allure.title("UI_01: Tìm kiếm trên Google thành công có kết quả")
    def test_google_search_basic(self, driver):
        target_url = "https://www.google.com"
        
        with allure.step(f"1. Truy cập vào {target_url}"):
            driver.get(target_url)
            time.sleep(1) 
            
        with allure.step("2. Nhập từ khóa hợp lệ và tìm kiếm"):
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys("Automation Test with Selenium and Pytest")
            search_box.send_keys(Keys.RETURN)
            time.sleep(2) 
            
        with allure.step("3. Xác minh kết quả tìm kiếm hiển thị"):
            assert "Automation Test" in driver.title
            search_results = driver.find_elements(By.ID, "search")
            assert len(search_results) > 0, "Không tìm thấy khối kết quả (ID='search')!"

    @allure.title("UI_02: Tìm kiếm từ khóa vô nghĩa (Không có kết quả)")
    def test_google_search_no_result(self, driver):
        target_url = "https://www.google.com"
        
        with allure.step(f"1. Truy cập vào {target_url}"):
            driver.get(target_url)
            time.sleep(1)
            
        with allure.step("2. Nhập chuỗi ký tự ngẫu nhiên vô nghĩa"):
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            # Gõ một chuỗi dài đảm bảo không thể có trên đời
            gibberish_text = "qwertyuioplkjhgfdsazxcvbnm1234567890xyz"
            search_box.send_keys(gibberish_text)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)
            
        with allure.step("3. Xác minh Google báo không tìm thấy tài liệu"):
            page_source = driver.page_source
            # Google thường trả về câu "không tìm thấy tài liệu nào" hoặc "did not match any documents"
            assert "không tìm thấy" in page_source.lower() or "did not match" in page_source.lower()


# =====================================================================
# PHẦN 2: API & BACKEND TESTING (TEST GIAO THỨC NGẦM)
# =====================================================================
@allure.epic("Cross-Project Testing")
@allure.feature("Google API & Performance")
class TestGoogleAPI:

    @allure.title("API_01: Ping Trang chủ Google (Đảm bảo Web không bị sập)")
    def test_google_homepage_status(self):
        target_url = "https://www.google.com"
        
        with allure.step(f"1. Gửi request GET tới {target_url}"):
            response = requests.get(target_url)
            
        with allure.step("2. Xác minh HTTP Status Code là 200 (Thành công)"):
            assert response.status_code == 200, f"Lỗi! Status code trả về là {response.status_code}"
            
        with allure.step("3. Xác minh thời gian phản hồi dưới 2 giây (Performance)"):
            # Lấy thời gian phản hồi tính bằng giây
            response_time = response.elapsed.total_seconds()
            assert response_time < 2.0, f"Trang web phản hồi quá chậm: {response_time} giây!"

    @allure.title("API_02: Test API Gợi ý từ khóa (Google Autocomplete API)")
    def test_google_autocomplete_api(self):
        # Đây là API ngầm của Google dùng để gọi ý chữ khi bạn đang gõ
        api_url = "http://suggestqueries.google.com/complete/search"
        params = {
            "client": "chrome",
            "q": "kiem thu phan mem" # Từ khóa gõ dở
        }
        
        with allure.step(f"1. Gửi request GET tới API Autocomplete với từ khóa: '{params['q']}'"):
            response = requests.get(api_url, params=params)
            
        with allure.step("2. Xác minh API phản hồi thành công và trả về dữ liệu JSON"):
            assert response.status_code == 200
            
            # Google trả về data dạng mảng (Array). VD: ["kiem thu", ["kiem thu phan mem la gi", ...]]
            data = response.json()
            assert len(data) >= 2, "Cấu trúc JSON trả về không đúng chuẩn của Google"
            
        with allure.step("3. Xác minh có chứa các từ khóa gợi ý liên quan"):
            suggestions = data[1] # Lấy mảng chứa các gợi ý
            assert len(suggestions) > 0, "Google không trả về bất kỳ gợi ý nào!"
            print(f"\n[INFO] Các gợi ý từ Google: {suggestions[:3]}...") # In thử 3 gợi ý đầu tiên ra log