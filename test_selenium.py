import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

driver.get('https://raydium.io/swap')
time.sleep(2)
driver.find_element(by=By.CSS_SELECTOR, value="#__layout > section > main > div > div.page-head.fs-container > div > i.anticon.anticon-search").click()

time.sleep(1)

search_field = driver.find_element(by=By.CSS_SELECTOR, value="div.ant-modal-content > div.ant-modal-body > div > input")

time.sleep(1)

search_field.send_keys("3mYsmBQLB8EZSjRwtWjPbbE8LiM1oCCtNZZKiVBKsePa")

time.sleep(1)

driver.find_element(by=By.CSS_SELECTOR, value="div.ant-modal-content > div.ant-modal-body > div > div > div:nth-child(1) > button").click()

time.sleep(1)

driver.find_element(by=By.CSS_SELECTOR, value="#__layout > section > main > div > div.page-head.fs-container > div > i.anticon.anticon-info-circle").click()

time.sleep(1)

token_element = driver.find_element(by=By.CSS_SELECTOR, value="div.ant-tooltip-content > div.ant-tooltip-inner > div > div:nth-child(1) > div.action > a")
solscan_link = token_element.get_attribute('href')

print(solscan_link)
