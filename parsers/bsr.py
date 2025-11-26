# parsers/bsr.py
"""
Парсер для BlackScreenRecords.com с наследованием от BaseParser
"""
import re
import time
import json
from typing import Dict, List, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pathlib import Path
from .base_parser import BaseParser


class BSRParser(BaseParser):
    """Парсер для сайта BlackScreenRecords.com"""

    def __init__(self, output_root: str = "parsed", headless: bool = True):
        super().__init__("BSR")
        self.base_url = "https://blackscreenrecords.com"
        self.output_root = Path(output_root)
        self.output_root.mkdir(parents=True, exist_ok=True)
        self.headless = headless
        self.min_image_size = 480  # Минимальный размер для фильтрации

    SEL_GRID_ITEM = "div.product-grid-item"
    SEL_LINK = "a.product-grid-item__title[data-grid-link]"
    SEL_SOLD = "div.product__badge div.product__badge__svg[aria-label='Sold out']"
    SEL_VARIANT = "form[data-product-form] input[name='id']"

    def handle_cookies(self, driver):
        try:
            time.sleep(0.5)
        except Exception as e:
            self.log(f"Ошибка обработки cookies: {e}")

    def get_product_urls(self, category_url: str, max_products: int = 100) -> List[str]:
        return self.collect_links(category_url, max_products)

    def wait_grid_ready(self, driver, css: str, timeout: float = 20.0):
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))

    def scroll_page_incremental(self, driver, step=800, pause=0.6, max_steps=300):
        last_y = -1
        stagnant = 0
        for _ in range(max_steps):
            driver.execute_script(f"window.scrollBy(0, {step});")
            time.sleep(pause)
            y = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
            if y == last_y:
                stagnant += 1
            else:
                stagnant = 0
            last_y = y
            at_bottom = driver.execute_script(
                "return (window.innerHeight + window.pageYOffset) >= (document.body.scrollHeight - 5);"
            )
            if at_bottom or stagnant >= 3:
                break

    def collect_links(self, catalog_url: str, max_links: int = 200) -> List[str]:
        print(f"\n🔍 Collecting product URLs from: {catalog_url}")
        driver = self.setup_driver(headless=self.headless)
        if not driver:
            print("❌ Failed to setup driver")
            return []
        product_urls: List[str] = []
        current_page = 1
        max_pages = 50
        try:
            driver.get(catalog_url)
            self.handle_cookies(driver)
            print("⏳ Waiting for initial page load...")
            time.sleep(2)
            self.wait_grid_ready(driver, self.SEL_GRID_ITEM, timeout=20.0)
            while len(product_urls) < max_links and current_page <= max_pages:
                print(f"\n📄 Страница {current_page}")
                self.scroll_page_incremental(driver, step=800, pause=0.6)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                items = soup.select(self.SEL_GRID_ITEM)
                previous_count = len(product_urls)
                for it in items:
                    if it.select_one(self.SEL_SOLD):
                        continue
                    a = it.select_one(self.SEL_LINK)
                    if not a:
                        continue
                    href = a.get("href") or ""
                    if not href:
                        continue
                    if "/collections/" not in href or "/products/" not in href:
                        continue
                    if "variant=" not in href:
                        var = it.select_one(self.SEL_VARIANT)
                        if var:
                            vid = (var.get("value") or "").strip()
                            if vid:
                                sep = "&" if "?" in href else "?"
                                href = f"{href}{sep}variant={vid}"
                    if href.startswith("/"):
                        href = self.base_url + href
                    elif not href.startswith("http"):
                        href = f"{self.base_url}/{href}"
                    if href not in product_urls:
                        product_urls.append(href)
                        if len(product_urls) >= max_links:
                            break
                new_links = len(product_urls) - previous_count
                print(f"  📊 Collected: {len(product_urls)} (+{new_links})")
                if len(product_urls) >= max_links:
                    print(f"  ✅ Reached limit of {max_links} products")
                    break
                base_catalog_url = driver.current_url.split("?")[0]
                next_page = current_page + 1
                next_url = f"{base_catalog_url}?page={next_page}"
                print(f"\n➡️ Переход на страницу {next_page}: {next_url}")
                driver.get(next_url)
                time.sleep(2)
                if f"page={next_page}" not in driver.current_url and driver.current_url != next_url:
                    print(f"\n✅ Больше страниц нет (последняя: {current_page})")
                    break
                try:
                    self.wait_grid_ready(driver, self.SEL_GRID_ITEM, timeout=15.0)
                except Exception:
                    print(f"⚠️ Сетка товаров не загрузилась на странице {next_page}")
                    break
                current_page = next_page
            print(f"\n📋 Collected URLs:")
            for i, url in enumerate(product_urls[:max_links], 1):
                print(f"  [{i}] {url}")
        except Exception as e:
            print(f"❌ Error collecting URLs: {e}")
            import traceback
            traceback.print_exc()
        finally:
            try:
                driver.quit()
            except:
                pass
        result = product_urls[:max_links]
        print(f"\n✅ Total collected: {len(result)} product URLs")
        return result

    def parse_product_page(self, driver, url: str) -> Dict:
        self.log(f"[BSR] Открываем карточку: {url}")
        driver.get(url)
        self.handle_cookies(driver)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product__title"))
            )
        except Exception:
            self.log(f"[BSR] Не удалось дождаться основного контента: {url}")
            return {}

        soup = BeautifulSoup(driver.page_source, "html.parser")
        data: Dict[str, object] = {}

        # ===== Title & Artist =====
        title_author = soup.select_one(".product__title-and-price")
        if title_author:
            t = title_author.select_one("h1.product__title")
            if t:
                data["title"] = t.get_text(strip=True)
            a = title_author.select_one("h3.product__author")
            if a:
                at = a.get_text(strip=True)
                if at.lower().startswith("by "):
                    at = at[3:]
                data["artist"] = at
        if "title" not in data:
            t = soup.select_one("h1.product__title")
            if t:
                data["title"] = t.get_text(strip=True)
        if "artist" not in data:
            a = soup.select_one("h3.product__author")
            if a:
                at = a.get_text(strip=True)
                if at.lower().startswith("by "):
                    at = at[3:]
                data["artist"] = at

        # ===== Label =====
        label_tag = soup.select_one("div.product__block div.product__subheading p")
        if label_tag:
            raw_label = label_tag.get_text(strip=True)
            parts = [p.strip() for p in raw_label.replace("/", ",").split(",") if p.strip()]
            data["label"] = ", ".join(parts) if parts else None
        else:
            data["label"] = None

        # ===== Price =====
        price_tag = soup.select_one("span[data-product-price]")
        if price_tag:
            data["price"] = price_tag.get_text(strip=True)

        # ===== Format =====
        fmt = None
        btn_val = soup.select_one("button.select-popout__toggle span.select-popout__value")
        if btn_val:
            fmt = btn_val.get_text(strip=True)
        if not fmt:
            checked_radio = soup.select_one("span.radio__button input.radio__input:checked + label.radio__label span")
            if checked_radio:
                fmt = checked_radio.get_text(strip=True)
        data["format"] = fmt if fmt else None

        # ===== Genre =====
        genre = None
        crumbs = [c.get_text(strip=True) for c in soup.select("nav.breadcrumb a, ol.breadcrumb a") if c.get_text(strip=True)]
        if crumbs:
            candidates = [c for c in crumbs if c.lower() not in ("home", "collections", "products", "all products")]
            if candidates:
                genre = ", ".join(dict.fromkeys(candidates))
        if not genre:
            tags = [t.get_text(strip=True) for t in soup.select(".product__tags a") if t.get_text(strip=True)]
            if tags:
                genre = ", ".join(dict.fromkeys(tags))
        data["genre"] = genre

        # ===== Description =====
        desc_text = self._extract_description_by_button(soup)
        if desc_text:
            data["description"] = desc_text

        # ===== Tracklist =====
        data["tracklist"] = self._extract_tracklist_raw(soup)

        # ===== Release date =====
        release_date = "Уже в продаже"
        disc_title = soup.select_one(".product-disclaimer__title")
        if disc_title and "pre-order" in disc_title.get_text(strip=True).lower():
            date_tag = soup.select_one(".product-disclaimer__text strong, .product-disclaimer__text b")
            if date_tag:
                raw_date = date_tag.get_text(strip=True)
                # 🔥 Новая функция для преобразования английских дат
                release_date = self.parse_english_month_year(raw_date)
        data["release_date"] = release_date


        # ===== Images (НОВАЯ ЛОГИКА) =====
        image_urls = self.get_image_urls(soup)
        data["image_urls"] = image_urls
        self.log(f"[DBG] image_urls ({len(image_urls)}): {image_urls}")

        for key in ("artist", "title", "label", "format", "genre", "release_date", "price", "description", "tracklist", "image_urls"):
            data.setdefault(key, None)

        return data
    
    def parse_english_month_year(self, text: str) -> str:
        """
        Преобразует 'MARCH 2026' -> 'Март 2026'
        или 'March 21, 2026' -> '21 Марта 2026'
        """
        if not text:
            return "Уже в продаже"
        
        txt = text.strip()
        
        # Русские месяцы (именительный - без даты)
        MONTHS_RU_IM = {
            'january': 'Январь', 'february': 'Февраль', 'march': 'Март',
            'april': 'Апрель', 'may': 'Май', 'june': 'Июнь',
            'july': 'Июль', 'august': 'Август', 'september': 'Сентябрь',
            'october': 'Октябрь', 'november': 'Ноябрь', 'december': 'Декабрь'
        }
        
        # Русские месяцы (родительный - с датой)
        MONTHS_RU_GEN = {
            'january': 'Января', 'february': 'Февраля', 'march': 'Марта',
            'april': 'Апреля', 'may': 'Мая', 'june': 'Июня',
            'july': 'Июля', 'august': 'Августа', 'september': 'Сентября',
            'october': 'Октября', 'november': 'Ноября', 'december': 'Декабря'
        }
        
        # Паттерн 1: "Month Day, Year" (March 21, 2026)
        m1 = re.search(r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})', txt, re.IGNORECASE)
        if m1:
            month_en = m1.group(1).lower()
            day = m1.group(2)
            year = m1.group(3)
            month_ru = MONTHS_RU_GEN.get(month_en)
            if month_ru:
                return f"{day} {month_ru} {year}"
        
        # Паттерн 2: "MONTH YEAR" (MARCH 2026)
        m2 = re.search(r'([A-Za-z]+)\s+(\d{4})', txt, re.IGNORECASE)
        if m2:
            month_en = m2.group(1).lower()
            year = m2.group(2)
            month_ru = MONTHS_RU_IM.get(month_en)
            if month_ru:
                return f"{month_ru} {year}"
        
        return text


    def get_image_urls(self, soup: BeautifulSoup) -> List[str]:
        """Извлечение URL изображений ТОЛЬКО товара"""
        image_urls = []
        seen_urls = set()

        # 1. Все слайды галереи товара
        product_slides = soup.select('div[data-product-slide][data-type="image"]')
        self.log(f"[DBG] Найдено слайдов галереи: {len(product_slides)}")
        
        for slide in product_slides:
            # Ищем ВСЕ <img> в слайде
            imgs = slide.select('img')
            
            # Берем последний (обычно это полноразмерное изображение)
            if imgs:
                # Пробуем достать из последнего img src (это полное разрешение)
                last_img = imgs[-1]
                src = last_img.get('src', '').strip()
                
                if src and '/blank_' not in src and src not in seen_urls:
                    url = self._normalize_url(src)
                    if self._is_product_image(url) and url not in seen_urls:
                        image_urls.append(url)
                        seen_urls.add(url)
                        self.log(f"[DBG] ✅ Full-res image: {url}")
                        continue
            
            # Если последний img не подошел, ищем srcset в первом img
            for img in imgs:
                srcset = img.get('data-srcset', '') or img.get('srcset', '')
                if srcset:
                    urls = self._parse_srcset(srcset)
                    if urls:
                        # НЕ ФИЛЬТРУЕМ ПО РАЗМЕРУ - берем максимальное
                        if urls:
                            url = self._get_highest_resolution(urls)
                            if url and self._is_product_image(url) and url not in seen_urls:
                                image_urls.append(url)
                                seen_urls.add(url)
                                self.log(f"[DBG] ✅ Srcset image: {url}")
                                break

        # 2. ФОЛЛБЕК: JSON данные товара
        if not image_urls:
            script_tags = soup.find_all('script', type='application/json')
            for script in script_tags:
                if 'ProductJson' in script.get('id', ''):
                    try:
                        data_json = json.loads(script.string)
                        if 'media' in data_json:
                            for media in data_json['media']:
                                if media.get('media_type') == 'image':
                                    src = media.get('src', '')
                                    if src and src not in seen_urls:
                                        url = self._normalize_url(src)
                                        image_urls.append(url)
                                        seen_urls.add(url)
                                        self.log(f"[DBG] ✅ JSON image: {url}")
                    except Exception as e:
                        self.log(f"[DBG] Ошибка парсинга JSON ProductJson: {e}")

        return image_urls


    def _parse_srcset(self, srcset: str) -> List[Tuple[str, int]]:
        """Парсит srcset и возвращает список (url, width)"""
        urls = []
        for item in srcset.split(','):
            parts = item.strip().split()
            if len(parts) >= 1:
                url = parts[0]
                width = 0
                if len(parts) > 1 and parts[1].endswith('w'):
                    try:
                        width = int(parts[1][:-1])
                    except ValueError:
                        pass
                size_match = re.search(r'_(\d+)x(\d+)\.', url)
                if size_match and width == 0:
                    width = int(size_match.group(1))
                urls.append((url, width))
        return urls

    def _check_image_size_in_url(self, url: str, min_size: int) -> bool:
        """Проверяет размер изображения по URL"""
        size_match = re.search(r'_(\d+)x(\d+)\.', url)
        if size_match:
            width = int(size_match.group(1))
            height = int(size_match.group(2))
            return width >= min_size and height >= min_size

        if '2048x2048' in url or '1024x1024' in url or '720x720' in url:
            return True

        if any(small in url.lower() for small in ['135x135', '180x', '360x', '32x32', 'icon', 'logo', 'thumb']):
            return False

        return True

    def _get_highest_resolution(self, urls: List[Tuple[str, int]]) -> str:
        """Возвращает URL с максимальным разрешением"""
        if not urls:
            return None
        sorted_urls = sorted(urls, key=lambda x: x[1], reverse=True)
        url = sorted_urls[0][0]
        return self._normalize_url(url)

    def _normalize_url(self, url: str) -> str:
        """Нормализует URL"""
        if not url:
            return None
        url = url.strip()
        if url.startswith('//'):
            return 'https:' + url
        elif url.startswith('http://'):
            return url.replace('http://', 'https://')
        elif not url.startswith('http'):
            if self.base_url:
                return self.base_url.rstrip('/') + '/' + url.lstrip('/')
            return 'https:' + url
        return url

    def _is_product_image(self, url: str) -> bool:
        """Проверяет, является ли URL изображением товара (не логотипом, не баннером)"""
        if not url:
            return False
        url_lower = url.lower()

        # СТРОГИЙ ЧЕРНЫЙ СПИСОК
        exclude_patterns = [
            'bsr-logo', 'logo', 'header', 'footer', 'icon', 'favicon',
            'pattern', 'background', 'bg-', 'blank',
            'payment', 'badge', 'banner', 'loading',
            '.svg', '.gif',
            '135x135', '32x32', '64x64', '100x100',
            '180x', '360x'
        ]
        for pattern in exclude_patterns:
            if pattern in url_lower:
                return False

        # БЕЛЫЙ СПИСОК - только товары
        include_patterns = [
            '/cdn/shop/products/',
            '/cdn/shop/files/'
        ]
        for pattern in include_patterns:
            if pattern in url_lower:
                return True

        return False

    # ===== ОСТАЛЬНЫЕ МЕТОДЫ БЕЗ ИЗМЕНЕНИЙ =====
    def _extract_description_by_button(self, soup: BeautifulSoup) -> str:
        btn = soup.select_one('button.product__accordion__title[aria-controls*="page-description-"]')
        if not btn:
            return ""
        acc_id = (btn.get("aria-controls") or "").strip()
        if not acc_id:
            return ""
        content = soup.select_one(f"#{acc_id}.product__accordion__content") or soup.select_one(f"#{acc_id}")
        if not content:
            return ""
        parts: List[str] = []
        inner_nodes = content.select(".product__accordion__inner, .metafield-rich_text_field, .rte")
        if inner_nodes:
            for node in inner_nodes:
                txt = node.get_text(separator="\n", strip=True)
                if txt:
                    parts.append(txt)
        else:
            txt = content.get_text(separator="\n", strip=True)
            if txt:
                parts.append(txt)
        if not parts:
            return ""
        out, seen = [], set()
        for p in parts:
            if p not in seen:
                out.append(p)
                seen.add(p)
        return "\n".join(out)

    def _extract_tracklist_raw(self, soup: BeautifulSoup) -> str:
        btn = soup.select_one('button.product__accordion__title[aria-controls*="page-tracklist-"]')
        if not btn:
            return ""
        acc_id = (btn.get("aria-controls") or "").strip()
        if not acc_id:
            return ""
        content = soup.select_one(f"#{acc_id}.product__accordion__content") or soup.select_one(f"#{acc_id}")
        if not content:
            return ""
        node = (content.select_one(".metafield-multi_line_text_field")
                or content.select_one(".product__accordion__inner")
                or content)
        raw = node.get_text(separator="\n", strip=True)
        if not raw:
            return ""
        lines = [ln.rstrip() for ln in raw.splitlines()]
        return "\n".join(lines)

    def _normalize_date(self, text: str) -> str:
        months = {
            "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
            "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
        }
        m = re.search(r"([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})", text)
        if m:
            mon = months.get(m.group(1).lower())
            day = int(m.group(2))
            year = int(m.group(3))
            if mon:
                return f"{day:02d}.{mon:02d}.{year}"
        m2 = re.search(r"(\d{1,2})[\.\-\/](\d{1,2})[\.\-\/](\d{4})", text)
        if m2:
            d = int(m2.group(1))
            mon = int(m2.group(2))
            y = int(m2.group(3))
            return f"{d:02d}.{mon:02d}.{y}"
        return text

    def download_images_for_product(self, driver, data: Dict, album_folder_path: str) -> List[str]:
        urls = data.get("image_urls") or []
        if not urls:
            return []
        artist = (data.get("artist") or "Unknown").strip()
        title = (data.get("title") or "Untitled").strip()
        base_name = self.create_safe_filename(artist, title)
        downloaded: List[str] = []
        for i, img_url in enumerate(urls, 1):
            image_name_no_ext = f"{base_name}_{i:02d}"
            ok = self.download_image_with_selenium(driver, img_url, album_folder_path, image_name_no_ext)
            if ok:
                downloaded.append(f"{image_name_no_ext}.jpeg")
        return downloaded
    
    def save_product_info_custom(self, product_data: Dict, url: str) -> str:
        """
        Сохранение информации о товаре в формате HHV (правильный формат)
        """
        artist = product_data.get('artist', 'Unknown Artist')
        title = product_data.get('title', 'Untitled')
        release_date = product_data.get('release_date', '')
        price = product_data.get('price', '')
        label = product_data.get('label', '')
        format_info = product_data.get('format', '')
        genre = product_data.get('genre', '')
        description = product_data.get('description', '')
        tracklist = product_data.get('tracklist', 'Нет треклиста')
        image_urls = product_data.get('image_urls', [])
        downloaded_images = product_data.get('downloaded_images', [])
        
        # Создаем безопасное имя папки
        safe_title = re.sub(r'[\\/*?:"<>|]', "", f"{artist} - {title}")
        safe_title = re.sub(r'\s+', '_', safe_title)
        
        product_folder = self.output_root / safe_title
        product_folder.mkdir(parents=True, exist_ok=True)
        
        # Записываем info.txt
        info_path = product_folder / "info.txt"
        with open(info_path, "w", encoding="utf-8") as f:
            f.write(f"Source URL: {url}\n")
            f.write(f"Site: {self.site_name}\n\n")
            
            # Основные поля
            f.write(f"artist: {artist}\n")
            f.write(f"title: {title}\n")
            
            # Дополнительные поля
            if label:
                f.write(f"label: {label}\n")
            if format_info:
                f.write(f"format: {format_info}\n")
            if genre:
                f.write(f"genre: {genre}\n")
            
            f.write(f"release_date: {release_date}\n")
            if price:
                f.write(f"price: {price}\n")
            
            f.write("\n")
            
            # Изображения
            if image_urls:
                f.write("image_urls:\n")
                for img_url in image_urls:
                    f.write(f"  {img_url}\n")
            
            if downloaded_images:
                f.write("\ndownloaded_images:\n")
                for img_name in downloaded_images:
                    f.write(f"  {img_name}\n")
            
            f.write("\n")
            
            # Описание
            if description:
                f.write("description:\n")
                f.write(description.strip() + "\n\n")
            
            # Треклист
            if tracklist and tracklist != "Нет треклиста":
                f.write("tracklist:\n")
                f.write(tracklist.strip() + "\n")
        
        print(f"✅ info.txt saved: {info_path}")
        return str(product_folder)


    def log(self, message: str):
        print(message)
