import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


# #url of the page we want to scrape
# url = "https://www.naukri.com/top-jobs-by-designations# desigtop600"
  
# # initiating the webdriver. Parameter includes the path of the webdriver.
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get(url) 
  
# # this is just to ensure that the page is loaded
# time.sleep(5) 
  
# html = driver.page_source
  
# # this renders the JS code and stores all
# # of the information in static HTML code.
  
# # Now, we could simply apply bs4 to html variable
# soup = BeautifulSoup(html, "html.parser")
# all_divs = soup.find('div', {'id' : 'nameSearch'})
# job_profiles = all_divs.find_all('a')
# # printing top ten job profiles
# count = 0
# for job_profile in job_profiles :
#     print(job_profile.text)
#     count = count + 1
#     if(count == 10) :
#         break
  
# driver.close() # closing the webdriver




URL = 'https://www.zillow.com/capitol-hill-seattle-wa/houses/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Capitol%20Hill%2C%20Seattle%2C%20WA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.33887483615112%2C%22east%22%3A-122.30012228030395%2C%22south%22%3A47.607042462212405%2C%22north%22%3A47.64036383721583%7D%2C%22mapZoom%22%3A15%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A250206%2C%22regionType%22%3A8%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22baths%22%3A%7B%22min%22%3A2%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(URL)
time.sleep(8)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
house_divs = soup.find('div', {'id': 'grid-search-results'})
houses = house_divs.find_all("div", class_="list-card-info")
numHouses = 0
for house in houses:
    try: 
        house_price = house.find('div', class_="list-card-price")
        house_details = house.find('ul', class_="list-card-details")
        
        links = house.find_all('a')
        print(links)
        
        # address = links.find('address', class_="list-card-addr")
        
        # print(address)
        print(house_price.text.strip())
        print(house_details.text.strip())
        numHouses +=1
    except:
        None
    
print(f"Number of houses: {numHouses}")
driver.close()

