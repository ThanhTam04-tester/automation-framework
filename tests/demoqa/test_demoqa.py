import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.epic("DemoQA Automation Project")
@allure.feature("Elements - Text Box")
class TestDemoQATextBox:

    @allure.title("TC_01: Điền và submit form Text Box thành công")
    def test_text_box_submit(self, driver, config):
        target_url = f"{config['base_url']}/text-box"

        with allure.step(f"1. Truy cập trang Text Box: {target_url}"):
            driver.get(target_url)
            time.sleep(1)

        with allure.step("2. Nhập thông tin vào các trường"):
            driver.find_element(By.ID, "userName").send_keys("Nguyen Van A")
            driver.find_element(By.ID, "userEmail").send_keys("nguyenvana@example.com")
            driver.find_element(By.ID, "currentAddress").send_keys("123 Duong ABC, Ha Noi")
            driver.find_element(By.ID, "permanentAddress").send_keys("456 Duong XYZ, Ho Chi Minh")

        with allure.step("3. Click nút Submit"):
            driver.find_element(By.ID, "submit").click()
            time.sleep(1)

        with allure.step("4. Xác minh thông tin hiển thị đúng trong output"):
            output = driver.find_element(By.ID, "output")
            assert output.is_displayed(), "Không hiển thị kết quả sau khi submit!"

            output_text = output.text
            assert "Nguyen Van A" in output_text, "Tên không khớp trong output!"
            assert "nguyenvana@example.com" in output_text, "Email không khớp trong output!"

        with allure.step("5. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="TextBox_Submit_Result",
                attachment_type=allure.attachment_type.PNG
            )


@allure.epic("DemoQA Automation Project")
@allure.feature("Elements - Check Box")
class TestDemoQACheckBox:

    @allure.title("TC_02: Chọn checkbox Home và xác minh các mục con được chọn")
    def test_checkbox_select_home(self, driver, config):
        target_url = f"{config['base_url']}/checkbox"

        with allure.step(f"1. Truy cập trang Check Box: {target_url}"):
            driver.get(target_url)
            time.sleep(1)

        with allure.step("2. Expand toàn bộ cây checkbox"):
            expand_btn = driver.find_element(By.CSS_SELECTOR, "button[title='Expand all']")
            expand_btn.click()
            time.sleep(1)

        with allure.step("3. Click chọn checkbox Home (root)"):
            home_checkbox = driver.find_element(By.CSS_SELECTOR, "label[for='tree-node-home'] span.rct-checkbox")
            home_checkbox.click()
            time.sleep(1)

        with allure.step("4. Xác minh kết quả hiển thị các mục đã chọn"):
            result = driver.find_element(By.ID, "result")
            assert result.is_displayed(), "Không có kết quả hiển thị!"
            result_text = result.text.lower()
            assert "home" in result_text, "Mục 'home' không xuất hiện trong kết quả!"

        with allure.step("5. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="CheckBox_Home_Selected",
                attachment_type=allure.attachment_type.PNG
            )


@allure.epic("DemoQA Automation Project")
@allure.feature("Elements - Radio Button")
class TestDemoQARadioButton:

    @allure.title("TC_03: Chọn Radio Button 'Yes' và xác minh kết quả")
    def test_radio_button_yes(self, driver, config):
        target_url = f"{config['base_url']}/radio-button"

        with allure.step(f"1. Truy cập trang Radio Button: {target_url}"):
            driver.get(target_url)
            time.sleep(1)

        with allure.step("2. Click chọn Radio Button 'Yes'"):
            yes_label = driver.find_element(By.CSS_SELECTOR, "label[for='yesRadio']")
            yes_label.click()
            time.sleep(1)

        with allure.step("3. Xác minh text kết quả hiển thị 'Yes'"):
            success_text = driver.find_element(By.CSS_SELECTOR, "p.mt-3 span.text-success")
            assert success_text.text == "Yes", f"Kết quả không đúng: {success_text.text}"

        with allure.step("4. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="RadioButton_Yes_Selected",
                attachment_type=allure.attachment_type.PNG
            )

    @allure.title("TC_04: Chọn Radio Button 'Impressive' và xác minh kết quả")
    def test_radio_button_impressive(self, driver, config):
        target_url = f"{config['base_url']}/radio-button"

        with allure.step(f"1. Truy cập trang Radio Button: {target_url}"):
            driver.get(target_url)
            time.sleep(1)

        with allure.step("2. Click chọn Radio Button 'Impressive'"):
            impressive_label = driver.find_element(By.CSS_SELECTOR, "label[for='impressiveRadio']")
            impressive_label.click()
            time.sleep(1)

        with allure.step("3. Xác minh text kết quả hiển thị 'Impressive'"):
            success_text = driver.find_element(By.CSS_SELECTOR, "p.mt-3 span.text-success")
            assert success_text.text == "Impressive", f"Kết quả không đúng: {success_text.text}"

        with allure.step("4. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="RadioButton_Impressive_Selected",
                attachment_type=allure.attachment_type.PNG
            )


@allure.epic("DemoQA Automation Project")
@allure.feature("Elements - Web Tables")
class TestDemoQAWebTables:

    @allure.title("TC_05: Thêm một bản ghi mới vào Web Tables")
    def test_web_tables_add_record(self, driver, config):
        target_url = f"{config['base_url']}/webtables"

        with allure.step(f"1. Truy cập trang Web Tables: {target_url}"):
            driver.get(target_url)
            time.sleep(1)

        with allure.step("2. Click nút 'Add' để mở form thêm mới"):
            driver.find_element(By.ID, "addNewRecordButton").click()
            time.sleep(1)

        with allure.step("3. Điền thông tin vào form"):
            driver.find_element(By.ID, "firstName").send_keys("Tran")
            driver.find_element(By.ID, "lastName").send_keys("Van B")
            driver.find_element(By.ID, "userEmail").send_keys("tranvanb@example.com")
            driver.find_element(By.ID, "age").send_keys("28")
            driver.find_element(By.ID, "salary").send_keys("50000")
            driver.find_element(By.ID, "department").send_keys("QA")

        with allure.step("4. Submit form"):
            driver.find_element(By.ID, "submit").click()
            time.sleep(1)

        with allure.step("5. Xác minh bản ghi mới xuất hiện trong bảng"):
            table_content = driver.find_element(By.CLASS_NAME, "rt-tbody").text
            assert "Tran" in table_content, "Không tìm thấy bản ghi mới trong bảng!"
            assert "tranvanb@example.com" in table_content, "Email không khớp trong bảng!"

        with allure.step("6. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="WebTables_New_Record",
                attachment_type=allure.attachment_type.PNG
            )


@allure.epic("DemoQA Automation Project")
@allure.feature("Widgets - Date Picker")
class TestDemoQADatePicker:

    @allure.title("TC_06: Xác minh Date Picker mở ra và chọn ngày thành công")
    def test_date_picker_open(self, driver, config):
        target_url = f"{config['base_url']}/date-picker"

        with allure.step(f"1. Truy cập trang Date Picker: {target_url}"):
            driver.get(target_url)
            time.sleep(1)

        with allure.step("2. Click vào ô nhập ngày để mở date picker"):
            date_input = driver.find_element(By.ID, "datePickerMonthYearInput")
            date_input.clear()
            date_input.send_keys("05/20/2025")
            date_input.send_keys("\n")
            time.sleep(1)

        with allure.step("3. Xác minh giá trị ngày đã được nhập đúng"):
            value = date_input.get_attribute("value")
            assert "05/20/2025" in value, f"Giá trị ngày không đúng: {value}"

        with allure.step("4. Chụp ảnh màn hình minh chứng"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="DatePicker_Selected",
                attachment_type=allure.attachment_type.PNG
            )
