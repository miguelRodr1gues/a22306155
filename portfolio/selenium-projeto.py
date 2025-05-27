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

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar em modo headless (sem UI)
    chrome_options.add_argument("--disable-gpu")
    service = Service("/path/to/chromedriver")  # Atualiza para o caminho do teu chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_ciclo_vida_projeto(driver):
    base_url = "http://localhost:8000"
    wait = WebDriverWait(driver, 10)

    # 1. Login prévio (assumindo que já tens um utilizador criado e login é necessário para criar projetos)
    driver.get(base_url + "/accounts/login/")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))

    username = "admin"      # Ajusta para o teu utilizador válido
    password = "admin1234"  # Ajusta para a tua password

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))

    # 2. Aceder à página de criação do projeto
    driver.get(base_url + "/portfolio/projetos/novo/")  # Ajusta conforme a rota do teu site
    wait.until(EC.presence_of_element_located((By.NAME, "nome")))

    # 3. Criar um projeto novo
    nome_projeto = "Projeto Selenium " + random_string(5)
    descricao_projeto = "Descrição do projeto criado automaticamente para testes."
    # Exemplo para campos básicos
    driver.find_element(By.NAME, "nome").send_keys(nome_projeto)
    driver.find_element(By.NAME, "descricao").send_keys(descricao_projeto)

    # Se houver dropdown para disciplinas, escolhe uma (opcional)
    # Por exemplo:
    # disciplina_select = driver.find_element(By.NAME, "disciplina")
    # disciplina_select.click()
    # disciplina_option = driver.find_element(By.XPATH, "//option[contains(text(),'Programação Web')]")
    # disciplina_option.click()

    # Submeter o formulário
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # 4. Verificar que o projeto foi criado (por exemplo, pelo nome do projeto aparecer na página)
    assert nome_projeto in driver.page_source

    # 5. Editar o projeto criado
    # Supondo que a página redireciona para o detalhe do projeto e há um link para editar
    edit_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Editar")))
    edit_link.click()

    wait.until(EC.presence_of_element_located((By.NAME, "descricao")))

    descricao_editada = descricao_projeto + " - Editado."
    descricao_input = driver.find_element(By.NAME, "descricao")
    descricao_input.clear()
    descricao_input.send_keys(descricao_editada)

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Verificar que a descrição editada está visível
    assert descricao_editada in driver.page_source

    # 6. Eliminar o projeto
    delete_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Eliminar")))
    delete_link.click()

    # Confirmar alerta popup, se existir
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    # Esperar para ver se o projeto desapareceu
    time.sleep(2)
    assert nome_projeto not in driver.page_source

    # 7. Logout
    driver.find_element(By.LINK_TEXT, "Logout").click()
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Login")))
