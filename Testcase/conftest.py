import time

import pytest
from selenium import webdriver

from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def login():
    driver=webdriver.Chrome()
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("http://192.168.10.164:8420/#/login")
    driver.find_elements_by_css_selector("div[class='el-form-item__content']>div>input")[0].send_keys("liyuexuan")
    # driver.get("http://192.168.10.182:8000//#/login")
    # driver.find_elements_by_css_selector("div[class='el-form-item__content']>div>input")[0].send_keys("liyuexuan")
    driver.find_elements_by_css_selector("div[class='el-form-item__content']>div>input")[1].send_keys("Xinda123")
    driver.find_element_by_css_selector("form>button").click()
    driver.__setattr__("get-date","_0901")
    driver.__setattr__("value","_1")
    yield(driver)
    driver.quit()
    print("============关闭浏览器================")
