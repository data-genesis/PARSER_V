# parsers/base_parser.py
"""
Базовый класс для всех парсеров сайтов
"""
import os
import re
import time
import logging
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import base64
import sys


class BaseParser(ABC):
    """Базовый класс для всех парсеров"""
    
    def __init__(self, site_name: str):
        self.site_name = site_name
        self.driver = None
        self.setup_logging()
    
    def setup_logging(self):
        """Настройка логирования для парсера"""
        log_dir = os.path.join("logs", "parser")
        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception:
            pass
        log_filename = os.path.join(log_dir, f"{self.site_name}_parser_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            encoding='utf-8'
        )
        logging.info(f"=== {self.site_name} parser session started ===")
    
    # parsers/base_parser.py - замените ТОЛЬКО метод setup_driver

    def setup_driver(self, headless=True) -> Optional[webdriver.Chrome]:
        """Инициализация Chrome WebDriver с общими настройками"""
        print(f"Setting up browser driver for {self.site_name}...")
        options = Options()
        
        # HEADLESS режим (можно отключить)
        if headless:
            options.add_argument("--headless")
            print("  🔇 Headless mode: ON (фоновый режим)")
        else:
            print("  🔊 Headless mode: OFF (окно браузера будет видно)")
        
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1200")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")
        options.add_argument('log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        try:
            # Ищем chromedriver в папке проекта
            driver_path = None
            
            # Список мест где искать (в порядке приоритета)
            candidates = [
                # В папке chromedriver в корне проекта
                os.path.join("chromedriver", "chromedriver.exe"),
                os.path.join("chromedriver", "chromedriver"),
                # В папке drivers
                os.path.join("drivers", "chromedriver.exe"),
                os.path.join("drivers", "chromedriver"),
                # Переменные окружения
                os.getenv("CHROMEDRIVER"),
                os.getenv("WEBDRIVER_CHROME_DRIVER"),
            ]
            
            for cand in candidates:
                if cand and os.path.exists(cand):
                    driver_path = os.path.abspath(cand)
                    print(f"✅ДРАЙВЕР НА МЕСТЕ: {driver_path}")
                    break
            
            if driver_path and os.path.exists(driver_path):
                service = ChromeService(executable_path=driver_path)
            else:
                # Фоллбек: webdriver_manager (скачает нужную версию)
                print("⚠️ Local ChromeDriver not found. Using webdriver-manager...")
                service = ChromeService(ChromeDriverManager().install())
            
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            print(f"✅ РАБОТАЕМ С {self.site_name}.")
            return driver
        except Exception as e:
            print(f"❌ Error setting up driver for {self.site_name}: {e}")
            import traceback
            traceback.print_exc()
            return None

    
    @abstractmethod
    def handle_cookies(self, driver):
        """Обработка cookies - должна быть реализована в каждом парсере"""
        pass
    
    @abstractmethod
    def get_product_urls(self, category_url: str, max_products: int = 100) -> List[str]:
        """Получение списка URL товаров из категории - должна быть реализована в каждом парсере"""
        pass
    
    @abstractmethod
    def parse_product_page(self, driver, url: str) -> Dict:
        """Парсинг отдельной страницы товара - должна быть реализована в каждом парсере"""
        pass
    
    @abstractmethod
    def get_image_urls(self, soup: BeautifulSoup) -> List[str]:
        """Извлечение URL изображений - должна быть реализована в каждом парсере"""
        pass
    
    def download_image_with_selenium(self, driver, image_url: str, folder_path: str, image_name: str, max_retries: int = 3) -> bool:
        """Универсальная функция загрузки изображений через Selenium"""
        for attempt in range(max_retries):
            try:
                logging.info(f"Attempting image download (attempt {attempt + 1}/{max_retries}) | url={image_url} | save_dir={folder_path} | filename={image_name}.jpeg")
                
                driver.set_script_timeout(60)
                
                js_script = """
                    var url = arguments[0];
                    var callback = arguments[1];
                    var xhr = new XMLHttpRequest();
                    xhr.timeout = 30000;
                    xhr.onload = function() {
                        var reader = new FileReader();
                        reader.onloadend = function() {
                            callback(reader.result);
                        }
                        reader.readAsDataURL(xhr.response);
                    };
                    xhr.onerror = function() {
                        callback(null);
                    };
                    xhr.ontimeout = function() {
                        callback(null);
                    };
                    xhr.open('GET', url);
                    xhr.responseType = 'blob';
                    xhr.send();
                """
                
                base64_data = driver.execute_async_script(js_script, image_url)
                
                if base64_data is None:
                    raise Exception("XHR request failed or timed out")
                    
                header, encoded = base64_data.split(",", 1)
                img_bytes = base64.b64decode(encoded)
                
                os.makedirs(folder_path, exist_ok=True)
                img_path = os.path.join(folder_path, f"{image_name}.jpeg")
                with open(img_path, 'wb') as f:
                    f.write(img_bytes)
                
                try:
                    image = Image.open(BytesIO(img_bytes))
                    image = image.convert('RGB')
                    image.save(img_path, format='JPEG', quality=92, optimize=True)
                except Exception:
                    pass
                
                return True
            except Exception as e:
                logging.info(f"Image download error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    return False
    
    def create_safe_filename(self, artist: str, title: str) -> str:
        """Создание безопасного имени файла"""
        full_title = f"{artist} - {title}"
        safe_filename = re.sub(r'[\\/*?:"<>|]', "", full_title)
        url_safe_filename = re.sub(r'\s+', '-', safe_filename)
        url_safe_filename = re.sub(r'-+', '-', url_safe_filename)
        datestamp = datetime.now().strftime("%Y.%m.%d")
        return f"{url_safe_filename}_{datestamp}"
    
    def save_product_info(self, product_data: Dict, url: str, output_folder: str = "output") -> Optional[str]:
        """Сохранение информации о товаре в файл"""
        artist = product_data.get('artist', 'Unknown Artist')
        title = product_data.get('title', 'Untitled')
        
        safe_album_title_for_folder = re.sub(r'[\\/*?:"<>|]', "", f"{artist} - {title}")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        album_folder_name = f"{safe_album_title_for_folder}_{timestamp}"
        album_folder_path = os.path.join(output_folder, album_folder_name)
        os.makedirs(album_folder_path, exist_ok=True)

        final_text_parts = [
            f"Source URL: {url}",
            f"Site: {self.site_name}",
            ""
        ]
        
        for key, value in product_data.items():
            if isinstance(value, list):
                final_text_parts.append(f"{key}:")
                final_text_parts.extend([f"  {item}" for item in value])
            else:
                final_text_parts.append(f"{key}: {value}")

        final_text = "\n".join(final_text_parts)
        text_filename = os.path.join(album_folder_path, "info.txt")
        
        try:
            with open(text_filename, 'w', encoding='utf-8') as f:
                f.write(final_text)
            print(f"Successfully saved data to {text_filename}")
            logging.info(f"Saved info.txt to {text_filename}")
            return text_filename
        except IOError as e:
            print(f"Error saving file {text_filename}: {e}")
            logging.exception(f"Failed to write info.txt at {text_filename}")
            return None
