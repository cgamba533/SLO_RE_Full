from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def webListings():
    service = Service(executable_path=r'input_driver_path')
    driver = webdriver.Chrome(service=service)
    driver.get("input_web_url") # Url to be scrapped

    # Wait for the 'address-content' elements to be loaded
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'address-content')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup.prettify())

    response = soup.find_all('div', class_='address-content')

    driver.quit()

    print(response)

    data = []

    for item in response:
        data.append(item.text.strip())

    print(data)
    return data

extracted_data = webListings()
print(extracted_data)
