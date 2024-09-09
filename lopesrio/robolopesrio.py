# from selenium.webdriver.support.ui import Select

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# time.sleep(18000)

navegador = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

navegador.implicitly_wait(20) # seconds
navegador.get('https://lopesrio.com.br/login/')

time.sleep(2)
navegador.find_element(By.XPATH, '//*[@id="user_login"]').send_keys("helder")
navegador.find_element(By.XPATH, '//*[@id="user_pass"]').send_keys("oW^afn)2QkME!fwX)PA@3xkp")
navegador.find_element(By.ID, 'wp-submit').click()

# time.sleep(5)
# navegador.find_element(By.XPATH, '//*[@id="user_pass"]').send_keys("oW^afn)2QkME!fwX)PA@3xkp")
# navegador.find_element(By.ID, 'wp-submit').click()

navegador.get('https://lopesrio.com.br/wp-admin/admin.php?page=pmxi-admin-manage')

navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/form[2]/table/tbody/tr[1]/td[2]/h2/a').click()

# iniciar importação
navegador.find_element(By.ID, 'wpai-submit-confirm-form').click()

time.sleep(5)
navegador.close()
