import requests
import re
from bs4 import BeautifulSoup


# TODO -- Accept the listing IDs that are found in Client


# The find_prices function will take in the reference ID that was pulled
# From discogs upon user searched and then stripped with regex too only have IDs
# To then scrape the current for sale prices since this doesn't exist natively through
# Discogs. IOt then returns a list of prices
def find_prices(vinyl_id):
    url = 'https://www.discogs.com/sell/list?master_id=' + (str(vinyl_id)) + '&ev=mb&format=Vinyl'
    listing_page = requests.get(url)
    price_fetch = BeautifulSoup(listing_page.text, 'lxml')
    prices = []
    for x in price_fetch.find_all('span', class_='price'):
        prices.append(x.text.strip())

    title = price_fetch.find('a', class_='item_description_title')
    title = title.text.strip('Shop')
    #print(f'Title searcher found: {title}')

    return prices, title


# The build average prices function takes in the price list from find_prices and scrapes them from anything
# that isn't a valid price - again using regex which I hate, but final project you know. When you
# become a big boy developer  https://regexr.com/ is very helpful. build_average_price returns the average
# vinyl price of the release
def price_structure(price_list):

    stripped_list = []
    # "Anyone who says they know regex is full of shit." - My grandmother

    trim_usd = re.compile(r'[^\d.,]+')
    for x in price_list:
        cleaned = trim_usd.sub('', x)
        stripped_list.append(float(cleaned.replace(',', '')))
    return stripped_list


def generate_average_price(stripped_list):
    price_sum = 0
    for price in stripped_list:
        price_sum += price

    average = (price_sum/len(stripped_list))

    return average
