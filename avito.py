from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.options import Options
import pandas as pd
import re

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://www.avito.ru/moskva_i_mo/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?cd=1&f=ASgBAQICAUSwwQ2I_DcCQOTgDbSIwlyKwlyMwlyOwlyQwlyGwlyEwlyCwlyAwlz~wVz8wVzm4A2U~sFc~MFc9sFc9MFc6MFc6sFc7sFc8MFc8sFc")

print("Firefox opened! Script is running");

csv_file = open("avito.csv", "w")
pd_csv_file = pd.DataFrame(columns = ['href', 'title', 'price', 'description', 'memory', 'ram', 'sys'])
    
for j in range(2):
    time.sleep(1)

    title = driver.find_elements(By.CLASS_NAME, "iva-item-titleStep-pdebR")
    price = driver.find_elements(By.CLASS_NAME, "iva-item-priceStep-uq2CQ")
    description = driver.find_elements(By.CLASS_NAME, "iva-item-descriptionStep-C0ty1")
    href = driver.find_elements(By.CLASS_NAME, "iva-item-sliderLink-uLz1v")
    ram_memory = driver.find_elements(By.CLASS_NAME, "iva-item-autoParamsStep-WzfS8")

    for i in range(len(title)):
        str = ram_memory[i].text
        str = str.split()
        str = ''.join(str)
        str_split = str.split(',')
        fragment = 'дюйм'
        new_str = []
        for word in str_split:
            if fragment not in word:
                new_str.append(word)
        str = ','.join(new_str)
        str = re.sub(r'[А-Я]+\s?', '', str).strip()
        str = re.findall(r'[-+]?(?:\d*\.*\d+)', str)
        str[1] = float(str[1])
        if str[1] > 18:
            str[1] = str[1]/1000
        
        sys = " "
        if ('iPhone' or 'Iphone' or 'IPhone' or 'iphone') in title[i].text:
            sys = "ios"
        else:
            sys = "android"
        
        price_int = re.sub(r'[^\d,.]', '', price[i].text)
        
        pd_csv_file.loc[len(pd_csv_file.index)] = [href[i].get_attribute('href'), title[i].text, price_int, description[i].text, int(str[0]), float(str[1]), sys]
        pd_csv_file.to_csv('avito.csv', sep = '|')
        if i == 50:
            break

    time.sleep(2)
    element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[3]/div[3]/div[3]/div[1]/span[9]")
    element.click()

print(pd_csv_file)
csv_file.close()
driver.quit()
print("Script is finished!")
