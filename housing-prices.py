from collections import OrderedDict
import itertools
import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas
import time


header1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
header2 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'upgrade-insecure-requests': '1',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
    }
header_list = [header1, header2]

def get_requests(url:str, boo:bool):
    """ Creates a list of requests for the city and type of request the user inputs.
    5 different url's of zillows houses for rent or sale are created and turned into 
    requests via requests.Session. 

    Args:
        input (list): A list of size 2 with index 0 containing the city and index 1 
        containing the type of request (for_sale or for_rent)

    Returns:
        A request for the url
    """
    # creates a requests that we fill with the different urls
    with requests.Session() as s:
        head = header_list[0] if boo else header_list[1]
        req = s.get(url, headers=head)
    return req


def get_input() -> list[str, str]:
    """ Requests user input on the city and type of search they would like

    Returns:
        list[str, str]: [city, requestType]
    """
    city = input('Enter a city you would like to search:\n').strip()
    req = input('Type: for_sale, for_rent:\n').lower()
    return [city, req]

def parse_details(details:str) -> list:
    """ parses through the details of the home into beds, baths, sqft, and the sale Type

    Args:
        details (str): the string that we parse

    Returns:
        list: [Beds, Bathrooms, Sqft, Sale info]
    """
    dSplit = details.split('-')
    split = re.split('[bds bd ba]+', dSplit[0])
    beds = split[0]
    bath = split[1]
    sqft = split[2]
    extra = dSplit[1].strip()
    ret = [beds, bath, sqft, extra]
    return ret

def parse_soup(request, dataframe):
    """ Pareses the list of pages for data we're interested in (address, price, size, link..etc)

    Args:
        soup_list (list): a list of objects containing the html code 
    """
    soup = BeautifulSoup(request.content, 'html.parser')
    houses_info = soup.find_all(class_='list-card-info')
    for house in houses_info:
        # zillow puts a class at the end for more attributes that we dont want
        if house.find(class_='') == None:
            continue
        try:
            address = house.find(class_='list-card-addr').text.strip()
            details = house.find(class_='list-card-details').text.strip()
            detail_split = parse_details(details)
            print(detail_split)
            price = house.find(class_='list-card-price').text.strip()
            link = house.find('a').get('href')
            # zillow stores some links without the initial part when directing 
            # the user to an appartment complex, so we add that on
            if link and link[0:22] != "https://www.zillow.com":
                link = "https://www.zillow.com" + link
            
        except Exception as err:
            print(err)

def main():
    input = get_input()
    city = input[0]
    search_type = input[1]
    # creates a list of urls representing the different pages on zillo
    boo = True
    data_frame = pandas.DataFrame()
    for i in range(1,11):
        url = (f'https://www.zillow.com/homes/{search_type}/{city}/{i}_p')
        request = get_requests(url, boo)
        parse_soup(request, data_frame)
        boo = not boo

if __name__ == "__main__":
    main()



