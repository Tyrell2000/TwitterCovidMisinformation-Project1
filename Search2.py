import requests
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
from urllib.parse import urlparse
import datetime

seedURL = 'https://thehill.com/policy/healthcare/public-global-health/561627-pfizer-vaccine-less-effective-against-delta-variant'
date = datetime.date.today().strftime('%Y-%m-%d')
# csvName = seedURL + '_' + str(date)
csvName = 'seedsset' + '_' + str(date)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = seedURL
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
baseLink = urlparse(url).netloc

csv = open(csvName + '.csv', "w+", encoding="utf-8")
csv.close()

# csvContent = list(open(csvName + '.csv', 'r'))
# print(len(list(open(csvName + '.csv', 'r'))))
# print(list(csvContent))

urls = []

counter = 0
for link in soup.find_all('a'):
    csv = open(csvName + '.csv', 'a', encoding="utf-8")
    getLink = link.get('href')

    if getLink[0] == '/':
        getLink = 'http://' + baseLink + getLink

    if getLink + '\n' not in list(open(csvName + '.csv', 'r')):
        # print(list(open(csvName + '.csv', 'r')))
        if link.get('href')[0] == '/' or 'http://' in link.get('href'):
            ##print(getLink)
            if link.get('href')[0] == '/':
                csv.write('http://' + urlparse(url).netloc + link.get('href'))

            elif 'http://' in link.get('href') and link.get('href') not in urls:
                urls.append(link.get('href'))
                csv.write(link.get('href'))

            counter = counter + 1
            csv.write('\n')
            csv.close()
    if counter == 5:
        break

for URL in open(csvName + '.csv', 'r'):
    # print('url: '+ URL)
    if len(list(open(csvName + '.csv', 'r'))) >= 1000:
        break
    url = URL
    page = requests.get(url.strip())
    soup = BeautifulSoup(page.content, 'html.parser')
    baseLink = urlparse(url).netloc
    # print(urlparse(url).netloc)
    # print('BaseLink:' + baseLink)
    counter = 0
    for link in soup.find_all('a'):
        if len(link.get('href')) > 0:
            csv = open(csvName + '.csv', 'a', encoding="utf-8")
            getLink = link.get('href')

            if getLink[0] == '/':
                getLink = 'http://' + baseLink + getLink
            if getLink + '\n' not in list(open(csvName + '.csv', 'r')):
                # print(list(open(csvName + '.csv', 'r')))
                if link.get('href')[0] == '/' or 'http://' in link.get('href'):
                    print(len(urls), ": " + getLink)
                    if link.get('href')[0] == '/' and getLink not in urls:
                        urls.append(getLink)
                        # print('if / is in link:' + urlparse(url).netloc + link.get('href'))
                        csv.write('http://' + urlparse(url).netloc + link.get('href'))

                    elif 'http://' in link.get('href'):
                        # print('if / is not in link:' + urlparse(url).netloc + link.get('href'))
                        csv.write(link.get('href'))

                    counter = counter + 1
                    csv.write('\n')
                    csv.close()
            if counter == 5:
                break
