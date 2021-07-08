import requests
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
from urllib.parse import urlparse
import datetime

seedURL = 'https://thehill.com/policy/healthcare/public-global-health/561627-pfizer-vaccine-less-effective-against-delta-variant'
date = datetime.date.today().strftime('%Y-%m-%d')
#txtName = seedURL + '_' + str(date)
txtName = 'seedsset' + '_' + str(date)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = seedURL
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
baseLink = urlparse(url).netloc

txt = open(txtName + '.txt', "w+", encoding="utf-8")
txt.close()

#txtContent = list(open(txtName + '.txt', 'r'))
#print(len(list(open(txtName + '.txt', 'r'))))
#print(list(txtContent))

counter = 0
for link in soup.find_all('a'):
        txt = open(txtName + '.txt', 'a', encoding="utf-8")
        getLink = link.get('href')

        if getLink[0] == '/':
                getLink = 'http://' + baseLink + getLink

        if getLink + '\n' not in list(open(txtName + '.txt', 'r')):
                #print(list(open(txtName + '.txt', 'r')))
                if link.get('href')[0] == '/' or 'http://' in link.get('href'):
                        print(getLink)
                        if link.get('href')[0] == '/':
                                txt.write('http://' +  urlparse(url).netloc + link.get('href'))

                        elif 'http://' in link.get('href'):
                                txt.write(link.get('href'))

                        counter = counter + 1
                        txt.write('\n')
                        txt.close()
        if counter == 5:
                break


for URL in open(txtName + '.txt', 'r'):
        #print('url: '+ URL)
        if len(list(open(txtName + '.txt', 'r'))) >= 1000:
                break
        url = URL
        page = requests.get(url.strip())
        soup = BeautifulSoup(page.content, 'html.parser')
        baseLink = urlparse(url).netloc
        #print(urlparse(url).netloc)
        #print('BaseLink:' + baseLink)
        counter=0
        for link in soup.find_all('a'):
                if len(link.get('href')) > 0:
                        txt = open(txtName + '.txt', 'a', encoding="utf-8")
                        getLink = link.get('href')

                        if getLink[0] == '/':
                                getLink = 'http://' + baseLink + getLink
                        if getLink + '\n' not in list(open(txtName + '.txt', 'r')):
                                #print(list(open(txtName + '.txt', 'r')))
                                if link.get('href')[0] == '/' or 'http://' in link.get('href'):
                                        print(getLink)
                                        if link.get('href')[0] == '/':
                                                #print('if / is in link:' + urlparse(url).netloc + link.get('href'))
                                                txt.write('http://' + urlparse(url).netloc + link.get('href'))

                                        elif 'http://' in link.get('href'):
                                                #print('if / is not in link:' + urlparse(url).netloc + link.get('href'))
                                                txt.write(link.get('href'))

                                        counter = counter + 1
                                        txt.write('\n')
                                        txt.close()
                        if counter == 5:
                                break