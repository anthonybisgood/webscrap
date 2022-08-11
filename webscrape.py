from tkinter import Variable
import requests
from bs4 import BeautifulSoup




def get_raw(url: str) -> Variable:
    """Opens the url with the given id and uses
    Beautiful soup to extract the raw html code

    Args:
        url (str): The URL we are trying to get data from
        ID (str): The ID that we are 
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    try:
        results = soup.find("table", class_="ticker")
        return results
    except Exception as err:
        print(err)
        return err

def parse_html(rawHtml:str, wrapper:str, className:str):
    elements = rawHtml.find("div", class_="ticker")
    # for element in elements:
    #     try:
    #         title_element = element.find("h2", class_="title")
    #         company_element = element.find("h3", class_="company")
    #         location_element = element.find("p", class_="location")
    #         print(title_element.text.strip())
    #         print(company_element.text.strip())
    #         print(location_element.text.strip())
    #         print()
    #     except Exception as err:
    #         print(err)
    #         return err

def getLinks(parsedHtml:str):   
    pythonJobs = parsedHtml.find_all(
        "a", string=lambda text: "ticker" in text.lower()
    )
    pythonJobElements = [h2_element.parent.parent.parent for h2_element in pythonJobs]
    for jobElement in pythonJobElements:
        # print(jobElement.text.strip())
        # To get links
        links = jobElement.find_all("a")
        for link in links:
            print(link)
            link_URL= link["href"]
            print(f"Apply here: {link_URL}\n")
            
def main(url: str):
    raw = get_raw(url)
    # print(raw)
    #parsedHtml = self.parse_html(raw, "wrapper(div..etc)", "className")
    getLinks(raw)
        
if __name__ == "__main__":
    url = "https://www.investors.com/news/esg-companies-list-best-esg-stocks-environmental-social-governance-values/"
    main(url)
    


