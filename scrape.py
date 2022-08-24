from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv 
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
START_URL = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome('chromedriver.exe')
browser.get(START_URL)
time.sleep(10)
planet_data = []
new_planet_data = []
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period",'eccentricity']
def scrape():
    for i in range (0,428):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,'html.parser')
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value")) 
            if current_page_num < i: 
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click() 
            elif current_page_num > i: 
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click() 
            else: 
                break

        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    hyperlink_li_tag = li_tags[0]
                    temp_list.append('https://exoplanets.nasa.gov'+ hyperlink_li_tag.find_all("a",href=True)[0]['href'])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            planet_data.append(temp_list)
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a'))).click()
        print(f"{i} page done 1")
    with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)
scrape()

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,'html.parser')
        temp_list = []
        for tr_tags in soup.find_all('tr',attrs= {'class':'fact_row'}):
            td_tags = tr_tags.find_all('td')
            for td_tag in td_tags: 
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0]) 
                except: 
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
for index,data in enumerate(planet_data):
    scrape_more_data(data[5])
    print(f'scraping at hyperlink {index+1} is completed')
print(new_planet_data[0:10])
final_planet_data = []
for index,data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)
with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)
    

