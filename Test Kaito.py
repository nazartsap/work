import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import subprocess
import time
import psutil
from seleniumwire import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from faker import Faker
from tkinter import simpledialog
import pymongo
from pymongo import MongoClient

client_uri = "mongodb+srv://nazar:Iwasborn1012@cluster0.7d9g74q.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(client_uri)
db = client['KAITO'] 
users_collection = db['users']  

def authenticate():
    username = simpledialog.askstring("login", "Enter your username:")
    password = simpledialog.askstring("password", "Enter your password:", show="*")

    if username is not None and password is not None:
        user = users_collection.find_one({"login": username, "password": password})
        if user:
            root.withdraw()  # Скрыть первую форму
            show_main_form()  # Показать вторую форму
        else:
            tk.messagebox.showerror("Error", "Authentication failed. Please try again.")

# Определите глобальные переменные для хранения значений из полей ввода
proxy_entries = []
email_entries = []

def show_main_form():
    def browse_proxies():
        global proxy_entries
        proxy_entries = proxy_text.get("1.0", "end-1c").splitlines()

    def browse_emails():
        global email_entries
        email_entries = email_text.get("1.0", "end-1c").splitlines()

    def run_script(proxy_url, email):
        driver_path = 'C:/webdrivers/chromedriver.exe'
        trace_extension_path = 'C:/Users/nazar/AppData/Local/Google/Chrome/User Data/Profile/Extensions/njkmjblmcfiobddjgebnoeldkjcplfjb/3.0.6_0'
        faker = Faker()

        chrome_options = Options()
        chrome_options.headless = False 
        chrome_options.add_argument(f'--user-data-dir=c:/Users/nazar/AppData/Local/Google/Chrome/User Data/Profile 4')
        chrome_options.add_argument(f'--load-extension={trace_extension_path}')  
        chrome_options.add_argument('--incognito')
        driver = uc.Chrome(executable_path=driver_path, options=chrome_options, seleniumwire_options={'proxy': {'https': proxy_url}})
        
        try:
            driver.get('https://www.kaito.ai/trial/Individual')

            random_name = faker.first_name()
            random_surname = faker.last_name()

            name_field = driver.find_element(By.NAME, 'given_name')
            name_field.send_keys(random_name)

            l_name_field = driver.find_element(By.NAME, 'family_name')
            l_name_field.send_keys(random_surname)

            select_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'field-:R12j99f6:'))
            )
            email_field = driver.find_element(By.NAME, 'email')
            email_field.clear()  # Clear the email field
            email_field.send_keys(email)  # Use the specific email for this proxy

            select = Select(select_element)
            select.select_by_visible_text("Indonesia")

            span_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chakra-checkbox__control.css-nxy0t9"))
            )
            for element in span_elements:
                element.click()

            login_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".chakra-button.css-xbdp3o"))
            )
            login_button.click()
            time.sleep(50)

        except Exception as e:
            print(f'Error with proxy {proxy_url} for email {email}: {str(e)}')
        
        finally:
            # Close the browser and terminate the Google Chrome process using psutil
            driver.quit()
            for process in psutil.process_iter(attrs=['pid', 'name']):
                if 'chrome' in process.info['name'].lower():  # Проверяем имя процесса, игнорируя регистр
                    try:
                        psutil.Process(process.info['pid']).terminate()
                    except psutil.NoSuchProcess:
                        pass

        time.sleep(20)
        print(f'Success with proxy {proxy_url} for email: {email}')

    # Определите функцию для запуска скрипта на основе значений из полей ввода
    def start_script():
        if not proxy_entries or not email_entries:
            messagebox.showerror("Error", "Please enter proxy and email lists.")
            return
        
        for proxy, email in zip(proxy_entries, email_entries):
            run_script(proxy, email)
            result_text.insert(tk.END, f"Success with proxy {proxy} for email {email}\n")

    main_form = tk.Tk()
    main_form.title("Proxy Email Scraper")

    # Создание и размещение элементов на форме
    proxy_label = tk.Label(main_form, text="Proxy List:")
    proxy_label.pack()

    proxy_text = scrolledtext.ScrolledText(main_form, width=40, height=10)
    proxy_text.pack()

    browse_proxy_button = tk.Button(main_form, text="Browse", command=browse_proxies)
    browse_proxy_button.pack()

    email_label = tk.Label(main_form, text="Email List:")
    email_label.pack()

    email_text = scrolledtext.ScrolledText(main_form, width=40, height=10)
    email_text.pack()

    browse_email_button = tk.Button(main_form, text="Browse", command=browse_emails)
    browse_email_button.pack()

    start_button = tk.Button(main_form, text="Start Script", command=start_script)
    start_button.pack()

    result_text = scrolledtext.ScrolledText(main_form, width=40, height=10)
    result_text.pack()
    main_form.protocol("WM_DELETE_WINDOW", root.quit)
    main_form.mainloop()


root = tk.Tk()
root.title("Login Form")

# Кнопка для аутентификации
login_button = tk.Button(root, text="Login", command=authenticate)
login_button.pack()

root.protocol("WM_DELETE_WINDOW", root.quit)
root.mainloop()