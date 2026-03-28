import pytest
from core.config_loader import load_config
from core.logger import get_logger
from core.api_client import APIClient
from core.driver_factory import create_driver

logger = get_logger("tests")


# load config
@pytest.fixture(scope="session")
def config():
    return load_config()


# API client
@pytest.fixture(scope="session")
def api_client(config):
    return APIClient(
        base_url=config["api_url"],
        timeout=config.get("timeout", 10)
    )


# UI driver
@pytest.fixture(scope="function")
def driver():
    driver = create_driver()
    yield driver
    driver.quit()


# log test start/end
def pytest_runtest_logstart(nodeid, location):
    logger.info(f"[TEST START] {nodeid}")


def pytest_runtest_logfinish(nodeid, location):
    logger.info(f"[TEST END] {nodeid}")