import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('intraday_bar_bot.log', encoding='utf-8')
    ]
)

def get_intraday_signals(url):
    """Получение сигналов с сайта Intraday Bar"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        signals = []

        # Парсинг сигналов (этот блок нужно адаптировать под структуру сайта)
        signal_elements = soup.find_all('div', class_='signal-class')  # Примерный селектор
        for element in signal_elements:
            symbol = element.find('span', class_='symbol-class').text  # Примерный селектор
            signal_type = element.find('span', class_='type-class').text  # Примерный селектор
            entry_price = float(element.find('span', class_='entry-class').text)  # Примерный селектор
            take_profit = float(element.find('span', class_='tp-class').text)  # Примерный селектор
            stop_loss = float(element.find('span', class_='sl-class').text)  # Примерный селектор
            signals.append((symbol, signal_type, entry_price, take_profit, stop_loss))
        
        return signals
    except requests.RequestException as e:
        logging.error(f"Ошибка при получении сигналов: {e}")
        return []

def get_intraday_signals_selenium(url):
    """Получение сигналов с сайта Intraday Bar с использованием Selenium"""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(5)  # Время ожидания загрузки страницы, можно увеличить при необходимости

        signals = []
        
        # Парсинг сигналов (этот блок нужно адаптировать под структуру сайта)
        signal_elements = driver.find_elements(By.CLASS_NAME, 'signal-class')  # Примерный селектор
        for element in signal_elements:
            symbol = element.find_element(By.CLASS_NAME, 'symbol-class').text  # Примерный селектор
            signal_type = element.find_element(By.CLASS_NAME, 'type-class').text  # Примерный селектор
            entry_price = float(element.find_element(By.CLASS_NAME, 'entry-class').text)  # Примерный селектор
            take_profit = float(element.find_element(By.CLASS_NAME, 'tp-class').text)  # Примерный селектор
            stop_loss = float(element.find_element(By.CLASS_NAME, 'sl-class').text)  # Примерный селектор
            signals.append((symbol, signal_type, entry_price, take_profit, stop_loss))
        
        driver.quit()
        return signals
    except Exception as e:
        logging.error(f"Ошибка при получении сигналов с помощью Selenium: {e}")
        return []

def main():
    url = 'https://www.intradaybar.com/signals'  # Примерный URL для сигналов
    use_selenium = False  # Использовать Selenium или нет

    if use_selenium:
        signals = get_intraday_signals_selenium(url)
    else:
        signals = get_intraday_signals(url)

    if signals:
        for signal in signals:
            symbol, signal_type, entry_price, take_profit, stop_loss = signal
            logging.info(f"Signal: {signal_type} {symbol} (entry: {entry_price}, take profit: {take_profit}, stop loss: {stop_loss})")
    else:
        logging.info("Нет новых сигналов")

if __name__ == '__main__':
    main()
