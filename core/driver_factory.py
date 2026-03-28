from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from core.config_loader import get_config
from core.logger import get_logger

logger = get_logger("driver_factory")


def create_driver():
    config = get_config()

    browser = config.get("browser", "chrome").lower()
    headless = config.get("headless", False)

    logger.info(f"Start browser: {browser} | headless={headless}")

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )

    else:
        raise Exception(f"Browser not supported: {browser}")

    driver.maximize_window()
    return driver