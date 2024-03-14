from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

# Set up Selenium Firefox Driver
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

fp  = webdriver.FirefoxProfile("ff_profile")
options.profile = fp

service = Service(executable_path="/snap/bin/firefox.geckodriver")
driver = webdriver.Firefox(options=options, service=service) 

# Iterate through all years and months
for year in range(2018,2024):
    for month in range(12):
        # url = f'https://www.wunderground.com/history/monthly/us/ny/new-york-city/KLGA/date/{year}-{month}'
        # url = f"https://www.wunderground.com/history/monthly/us/tx/austin/KAUS/date/{year}-{month}"
        # url = f"https://www.wunderground.com/history/monthly/us/fl/miami/KMIA/date/{year}-{month}"
        url = f"https://www.wunderground.com/history/monthly/us/in/gary/KGYY/date/{year}-{month}"

        # This starts an instance of Firefox at the specified URL:
        driver.get(url)

        tables = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table")))

        new_table = pd.DataFrame()

        for table_idx, table in enumerate(tables):
            newTable = pd.read_html(table.get_attribute('outerHTML'))
            if newTable:
                if table_idx == 2:
                    new_table.insert(0,"Day",newTable[0][1:])
                    new_table.insert(0,"Month",newTable[0][0][0])
                    new_table.insert(0,"Year", year)
                if table_idx == 3:
                    new_table.insert(3,"Max Temp",newTable[0][0][1:])
                    new_table.insert(4,"Avg Temp", newTable[0][1][1:])
                    new_table.insert(5,"Min Temp", newTable[0][2][1:])
                if table_idx == 4:
                    new_table.insert(6,"Max Dew Point",newTable[0][0][1:])
                    new_table.insert(7,"Avg Dew Point", newTable[0][1][1:])
                    new_table.insert(8,"Min Dew Point", newTable[0][2][1:])
                if table_idx == 5:
                    new_table.insert(9,"Max Humidity",newTable[0][0][1:])
                    new_table.insert(10,"Avg Humidity", newTable[0][1][1:])
                    new_table.insert(11,"Min Humidity", newTable[0][2][1:])
                if table_idx == 6:
                    new_table.insert(12,"Max Wind Speed",newTable[0][0][1:])
                    new_table.insert(13,"Avg Wind Speed", newTable[0][1][1:])
                    new_table.insert(14,"Min Wind Speed", newTable[0][2][1:])
                if table_idx == 7:
                    new_table.insert(15,"Max Pressure",newTable[0][0][1:])
                    new_table.insert(16,"Avg Pressure", newTable[0][1][1:])
                    new_table.insert(17,"Min Pressure", newTable[0][2][1:])

        with open("chicago.csv"):
            new_table.to_csv("chicago.csv", mode='a', index=False, header=False)

driver.quit()
