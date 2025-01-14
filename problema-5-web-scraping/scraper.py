import requests
from bs4 import BeautifulSoup
import time
import random
import hashlib

# Função para obter o conteúdo da página
def get_page_content(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# Função para calcular o hash do conteúdo HTML da página
def calculate_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# Função para detectar mudanças no layout
def detect_layout_changes(url, headers, previous_hash=None):
    content = get_page_content(url, headers)
    current_hash = calculate_hash(content)
    
    if previous_hash and current_hash != previous_hash:
        return True, current_hash  # Mudança detectada
    else:
        return False, current_hash  # Nenhuma mudança detectada

# Cabeçalhos imitando um navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

# URL da página fictícia
url = 'https://example.com/produtos'

# Intervalo de tempo entre as requisições (2 a 5 segundos)
delay_range = (2, 5)

# Hash anterior do layout
previous_hash = None

# Realizar scraping e detecção de mudanças no layout
for _ in range(5):  # Executar 5 vezes como exemplo
    try:
        change_detected, previous_hash = detect_layout_changes(url, headers, previous_hash)
        if change_detected:
            print("Mudança detectada no layout da página!")
        else:
            print("Nenhuma mudança detectada no layout da página.")
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
    
    # Atraso aleatório entre as requisições
    time.sleep(random.randint(*delay_range))

print("Scraping finalizado.")
