# Zillow Prices
A program used to scrape the prices of homes on zillow. Can be used for both renting and buying homes. Prompts the user for the city they are interested in and what type of field they are interested in (renting or buying). Gives the user a list of homes based on the price per sqare footage to value the homes. Housing info
is written into house_info.txt. 

Due to Zillow returning Captcha pages if you try to open their website too many times, only a limited number of homes can be shown. Headers have been added to the page requests but it is not a 100% solution. So note that the properties in house_info.txt is not the full list of houses. 

To run, run 'python3 housing-prices.py' in terminal.
