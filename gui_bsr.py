# gui_bsr.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import datetime
from pathlib import Path
import threading
import importlib
import traceback

# Авто‑перезагрузка модулей в dev-режиме
if 'parsers.base_parser' in sys.modules:
    importlib.reload(sys.modules['parsers.base_parser'])
if 'parsers.bsr' in sys.modules:
    importlib.reload(sys.modules['parsers.bsr'])

from parsers.bsr import BSRParser

# Логи
_LOG_DIR = os.path.join("logs", "parser")
os.makedirs(_LOG_DIR, exist_ok=True)
GUI_LOG_FILE = os.path.join(
    _LOG_DIR, "bsr_gui_log_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
)

# Стили
BG_BLACK = "#0a0e14"
FG_GREEN = "#00ff41"
FG_DARK_GREEN = "#00aa2b"
LABEL_BG = "#151b24"
ENTRY_BG = "#2d3035"
ENTRY_FG = "#00ff41"
BUTTON_BG = "#3d4146"
BUTTON_FG = "#00ff41"
BUTTON_ACTIVE_BG = "#3a3f44"

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
    def flush(self):
        pass

class BSRParserGUI:
    def __init__(self, master):
        self.master = master
        master.title("BSR Parser - BlackScreen Records")
        master.geometry("1000x800")
        master.configure(bg=BG_BLACK)

        # Переменные
        self.catalog_url_var = tk.StringVar(value="")
        self.links_file_var = tk.StringVar(value="blackscreen_links.txt")
        self.max_links_var = tk.IntVar(value=200)
        self.headless_var = tk.BooleanVar(value=True)

        self.csv_input_var = tk.StringVar(value="")
        self.csv_output_var = tk.StringVar(value="")
        self.info_folder_var = tk.StringVar(value="parsed")

        # UI
        self.create_header()
        self.create_link_collection_section()
        self.create_parsing_section()
        self.create_csv_section()
        self.create_soldout_section()
        self.create_log_section()

        # Перенаправляем print в лог
        sys.stdout = TextRedirector(self.log_text)

    def create_header(self):
        frame = tk.Frame(self.master, bg=BG_BLACK)
        frame.pack(pady=10)
        tk.Label(frame, text="⬛ BSR PARSER ⬛", font=("Courier New", 20, "bold"),
                 bg=BG_BLACK, fg=FG_GREEN).pack()
        tk.Label(frame, text="BlackScreen Records Automation Tool",
                 font=("Courier New", 10), bg=BG_BLACK, fg=FG_DARK_GREEN).pack()

    def create_link_collection_section(self):
        frame = tk.LabelFrame(self.master, text="[1] СБОР ССЫЛОК",
                              font=("Courier New", 11, "bold"),
                              bg=LABEL_BG, fg=FG_GREEN, relief=tk.GROOVE, bd=2)
        frame.pack(padx=15, pady=10, fill=tk.X)

        row1 = tk.Frame(frame, bg=LABEL_BG); row1.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(row1, text="URL каталога:", bg=LABEL_BG, fg=FG_GREEN,
                 font=("Courier New", 10)).pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.catalog_url_var, bg=ENTRY_BG, fg=ENTRY_FG,
                 font=("Courier New", 9), width=60).pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(frame, bg=LABEL_BG); row2.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(row2, text="Файл ссылок:", bg=LABEL_BG, fg=FG_GREEN,
                 font=("Courier New", 10)).pack(side=tk.LEFT)
        tk.Entry(row2, textvariable=self.links_file_var, bg=ENTRY_BG, fg=ENTRY_FG,
                 font=("Courier New", 9), width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(row2, text="Обзор", command=self.browse_links_file, bg=BUTTON_BG,
                  fg=BUTTON_FG, font=("Courier New", 9)).pack(side=tk.LEFT)

        row3 = tk.Frame(frame, bg=LABEL_BG); row3.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(row3, text="Макс. ссылок:", bg=LABEL_BG, fg=FG_GREEN,
                 font=("Courier New", 10)).pack(side=tk.LEFT)
        tk.Entry(row3, textvariable=self.max_links_var, bg=ENTRY_BG, fg=ENTRY_FG,
                 font=("Courier New", 9), width=10).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(row3, text="Headless режим", variable=self.headless_var,
                       bg=LABEL_BG, fg=FG_GREEN, selectcolor=BUTTON_BG,
                       font=("Courier New", 10)).pack(side=tk.LEFT, padx=20)

        tk.Button(frame, text="▶ СОБРАТЬ ССЫЛКИ", command=self.run_collect_links,
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Courier New", 11, "bold"),
                  activebackground=BUTTON_ACTIVE_BG, height=2).pack(pady=10)

    def create_parsing_section(self):
        frame = tk.LabelFrame(self.master, text="[2] ПАРСИНГ КАРТОЧЕК",
                              font=("Courier New", 11, "bold"),
                              bg=LABEL_BG, fg=FG_GREEN, relief=tk.GROOVE, bd=2)
        frame.pack(padx=15, pady=10, fill=tk.X)

        row1 = tk.Frame(frame, bg=LABEL_BG); row1.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(row1, text="Файл ссылок:", bg=LABEL_BG, fg=FG_GREEN,
                 font=("Courier New", 10)).pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.links_file_var, bg=ENTRY_BG, fg=ENTRY_FG,
                 font=("Courier New", 9), width=40).pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(frame, bg=LABEL_BG); row2.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(row2, text="Папка вывода:", bg=LABEL_BG, fg=FG_GREEN,
                 font=("Courier New", 10)).pack(side=tk.LEFT)
        tk.Entry(row2, textvariable=self.info_folder_var, bg=ENTRY_BG, fg=ENTRY_FG,
                 font=("Courier New", 9), width=40).pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="▶ ЗАПУСТИТЬ ПАРСИНГ", command=self.run_parsing,
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Courier New", 11, "bold"),
                  activebackground=BUTTON_ACTIVE_BG, height=2).pack(pady=10)

    def create_csv_section(self):
        frame = tk.LabelFrame(self.master, text="[3] ГЕНЕРАЦИЯ CSV",
                              font=("Courier New", 11, "bold"),
                              bg=LABEL_BG, fg=FG_GREEN, relief=tk.GROOVE, bd=2)
        frame.pack(padx=15, pady=10, fill=tk.X)

        row1 = tk.Frame(frame, bg=LABEL_BG); row1.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(row1, text="Папка parsed/:", bg=LABEL_BG, fg=FG_GREEN,
                 font=("Courier New", 10)).pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.info_folder_var, bg=ENTRY_BG, fg=ENTRY_FG,
                 font=("Courier New", 9), width=40).pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(frame, bg=LABEL_BG); row2.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(row2, text="Выходной CSV:", bg=LABEL_BG, fg=FG_GREEN,
                 font=("Courier New", 10)).pack(side=tk.LEFT)
        tk.Entry(row2, textvariable=self.csv_output_var, bg=ENTRY_BG, fg=ENTRY_FG,
                 font=("Courier New", 9), width=40).pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="▶ СОЗДАТЬ CSV", command=self.run_csv_generation,
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Courier New", 11, "bold"),
                  activebackground=BUTTON_ACTIVE_BG, height=2).pack(pady=10)

    def create_soldout_section(self):
        frame = tk.LabelFrame(self.master, text="[4] ПРОВЕРКА SOLD OUT",
                              font=("Courier New", 11, "bold"),
                              bg=LABEL_BG, fg=FG_GREEN, relief=tk.GROOVE, bd=2)
        frame.pack(padx=15, pady=10, fill=tk.X)

        row1 = tk.Frame(frame, bg=LABEL_BG); row1.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(row1, text="Входной CSV:", bg=LABEL_BG, fg=FG_GREEN,
                 font=("Courier New", 10)).pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.csv_input_var, bg=ENTRY_BG, fg=ENTRY_FG,
                 font=("Courier New", 9), width=40).pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="▶ ПРОВЕРИТЬ НАЛИЧИЕ", command=self.run_soldout_check,
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Courier New", 11, "bold"),
                  activebackground=BUTTON_ACTIVE_BG, height=2).pack(pady=10)

    def create_log_section(self):
        frame = tk.LabelFrame(self.master, text="ЛОГИ ВЫПОЛНЕНИЯ",
                              font=("Courier New", 11, "bold"),
                              bg=LABEL_BG, fg=FG_GREEN, relief=tk.GROOVE, bd=2)
        frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(frame, bg=BG_BLACK, fg=FG_GREEN,
                                font=("Courier New", 9), wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

    # Обработчики
    def browse_links_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.links_file_var.set(filename)

    def run_collect_links(self):
        thread = threading.Thread(target=self._collect_links_thread, daemon=True)
        thread.start()

    def _collect_links_thread(self):
        try:
            print("\n" + "="*60)
            print("[BSR] НАЧАЛО СБОРА ССЫЛОК")
            print("="*60)

            catalog_url = self.catalog_url_var.get()
            output_file = self.links_file_var.get()
            max_links = self.max_links_var.get()
            headless = self.headless_var.get()

            if not catalog_url.strip():
                messagebox.showwarning("Внимание", "Укажите URL каталога.")
                return

            parser = BSRParser(headless=headless)
            links = parser.collect_links(catalog_url=catalog_url, max_links=max_links)

            with open(output_file, "w", encoding="utf-8") as f:
                for link in links:
                    f.write(link + "\n")

            print(f"\n✅ Сохранено {len(links)} ссылок в {output_file}")
            print("="*60)
            messagebox.showinfo("Успех", f"Собрано {len(links)} ссылок!")
        except Exception as e:
            print(f"\n❌ ОШИБКА: {e}")
            traceback.print_exc()
            messagebox.showerror("Ошибка", str(e))

    def run_parsing(self):
        # Запуск парсинга карточек
        thread = threading.Thread(target=self._parse_thread, daemon=True)
        thread.start()

    def _parse_thread(self):
        try:
            print("\n" + "="*60)
            print("[BSR] ЗАПУСК ПАРСИНГА КАРТОЧЕК")
            print("="*60)

            links_path = self.links_file_var.get().strip()
            output_folder = self.info_folder_var.get().strip() or "parsed"
            headless = self.headless_var.get()

            if not os.path.isfile(links_path):
                messagebox.showwarning("Внимание", f"Файл ссылок не найден: {links_path}")
                return

            # Читаем ссылки
            with open(links_path, "r", encoding="utf-8") as f:
                links = [ln.strip() for ln in f if ln.strip()]

            if not links:
                print("⚠️ В файле ссылок нет URL")
                messagebox.showwarning("Внимание", "В файле ссылок нет URL.")
                return

            parser = BSRParser(headless=headless)
            driver = parser.setup_driver(headless=headless)
            if not driver:
                messagebox.showerror("Ошибка", "Не удалось инициализировать браузер.")
                return

            parsed_ok = 0
            try:
                for idx, url in enumerate(links, 1):
                    print(f"\n[{idx}/{len(links)}] Парсинг: {url}")
                    try:
                        data = parser.parse_product_page(driver, url)
                        if not data:
                            print("  ⚠️ Пропущено (пустой результат)")
                            continue

                        # Сохраняем info.txt и получаем путь
                        saved_path = parser.save_product_info(data, url, output_folder=output_folder)
                        if not saved_path:
                            print("  ⚠️ Не удалось сохранить данные")
                            continue

                        # Используем папку, созданную parser.save_product_info
                        album_dir = os.path.dirname(saved_path)

                        # Скачиваем изображения в ту же папку
                        try:
                            downloaded = parser.download_images_for_product(driver, data, album_dir)
                            data["downloaded_images"] = downloaded
                            print(f"  🖼 Загружено изображений: {len(downloaded)}")
                        except Exception as ie:
                            data["downloaded_images"] = []
                            print(f"  ⚠️ Ошибка загрузки изображений: {ie}")

                        parsed_ok += 1
                        print(f"  ✅ Данные сохранены в: {album_dir}")

                        if downloaded:
                            info_file = os.path.join(album_dir, "info.txt")
                            with open(info_file, 'a', encoding='utf-8') as f:
                                f.write("\n\ndownloaded_images:\n")
                                for img_name in downloaded:
                                    f.write(f"  {img_name}\n")
                            print(f"  ✏️  Обновлен info.txt с downloaded_images")

                    except Exception as e:
                        print(f"  ❌ Ошибка при парсинге: {e}")
                        traceback.print_exc()
                        continue


            finally:
                try:
                    driver.quit()
                except Exception:
                    pass

            print("\n" + "-"*60)
            print(f"Готово: {parsed_ok}/{len(links)} карточек сохранено в {output_folder}")
            print("-"*60)
            messagebox.showinfo("Готово", f"Сохранено {parsed_ok} карточек в {output_folder}")

        except Exception as e:
            print(f"\n❌ ОШИБКА: {e}")
            traceback.print_exc()
            messagebox.showerror("Ошибка", str(e))

    def run_csv_generation(self):
        print("\n[INFO] Функция генерации CSV будет реализована позже")

    def run_soldout_check(self):
        print("\n[INFO] Функция проверки Sold Out будет реализована позже")

if __name__ == "__main__":
    root = tk.Tk()
    app = BSRParserGUI(root)
    root.mainloop()
