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

# change this, depending on if you have a file with urls(a seed set) already. True to use an existing file, False to
# create one
alreadyHaveSeedSet = False

# open the file with the seed set and clear it. set alreadyHaveSeedSet to False if you want to load a seed set
# from a file
if not alreadyHaveSeedSet:
    seedSet = open("seedSet.txt", "a", encoding="utf-8")
    seedSet.truncate(0)

# use this loop if you want to load a seed set from a file. just change the file name and set alreadyHaveSeedSet to
# True to activate this loop
if alreadyHaveSeedSet:
    urls = []
    seedSet = open("seedSet.txt", "r", encoding="utf-8")
    for url in seedSet.readlines():
        urls.append(url)

# go through every url in the list(code equivalent of seed set)
for urlNumber in range(len(urls)):
    # open web page
    page = requests.get(urls[urlNumber], headers=headers)

    # set soup equal to the webpage html contents
    soup = BeautifulSoup(page.content, 'html.parser')

    # get all text from the webpage
    texts = soup.findAll(text=True)

    # filter out invisible text in the html
    visible_texts = filter(tag_visible, texts)

    # create/open file for this seed, named after number in the list of seeds starting from 0
    currentSeed = open(str(urlNumber) + ".txt", "w", encoding="utf-8")

    # cleaning the text that's added to this seed's file
    for lineOfText in visible_texts:
        if lineOfText != "\n" and lineOfText != " ":
            currentSeed.write(re.sub('[\t\n]', "", lineOfText))
            currentSeed.write("\n")

    # close the file associated with this seed. we are done adding text to it
    currentSeed.close()

    if not alreadyHaveSeedSet:
        # open the seed list text file
        seedSet = open("seedSet.txt", "a", encoding="utf-8")

        # write the current url to the seed list file
        seedSet.write(urls[urlNumber])

        # add a new line to separate the current url and the next url
        if urlNumber != len(urls) - 1:
            seedSet.write("\n")

        # close the file associated with the seed set. we are done adding urls to it
        seedSet.close()
