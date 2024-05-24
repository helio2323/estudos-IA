import sqlite3
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Caminho para o driver do Chrome

# Definir opções do Chrome
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": "caminho/para/diretorio_de_downloads", # Mudar para o caminho desejado
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
chrome_options.add_extension('./solver.crx')


# Inicializar o driver do Chrome com as opções configuradas
driver = webdriver.Chrome( options=chrome_options)

page_number = '1'

# Abrir uma página web
driver.get('https://www.lategames.net/roms/sega-32x/?page='+ page_number +'&sort=popularity')


# Conectar ao banco de dados
conn = sqlite3.connect('games.db')
cursor = conn.cursor()

try:
    # Selecionar todos os dados da tabela 'nintendo64'
    cursor.execute("SELECT * FROM usuarios") # ALTERAR AQUI
    
    # Iterar sobre os resultados e imprimir cada linha
    print('Iniciando o Download dos Jogos: ')
    for row in cursor.fetchall():

        dow = row[1]

        if dow == '':

            print('Iniciando o Download do Jogo: ')
            driver.get(row[0])

            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/section/div[1]/div[2]/div[4]/button[1]'))
            )
            
            # Clicar no elemento
            element.click()

            download = True

            while download:
                element_ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[1]/h1/span'))
                )
            
                txt = element_.text

                if txt == 'Your download has started!':
                    download = False

                    #atualiza o banco de dados #ALTERAR AQUI
                    cursor.execute("UPDATE usuarios SET donwload = 'ok' WHERE url = ?", (row[0],))
                    conn.commit()
                    print('Download concluído com sucesso!')

                print('Aguardando inicio do download...')
                time.sleep(1)



except sqlite3.Error as e:
    print(f"Erro ao acessar os dados: {e}")

finally:
    # Fechar a conexão com o banco de dados
    conn.close()
