import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# Configurações do Chrome WebDriver
@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar em modo headless (sem abrir janela)
    chrome_options.add_argument("--disable-gpu")
    service = Service("/path/to/chromedriver")  # Ajusta para o caminho do teu chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

def test_navegacao_basica(driver):
    base_url = "http://localhost:8000"

    # Visitar página inicial
    driver.get(base_url)
    time.sleep(1)
    assert "Home" in driver.title or "Início" in driver.title

    # Validar menu principal (exemplo)
    menu = driver.find_element(By.ID, "main-menu")
    assert menu is not None

    # Navegar para página de artigos
    driver.find_element(By.LINK_TEXT, "Artigos").click()
    time.sleep(1)
    assert "Artigos" in driver.title
    assert "NEGAO" in driver.page_source  # Exemplo de conteúdo esperado na página

    # Navegar para página de bandas
    driver.find_element(By.LINK_TEXT, "Bandas").click()
    time.sleep(1)
    assert "Bandas" in driver.title
    assert "Destiny's Child" in driver.page_source

    # Navegar para página de projetos
    driver.find_element(By.LINK_TEXT, "Projetos").click()
    time.sleep(1)
    assert "Projetos" in driver.title
    assert "Humans VS Zombies" in driver.page_source

    # Validar footer ou outro conteúdo fixo
    footer = driver.find_element(By.TAG_NAME, "footer")
    assert footer is not None
    assert "©" in footer.text

