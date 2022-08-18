from collections import OrderedDict
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas
import numpy as np

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
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}
header_list = [header1, header2]

detailsTest = ["$3,199+ 2 bds", '$1,936+ 1 bd$2,968+ 2 bds', '$2,936+ 1 bd$3,554+ 2 bds$4,950+ 3 bds',
               '4 bds2 ba2,000 sqft- House for rent', 'Studio1 ba311 sqft- Apartment for rent']


def get_requests(url: str, boo: bool):
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


def parse_soup(request, pageLists: list[dict]):
    """Pareses the list of pages for data we're interested in (address, price, size, link..etc)

    Args:
        request (page session): the page to parse through for data
        pageLists (list): a list of dictionaries containing the house info 

    """
    soup = BeautifulSoup(request.content, 'html.parser')
    houses_info = soup.find_all(class_='list-card-info')
    if not houses_info:
        return
    for house in houses_info:
        # zillow puts a class at the end for more attributes that we dont want
        if house.find(class_='') == None:
            continue
        try:
            address = house.find(class_='list-card-addr').text.strip()
            details = house.find(class_='list-card-details').text.strip()
            price = house.find(class_='list-card-price').text.strip()
            link = house.find('a').get('href')
            # zillow stores some links without the initial part when directing
            # the user to an appartment complex, so we add that on
            if link and link[0:22] != "https://www.zillow.com":
                link = "https://www.zillow.com" + link
            dict = {'price': price, 'address': address,
                    'details': details, 'link': link}
            pageLists.append(dict)
        except Exception as err:
            print(err)


def write_to_file(file, df, city, search_type):
    """Writes property info to text file

    Args:
        file (File): File containing property info
        df (DataFrame): A dataframe containing all the property info
        city (str): the city the user is interested in
        search_type (str): the search type the user wanted
    """
    if search_type == 'for_sale':
        file.write(f"{city} Homes for Sale:\n")
    else:
        file.write(f"{city} Homes/Appartments for Rent:\n")
    file.write(df.to_string())


def main():
    input = get_input()
    city = input[0]
    search_type = input[1]
    # creates a list of urls representing the different pages on zillo
    boo = True
    pageLists = []
    # creates the requests one at a time after the last request has been processed
    for pageNum in range(1, 11):
        url = (
            f'https://www.zillow.com/homes/{search_type}/{city}/{pageNum}_p')
        request = get_requests(url, boo)
        parse_soup(request, pageLists)
        boo = not boo
    if not pageLists:
        print(print('No return from Zillow (captcha block)'))
        exit()
    df = pandas.DataFrame(pageLists, columns=[
                          'price', 'address', 'details', 'link'])
    file = open('house_info.txt', 'w')
    write_to_file(file, df, city, search_type)
    file.close()


if __name__ == "__main__":
    main()
