# recomendo criar um ambiente virtual para instalar as bibliotecas
# python -m venv nome_ambiente


import re
import time
# pip install pandas
import pandas as pd
#  pip install webdriver
from selenium import webdriver
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
# configurações para abrir qualquer versão instalada do Chrome
navegador = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Indicando onde está o arquivo base
planilha = 'pesquisa_enderecos'
end_pes = pd.read_excel(f'{planilha}.xlsx')

# Removendo linhas duplicadas com base em uma coluna
end_pes = end_pes.drop_duplicates(subset=['enderecos'])
# Excluindo valores nan
end_pes = end_pes.dropna(subset=['enderecos'])

for index, row in end_pes.iterrows():
    endereco = row['enderecos']
    end_formatado = endereco.replace(' ', '+')
    navegador.get(f'https://www.google.com.br/maps/place/{end_formatado}')
    time.sleep(10)
    res_pes = navegador.current_url
    end_pes.at[index, 'url'] = res_pes
    
    # Expressão regular para encontrar os números entre "@" e ",17z/data" do link
    padrao = r'@(-?\d+\.\d+),(-?\d+\.\d+),'

    # Usando a função findall para extrair os números
    numeros = re.findall(padrao, res_pes)

    # Exibindo os números encontrados
    if numeros:
        latitude, longitude = numeros[0]
        print("Latitude:", latitude)
        print("Longitude:", longitude)
    else:
        print("Números não encontrados.")

    end_pes.at[index, 'lat'] = latitude
    end_pes.at[index, 'log'] = longitude

navegador.close()

end_pes.to_excel('resultados_enderecos.xlsx', index=False)