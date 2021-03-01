import logging
import os
from random import random

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    netid = os.getenv("netid")
    password = os.getenv("password")
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get("http://jkrb.xjtu.edu.cn/EIP/user/index.htm")
    wait = WebDriverWait(driver=driver, timeout=30)
    wait.until((EC.url_contains("org.xjtu.edu.cn")))
    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/input[1]'))
    )
    elem.send_keys(netid)
    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/input[2]'))
    )
    elem.send_keys(password)
    elem.send_keys(Keys.ENTER)
    wait.until(EC.url_contains("jkrb.xjtu.edu.cn"))
    logger.info("Successful Login")

    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload2()']")
    driver.switch_to.frame(iframe)

    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload1()']")
    driver.switch_to.frame(iframe)
    elem = driver.find_element_by_xpath("//div[@title='本科生每日健康状况填报']")
    elem.click()

    driver.implicitly_wait(1)
    driver.switch_to.default_content()
    driver.implicitly_wait(1)
    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload3()']")
    driver.switch_to.frame(iframe)
    elem = driver.find_element_by_xpath("//li[@data-blname='每日健康填报']")
    elem.click()
    driver.implicitly_wait(1)
    driver.switch_to.default_content()
    driver.implicitly_wait(5)
    try:
        iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload4()']")
        driver.switch_to.frame(iframe)
        iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload1()']")
        driver.switch_to.frame(iframe)

        # check travel history
        driver.find_element_by_xpath("//*[@id='mini-3$ck$1']").click()

        temp = str(round(36 + random(), 1))
        driver.find_element_by_xpath(
            "//input[@placeholder='请准确填写体温，格式如:36.5']"
        ).send_keys(temp)
        logger.info(f"Today's body temp. is {temp}")

        driver.switch_to.default_content()
        driver.implicitly_wait(1)
        iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload4()']")
        driver.switch_to.frame(iframe)
        submit_btn = driver.find_element_by_xpath("//a[@id='sendBtn']")
        submit_btn.click()
        elem = driver.find_element_by_xpath("//*[@id='mini-17']")
        elem.click()
        try:
            driver.switch_to.default_content()
            driver.implicitly_wait(1)
            iframe = driver.find_element_by_xpath(
                "//iframe[@onload='__iframe_onload4()']"
            )
            driver.switch_to.frame(iframe)
            elem = driver.find_element_by_xpath("//*[@id='mini-19$content']")
            logger.info(elem.text)
        except NoSuchElementException:
            logger.info("Successful submit!")

    except NoSuchElementException:
        driver.switch_to.default_content()
        iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload5()']")
        driver.switch_to.frame(iframe)
        elem = driver.find_element_by_xpath("//*[@id='messageId']")
        logger.info("You've already checked in.")
        logger.info(elem.text)


if __name__ == "__main__":
    main()
