import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from google_ia import song_name_ia

import os
import time

def actions_on_the_website(latest_video_path):
    try_count = 0
    max_tries = 3  # Número máximo de tentativas

    while try_count < max_tries:
        try:
            print("Iniciando ações para publicar o video. Aguarde!")
            song_name = song_name_ia()
            options = webdriver.ChromeOptions()
            options.add_argument(r"user-data-dir=C:\Users\thiag\AppData\Local\Google\Chrome\User Data\Profile 3")

            driver = webdriver.Chrome(options=options, use_subprocess=True)
            driver.get("https://www.tiktok.com/creator-center/upload?from=upload")
            time.sleep(5)

            # Localizações dos elementos...
            IFRAME_ELEMENT = '//*[@id="root"]/div[2]/div[2]/div/div/iframe'
            FILE_INPUT_ELEMENT = '//*[@id="root"]/div/div/div/div/div/div/div/input'
            TITLE_ELEMENT = '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/span/span'
            BUTTON_EDIT_VIDEO_ELEMENT = '//*[@id="root"]/div/div/div/div[1]/div[1]/div[2]/button'
            INPUT_MUSIC_SEARCH_ELEMENT = '//*[@id="tux-portal-container"]/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/div/div[2]/input'
            BUTTON_FIND_ELEMENT = '//*[@id="tux-portal-container"]/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/div[2]/button'
            DIV_BUTTON_USE_ELEMENT = '/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/div/div/div[2]'
            BUTTON_USE_ELEMENT = '/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/button'
            BUTTON_SAVE_VIDEO_ELEMENT = '//*[@id="tux-portal-container"]/div[2]/div/div/div/div/div[2]/div/div[1]/span/div/div[2]/button[2]'
            SEND_BUTTON_ELEMENT = '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[8]/div[2]/button'

            # Ação com iframe...
            iframe = driver.find_element(By.XPATH, IFRAME_ELEMENT)
            driver.switch_to.frame(iframe)

            # Upload do arquivo...
            upload_file = os.path.join(os.getcwd(), latest_video_path)
            file_input = driver.find_element(By.XPATH, FILE_INPUT_ELEMENT)
            file_input.send_keys(upload_file)

            # Espera pelo carregamento...
            wait = WebDriverWait(driver, 120)
            wait.until(EC.visibility_of_element_located((By.XPATH, TITLE_ELEMENT)))

            # Preenche o título...
            title = driver.find_element(By.XPATH, TITLE_ELEMENT)
            title.send_keys(' #viral #motivação #inspiração #pensamento #vida #dinheiro #ansiedade #depressão #frases #reflexão #foryou #foryoupage #fypシ')
            time.sleep(5)

            # Clica no botão para editar o video
            button_edit_video = driver.find_element(By.XPATH, BUTTON_EDIT_VIDEO_ELEMENT)
            button_edit_video.click()

            # Espera pelo carregamento...
            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, INPUT_MUSIC_SEARCH_ELEMENT)))

            # Adiciona a musica no input
            input_music_search = driver.find_element(By.XPATH, INPUT_MUSIC_SEARCH_ELEMENT)
            input_music_search.send_keys(song_name)

            time.sleep(1)

            # clica no botão procurar
            button_find = driver.find_element(By.XPATH, BUTTON_FIND_ELEMENT)
            button_find.click()

            # Espera pelo carregamento...
            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, DIV_BUTTON_USE_ELEMENT)))

            # Procura o botão Usar
            div_button_use = driver.find_element(By.XPATH, DIV_BUTTON_USE_ELEMENT)

            # Crie uma ação de passar o mouse sobre o elemento
            hover = ActionChains(driver).move_to_element(div_button_use)

            # Execute a ação
            hover.perform()

            time.sleep(5)

            # Clica no botão Usar
            button_use = driver.find_element(By.XPATH, BUTTON_USE_ELEMENT)
            button_use.click()
            print('ENTROU 6')
            time.sleep(10)

            # Clica no botao salvar edição
            button_save_video = driver.find_element(By.XPATH, BUTTON_SAVE_VIDEO_ELEMENT)
            button_save_video.click()

            time.sleep(5)

            # Envia o vídeo...
            send_button = driver.find_element(By.XPATH, SEND_BUTTON_ELEMENT)
            driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
            time.sleep(2)
            send_button.click()

            print("Publicando video...")
            time.sleep(50)
            print("Video publicado!")

            # Se tudo ocorreu bem, sair do loop
            break

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            try_count += 1
            print(f"Tentativa {try_count} de {max_tries}")

        finally:
            if driver:
                driver.quit()

    if try_count == max_tries:
        print("Não foi possível publicar o vídeo após várias tentativas.")

