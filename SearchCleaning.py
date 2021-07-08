import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
from pandas import DataFrame


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url1 = 'https://thehill.com/policy/healthcare/public-global-health/561627-pfizer-vaccine-less-effective-against-delta-variant'
url2 = 'https://www.cnn.com/2021/07/06/politics/republican-candidates-trump-election-lie/index.html'
url3 = 'https://www.cdc.gov/'
urls = [url1, url2, url3]

seedSet = open("seedSet.txt", "a", encoding="utf-8")
seedSet.truncate(0)

for urlNumber in range(len(urls)):
    page = requests.get(urls[urlNumber], headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)

    currentSeed = open(str(urlNumber) + ".txt", "w", encoding="utf-8")

    for lineOfText in visible_texts:
        if lineOfText != "\n" and lineOfText != " ":
            currentSeed.write(re.sub('[\t\n]', "", lineOfText))
            currentSeed.write("\n")

    currentSeed.close()

    seedSet = open("seedSet.txt", "a", encoding="utf-8")
    seedSet.write(urls[urlNumber])
    seedSet.write("\n")
    seedSet.close()
