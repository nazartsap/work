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
faker = Faker()

# Read emails from the file into a list
with open(email_file_path, 'r') as email_file:
    emails = email_file.read().splitlines()

# Read proxies from the file into a list
with open(proxy_file_path, 'r') as proxy_file:
    proxies = proxy_file.read().splitlines()

# Make sure there are enough proxies for the emails
if len(proxies) < len(emails):
    raise ValueError("Not enough proxies for the number of emails")
proxy_email_pairs = zip(proxies, emails)
for proxy_url, email in proxy_email_pairs:
    chrome_options = Options()
    chrome_options.headless = False 
    chrome_options.add_argument('--disable-cookies')
    chrome_options.add_argument(f'--user-data-dir=c:/Users/nazar/AppData/Local/Google/Chrome/User Data/Profile 8')
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
