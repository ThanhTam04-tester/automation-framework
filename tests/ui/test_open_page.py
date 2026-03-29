from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless=new")
# THÊM 2 DÒNG DƯỚI ĐÂY VÀO:
chrome_options.add_argument("--no-sandbox") # Bắt buộc phải có khi chạy trong Docker/Linux
chrome_options.add_argument("--disable-dev-shm-usage") # Giúp Chrome không bị tràn RAM ảo

driver = webdriver.Chrome(options=chrome_options)