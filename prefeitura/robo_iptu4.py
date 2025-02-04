# from selenium.webdriver.support.ui import Select

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image
import pytesseract
import pandas as pd

caminho = r"C:\Users\hconstancio\AppData\Local\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = caminho + r'\tesseract.exe'

navegador = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

# Função para obter o texto do CAPTCHA
def getTextoCaptcha():
    time.sleep(3)  # Aguardar o carregamento do CAPTCHA
    captcha = navegador.find_element(By.XPATH, '//*[@id="img"]')
    captcha.screenshot("captcha.png")  # Salva o CAPTCHA como imagem
    imagem = Image.open("captcha.png")
    texto_captcha = pytesseract.image_to_string(imagem).strip()  # Processa a imagem
    return texto_captcha

# Inicializar o navegador
# navegador = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

navegador.implicitly_wait(20)  # Tempo máximo para encontrar elementos
navegador.get('https://www2.rio.rj.gov.br/smf/iptulogradouro/')

print("Aguardando 10 segundos!")
time.sleep(10)

# Carregar o arquivo Excel com os códigos
# planilha = 'iptu'
# codigos = pd.read_excel(f'{planilha}.xlsx')
# codigos = codigos.dropna(subset=['cl'])  # Remove valores NaN
# codigos = codigos['cl'].tolist()  # Converte para lista

codigos = [
    206417, 206425, 207589, 207597, 207605, 207613, 207621, 110684, 110692
]

# Lista para armazenar os dados coletados
todos_os_dados = []

# def dadosCodigo():
#     # Capturar o valor pesquisado e o exercício
#     pesquisado = navegador.find_element(By.XPATH, "//tr[2]/td[1]").text.strip()
#     exercicio = navegador.find_element(By.XPATH, "//tr[2]/td[2]").text.strip()

#     # Capturar todas as linhas de logradouros
#     linhas = navegador.find_elements(By.XPATH, "//tr[@class='linha']")

#     for linha in linhas:
#         try:
#             codigo_logradouro = linha.find_element(By.XPATH, "./td[2]").text.strip()
#             logradouro = linha.find_element(By.XPATH, "./td[3]").text.strip()
#             bairro = linha.find_element(By.XPATH, "./td[4]").text.strip()
#             todos_os_dados.append({
#                 "Pesquisado": pesquisado,
#                 "Exercício": exercicio,
#                 "CódigoLogradouro": codigo_logradouro,
#                 "Logradouro": logradouro,
#                 "Bairro": bairro
#             })
#         except Exception as e:
#             print("Erro ao processar linha:", str(e))


def dadosCodigo():
    # Clicar no botão para abrir a tabela detalhada
    try:
        navegador.find_element(By.XPATH, '/html/body/div[1]/div/center/div/table/tbody/tr[4]/td[1]/input').click()
        time.sleep(3)  # Aguardar o carregamento da nova tabela
    except Exception as e:
        print("Erro ao clicar no botão da tabela detalhada:", str(e))
        return

    # Capturar informações do cabeçalho da tabela
    try:
        logradouro = navegador.find_element(By.XPATH, "//table/tbody/tr[2]/td[1]/b").text.strip()
        codigo_logradouro = navegador.find_element(By.XPATH, "//table/tbody/tr[2]/td[2]").text.strip()
        exercicio = navegador.find_element(By.XPATH, "//table/tbody/tr[2]/td[3]").text.strip()
    except Exception as e:
        print("Erro ao capturar cabeçalho da tabela:", str(e))
        return

    # Capturar as linhas de dados na tabela
    try:
        linhas = navegador.find_elements(By.XPATH, "//table/tbody/tr[position() > 3]")  # Ignorar cabeçalhos e linha do título

        for linha in linhas:
            try:
                trecho = linha.find_element(By.XPATH, "./td[1]").text.strip()
                impar = linha.find_element(By.XPATH, "./td[2]").text.strip()
                par = linha.find_element(By.XPATH, "./td[3]").text.strip()
                bairro = linha.find_element(By.XPATH, "./td[4]").text.strip()
                vap = linha.find_element(By.XPATH, "./td[5]").text.strip()
                vca = linha.find_element(By.XPATH, "./td[6]").text.strip()
                vij = linha.find_element(By.XPATH, "./td[7]").text.strip()
                vsc = linha.find_element(By.XPATH, "./td[8]").text.strip()
                vo = linha.find_element(By.XPATH, "./td[9]").text.strip()

                # Adicionar os dados coletados à lista global
                todos_os_dados.append({
                    "Logradouro": logradouro,
                    "Código do Logradouro": codigo_logradouro,
                    "Exercício": exercicio,
                    "Trecho": trecho,
                    "Ímpar (ini-fim)": impar,
                    "Par (ini-fim)": par,
                    "Bairro": bairro,
                    "Vap": vap,
                    "Vca": vca,
                    "Vij": vij,
                    "Vsc": vsc,
                    "Vo": vo
                })
            except Exception as e:
                print("Erro ao processar linha da tabela detalhada:", str(e))

    except Exception as e:
        print("Erro ao capturar as linhas da tabela detalhada:", str(e))




# Iterar sobre os códigos
for codigo in codigos:
    # time.sleep(5)
    # navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/form/table/tbody/tr[3]/td[1]/input').send_keys(codigo)

    # while True:  # Loop para resolver o CAPTCHA até ser aprovado
    #     try:
    #         captcha = getTextoCaptcha()
    #         navegador.find_element(By.XPATH, '//*[@id="texto_imagem"]').send_keys(captcha)
    #         navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/form/table/tbody/tr[5]/td/input').click()
            
    #         # Verificar se a página foi carregada corretamente
    #         time.sleep(3)
    #         if navegador.find_elements(By.XPATH, "//tr[2]/td[1]"):
    #             break  # CAPTCHA aprovado, sair do loop
    #     except:
    #         print("CAPTCHA incorreto, tentando novamente...")
    #         navegador.refresh()  # Recarregar a página e tentar novamente


    while True:  # Loop para resolver o CAPTCHA até ser aprovado
        try:
            time.sleep(5)
            navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/form/table/tbody/tr[3]/td[1]/input').send_keys(codigo)
            captcha = getTextoCaptcha()
            navegador.find_element(By.XPATH, '//*[@id="texto_imagem"]').send_keys(captcha)
            navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/form/table/tbody/tr[5]/td/input').click()
            
            # Verificar se a mensagem "Código digitado não confere!" aparece
            time.sleep(3)
            mensagem_erro = navegador.find_elements(By.XPATH, '/html/body/div[1]/div/center/div/table[1]/tbody/tr[3]/td/font[1]/b')
            if mensagem_erro and "Código digitado não confere! Favor refazer a consulta!" in mensagem_erro[0].text:
                print("Mensagem de erro detectada: Código digitado não confere. Tentando novamente...")
                navegador.find_element(By.XPATH, '/html/body/div[1]/div/center/div/table[2]/tbody/tr/td/div/form/input').click()
                time.sleep(3)  # Tempo para recarregar a página e tentar novamente
                continue  # Recomeça o loop para tentar novamente com o mesmo código
            
            # Verificar se a página foi carregada corretamente
            if navegador.find_elements(By.XPATH, "//tr[2]/td[1]"):
                break  # CAPTCHA aprovado, sair do loop
        except Exception as e:
            print("Erro ao resolver CAPTCHA ou consultar:", str(e))
            navegador.refresh()  # Recarregar a página e tentar novamente

    # Coletar os dados para o código atual
    dadosCodigo()

    # Retornar à página inicial
    navegador.get('https://www2.rio.rj.gov.br/smf/iptulogradouro/')

# Salvar todos os dados em uma planilha
df = pd.DataFrame(todos_os_dados)
df.to_excel("tabela_formatada4.xlsx", index=False)

print("Tabela salva como 'tabela_formatada4.xlsx'.")
navegador.quit()
