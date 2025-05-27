import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import string
import random

# Configurações do Chrome WebDriver
@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Rodar sem abrir janela
    chrome_options.add_argument("--disable-gpu")
    service = Service("/path/to/chromedriver")  # Ajusta para o caminho do teu chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_fluxo_autenticacao(driver):
    base_url = "http://localhost:8000"

    # Gerar dados aleatórios para o registo
    username = "user_" + random_string()
    email = username + "@example.com"
    password = "TestPass123!"

    wait = WebDriverWait(driver, 10)

    # 1. Página de registo
    driver.get(base_url + "/accounts/signup/")  # Ajusta a URL de registo conforme o teu site
    wait.until(EC.presence_of_element_located((By.NAME, "username")))

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password1").send_keys(password)
    driver.find_element(By.NAME, "password2").send_keys(password)

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Espera redirecionar e verificar login bem-sucedido (exemplo: botão logout)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))

    # 2. Logout para testar login separado
    driver.find_element(By.LINK_TEXT, "Logout").click()
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Login")))

    # 3. Login com o utilizador registado
    driver.find_element(By.LINK_TEXT, "Login").click()
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Confirma login (ex: link logout aparece)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))

    # 4. Criar um novo artigo
    driver.get(base_url + "/artigos/novo/")  # Ajusta URL para criação de artigo
    wait.until(EC.presence_of_element_located((By.NAME, "titulo")))

    titulo_artigo = "Artigo Teste " + random_string(5)
    conteudo_artigo = "Conteúdo do artigo de teste criado automaticamente."

    driver.find_element(By.NAME, "titulo").send_keys(titulo_artigo)
    driver.find_element(By.NAME, "conteudo").send_keys(conteudo_artigo)

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Verificar se o artigo foi criado e está visível (exemplo: título aparece na página)
    assert titulo_artigo in driver.page_source

    # 5. Apagar o artigo criado
    # Navega para a página do artigo (assumindo que após criação redireciona para o detalhe)
    # E encontra o botão ou link de eliminar
    try:
        delete_button = driver.find_element(By.LINK_TEXT, "Eliminar")
        delete_button.click()
        alert = driver.switch_to.alert
        alert.accept()  # Confirmar popup de eliminação se houver

        # Espera e verifica se o artigo foi eliminado (exemplo: volta à lista ou mensagem)
        time.sleep(2)
        assert titulo_artigo not in driver.page_source
    except Exception as e:
        pytest.fail(f"Não foi possível eliminar o artigo: {e}")

    # 6. Logout final
    driver.find_element(By.LINK_TEXT, "Logout").click()
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Login")))
