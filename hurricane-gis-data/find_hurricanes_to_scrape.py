import re
from bs4 import BeautifulSoup as bs
import requests

DOMAIN = "https://www.nhc.noaa.gov" 


def _get_soup(url):
    return bs(requests.get(url).text, 'html.parser')


def _get_urls_for_single_year(year):

    urls = []

    soup = _get_soup(f"https://www.nhc.noaa.gov/gis/archive_forecast.php?year={year}")

    for link in soup.findAll("a", attrs={'href': re.compile("archive_forecast_results")}):
        url = DOMAIN + link.get('href').replace(" ", "%20")
        # print(url)
        urls.append(url)

    return urls


def url_for_every_storm():

    urls = []
    for year in range(2008, 2024):
        # print(year)
        urls_for_this_year = _get_urls_for_single_year(year)

        for url in urls_for_this_year:
            urls.append(url)

    return urls
