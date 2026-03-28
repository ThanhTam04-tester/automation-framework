import pytest
from selenium.webdriver.common.by import By

@pytest.mark.ui
def test_login(driver):
    driver.get("http://127.0.0.1:5000/login")

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.TAG_NAME, "button").click()

    assert "users" in driver.current_url