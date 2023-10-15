import time
import psutil
from seleniumwire import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from faker import Faker

driver_path = 'C:/webdrivers/chromedriver.exe'
email_file_path = 'C:/Users/nazar/OneDrive/Desktop/email.txt'
proxy_file_path = 'C:/Users/nazar/OneDrive/Desktop/proxi.txt'  
trace_extension_path = 'C:/Users/nazar/AppData/Local/Google/Chrome/User Data/Profile/Extensions/njkmjblmcfiobddjgebnoeldkjcplfjb/3.0.6_0'
password_file_path = 'C:/Users/nazar/OneDrive/Desktop/password.txt'

# Read emails from the file into a list
with open(email_file_path, 'r') as email_file:
    emails = email_file.read().splitlines()

# Read proxies from the file into a list
with open(proxy_file_path, 'r') as proxy_file:
    proxies = proxy_file.read().splitlines()

with open(password_file_path, 'r') as password_file:
    passwords = password_file.read().splitlines()

# Make sure there are enough proxies for the emails
if len(proxies) < len(emails):
    raise ValueError("Not enough proxies for the number of emails")
proxy_email_pairs = zip(proxies, emails, passwords)
for proxy_url, email, password in proxy_email_pairs:
    chrome_options = Options()
    chrome_options.headless = False 
    chrome_options.add_argument(f'--user-data-dir=c:/Users/nazar/AppData/Local/Google/Chrome/User Data/Profile 4')
    chrome_options.add_argument(f'--load-extension={trace_extension_path}')  
    chrome_options.add_argument('--incognito')
    driver = uc.Chrome(executable_path=driver_path, options=chrome_options, seleniumwire_options={'proxy': {'https': proxy_url}})
    try:
        driver.get('https://konto.onet.pl/')
        wait = WebDriverWait(driver, 20)
        modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cmp-intro_intro')))
        button = driver.find_element(By.CSS_SELECTOR, '.cmp-button_button.cmp-intro_rejectAll.cmp-button_invert')
        button.click()
        modal_next = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cmp-popup_content')))
        button_disagree = driver.find_element(By.CSS_SELECTOR, '.cmp-button_button.cmp-intro_rejectAll.cmp-button_invert')
        button_disagree.click()      

        email_field = driver.find_element(By.NAME, 'email')
        email_field.clear()  
        email_field.send_keys(email)  

        next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-ca90c2ac-0.daaXLN"))
                )
        next_button.click()
        time.sleep(10)

        password_field = driver.find_element(By.NAME, 'password')
        password_field.clear()
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chakra-checkbox__control.css-nxy0t9"))
        )
        login_button.click()
        time.sleep(10)

    except Exception as e:
        print(f'Error with proxy {proxy_url} for email {email}: {str(e)}')
    
    finally:
        driver.quit()
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if 'chrome' in process.info['name'].lower():  
                try:
                    psutil.Process(process.info['pid']).terminate()
                except psutil.NoSuchProcess:
                    pass

    time.sleep(20)
    print(f'Success with proxy {proxy_url} for email: {email}')
