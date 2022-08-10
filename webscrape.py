from tkinter import Variable
import requests
from bs4 import BeautifulSoup


class Webscrape:
    def __init__(self):
        None

    def get_raw(self, url: str, ID: str) -> Variable:
        """Opens the url with the given id and uses
        Beautiful soup to extract the raw html code

        Args:
            url (str): The URL we are trying to get data from
            ID (str): The ID that we are 
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            results = soup.find(id=ID)
            return results
        except Exception as err:
            print(err)
            return err

    def parse_html(self, rawHtml:str, wrapper:str, className:str):
        elements = rawHtml.find_all("div", class_="card-content")
        for element in elements:
            try:
                title_element = element.find("h2", class_="title")
                company_element = element.find("h3", class_="company")
                location_element = element.find("p", class_="location")
                print(title_element.text.strip())
                print(company_element.text.strip())
                print(location_element.text.strip())
                print()
            except Exception as err:
                print(err)
                return err
    
    def getLinks(self, parsedHtml:str):   
        pythonJobs = parsedHtml.find_all(
            "h2", string=lambda text: "python" in text.lower()
        )
        pythonJobElements = [h2_element.parent.parent.parent for h2_element in pythonJobs]
        for jobElement in pythonJobElements:
            # print(jobElement.text.strip())
            # To get links
            links = jobElement.find_all("a")
            for link in links:
                link_URL= link["href"]
                print(f"Apply here: {link_URL}\n")
                
    def main(self, url: str, id: str):
        raw = self.get_raw(url, id)
        parsedHtml = self.parse_html(raw, "wrapper(div..etc)", "className")
        self.getLinks(raw)
        
        

x = Webscrape()
x.main("https://realpython.github.io/fake-jobs/", "ResultsContainer")
