import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas
import time


# URL = 'https://www.zillow.com/homes/for_sale/house_type/2.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.42466792853007%2C%22east%22%3A-122.2696577051414%2C%22south%22%3A47.597721274571754%2C%22north%22%3A47.73090310403484%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22baths%22%3A%7B%22min%22%3A2%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D'
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get(URL)
# time.sleep(8)

# html = driver.page_source

# soup = BeautifulSoup(html, 'html.parser')
# add = soup.find_all(class_='list-card-addr')
# house_divs = soup.find('div', {'id': 'grid-search-results'})
# houses = house_divs.find_all("div", class_="list-card-info")
# numHouses = 0

def get_requests(input:list) -> list:
    """ Creates a list of requests for the city and type of request the user inputs.
    5 different url's of zillows houses for rent or sale are created and turned into 
    requests via requests.Session. 

    Args:
        input (list): A list of size 2 with index 0 containing the city and index 1 
        containing the type of request (for_sale or for_rent)

    Returns:
        list: returns a len(5) list of requests
    """
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    city = input[0]
    search_type = input[1]
    
    # creates a list of urls representing the different pages on zillo
    urls = []
    for i in range(1,6):
        urls.append(f'https://www.zillow.com/homes/{search_type}/{city}/{i}_p')
    # creates a list of requests that we fill with the different urls
    reqList = []
    with requests.Session() as s:
        for url in urls:
            req = s.get(url, headers=header)
            reqList.append(req)
    return reqList

def get_input() -> list[str, str]:
    """ Requests user input on the city and type of search they would like

    Returns:
        list[str, str]: [city, requestType]
    """
    city = input('Enter a city you would like to search:\n').strip()
    city = 'seattle'
    req = input('Type: for_sale, for_rent:\n').lower()
    return [city, req]

def make_soup(reqList:list) -> list[BeautifulSoup]:
    """ Creates a list of 'soup' objects using the list of requests. 

    Args:
        reqList (list): a list of requests for different pages of Zillow

    Returns:
        list[BeautifulSoup]: a list of objects containing the html code 
    """
    soup_list = []
    for req in reqList:
        soup_list.append(BeautifulSoup(req.content, 'html.parser'))
    return soup_list

def parse_soup(soup_list:list):
    """ Pareses the list of pages for data we're interested in (address, price, size, link..etc)

    Args:
        soup_list (list): a list of objects containing the html code 
    """
    dataFrame = pandas.DataFrame()
    for soup in soup_list:
        print(soup)
        for i in soup:
            addr = soup.find_all(class_='list-card-addr')
            details = soup.find_all(class_='list-card-details')
            price = soup.find_all(class_='list-card-price')
            links = soup.find_all(class_='list-card-link')
            dataFrame['prices'] = price
            dataFrame['addr'] = addr
    print(dataFrame)
            
    

def main():
    input = get_input()
    requestList = get_requests(input)
    soups = make_soup(requestList)
    parse_soup(soups)
    
    
if __name__ == "__main__":
    main()



