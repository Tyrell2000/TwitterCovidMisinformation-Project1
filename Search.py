import requests
from bs4 import BeautifulSoup
import re
from pandas import DataFrame

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = 'https://thehill.com/policy/healthcare/public-global-health/561627-pfizer-vaccine-less-effective-against-delta-variant'
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

print(soup)
