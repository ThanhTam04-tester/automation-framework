from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Thêm 2 dòng này để trình duyệt chạy ẩn
chrome_options = Options()
chrome_options.add_argument("--headless=new") 

# Khi khởi tạo driver thì nhét cái options vào
driver = webdriver.Chrome(options=chrome_options)