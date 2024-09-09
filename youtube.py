from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

navegador = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

navegador.implicitly_wait(20) # seconds
navegador.maximize_window()
navegador.get("https://www.youtube.com/@lopesrio")

inscritosYoutube = navegador.find_element(By.XPATH, '//*[@id="page-header"]/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-content-metadata-view-model/div[2]/span[1]').text

print(inscritosYoutube)

navegador.close()