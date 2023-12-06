import re
import requests
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile
import shutil

from params import LOCAL_EXTRACTED_FOLDER, LOCAL_DOWNLOAD_FOLDER

DOMAIN = "https://www.nhc.noaa.gov/gis/" 
URL = DOMAIN + "/archive_forecast_results.php?id=al18&year=2012&name=Hurricane%20SANDY"

for folder in [LOCAL_DOWNLOAD_FOLDER, LOCAL_EXTRACTED_FOLDER]:
    if not folder.exists():
        folder.mkdir(parents=True)

def _get_soup(url):
    return bs(requests.get(url).text, 'html.parser')


def download_zips(url=URL, domain=DOMAIN):
    """
    Download all .zip files linked in the provided url
    """
    for link in _get_soup(url).findAll("a", attrs={'href': re.compile(".zip")}):

        file_link = link.get('href')
        print(f"Downloading {file_link}")

        with open(LOCAL_DOWNLOAD_FOLDER / link.text, 'wb') as file:
            response = requests.get(domain + file_link)
            file.write(response.content)

def extract_all_zip_files():

    for z in LOCAL_DOWNLOAD_FOLDER.rglob("*.zip"):
        with ZipFile(z, 'r') as zf:
            zf.extractall(path=LOCAL_EXTRACTED_FOLDER)

def cleanup():
    shutil.rmtree(LOCAL_DOWNLOAD_FOLDER)
    shutil.rmtree(LOCAL_EXTRACTED_FOLDER)
