import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import datetime
import Search
from pandas import DataFrame


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/50.0.2661.102 Safari/537.36'}
url1 = 'https://thehill.com/policy/healthcare/public-global-health/561627-pfizer-vaccine-less-effective-against-delta' \
       '-variant'
url2 = 'https://www.cnn.com/2021/07/06/politics/republican-candidates-trump-election-lie/index.html'
url3 = 'https://www.cdc.gov/'
url4 = 'https://www.foxnews.com/us/rescuers-at-florida-condo-collapse-told-they-can-go-home-but-they-refuse'
urls = [url1]

# change this, depending on if you have a file with urls(a seed set) already. True to use an existing file, False to
# create one
# ignore this
'''alreadyHaveSeedSet = False'''

# how many seeds you want
lastSeed = 100

# today's date
date = datetime.date.today().strftime('%Y-%m-%d')

# the name of the seed set file
seedFileName = "seedsset_" + str(date) + ".txt"

# clear the file, just in case there is anything inside of it
seedSet = open(seedFileName, "w", encoding="utf-8")
seedSet.truncate(0)
seedSet.close()

# open the file with the seed set and clear it. set alreadyHaveSeedSet to False if you want to load a seed set
# from a file
# ignore this
'''if not alreadyHaveSeedSet:
    seedSet = open(seedFileName, "w", encoding="utf-8")
    seedSet.truncate(0)
    seedSet.close()'''

# use this loop if you want to load a seed set from a file. just change the file name and set alreadyHaveSeedSet to
# True to activate this loop
## ignore this
'''if alreadyHaveSeedSet:
    urls = []
    seedSet = open("seedsset_2021-07-08.txt", "r", encoding="utf-8")
    for url in seedSet.readlines():
        urls.append(url[:-2])'''


# write text of webpage from given url to the given file name
def writeWebpageText(url, fileNumber):
    # open web page
    page = requests.get(url, headers=headers)
    ##print(currentSeedNumber)
    ##print(urls[currentSeedNumber])

    # set soup equal to the webpage html contents
    soup = BeautifulSoup(page.content, 'html.parser')

    # get all text from the webpage
    texts = soup.findAll(text=True)

    # filter out invisible text in the html
    visible_texts = filter(tag_visible, texts)

    # create/open file for this seed, named after position in the list of seeds(urls) starting from 0
    currentSeed = open(fileNumber + ".txt", "w", encoding="utf-8")

    # cleaning the text that's added to this seed's file
    for lineOfText in visible_texts:
        if lineOfText != "\n" and lineOfText != " ":
            currentSeed.write(re.sub('[\t\n]', "", lineOfText))
            currentSeed.write("\n")

    # close the file associated with this seed. we are done adding text to it
    currentSeed.close()


# gather the seeds and write them directly to the given file    ###not in use
def writeNewSeeds(seedset):
    if len(urls) < lastSeed:
        # add seeds you want to put in the seed set to this list and they will be added later for processing
        nextSeeds = Search.get5Seeds(urls[currentSeedNumber], urls)
    else:
        nextSeeds = []

    # for adding the next seed(s) to be added to the set
    for seed in nextSeeds:
        print(len(urls))
        ##print("next seed:", seed)
        seedSet.write(seed)
        urls.append(seed)

        if len(urls) == lastSeed:
            if seed != urls[lastSeed - 1]:
                seedSet.write("\n")
            else:
                seedSet.write("")
        else:
            seedSet.write("\n")


# gather the seeds and add them to the list: urls, until you have *lastSeed* amount
def writeNewSeeds2(currentSeedNumber):
    if len(urls) < lastSeed:
        # add seeds you want to put in the seed set to this list and they will be added later for processing
        nextSeeds = Search.get5Seeds(urls[currentSeedNumber], urls)
    else:
        nextSeeds = []

    # for adding the next seed(s) to be added to the set
    for seed in nextSeeds:
        ##print(len(urls))
        ##print("next seed:", seed)
        if len(urls) < lastSeed and seed not in urls:
            urls.append(seed)
            print(len(urls))


seedSetLength = len(urls)
currentSeedNumber = 0
notAtLastSeed = True
# run until you have all the seeds needed
while notAtLastSeed:
    # call the code to add more seeds, won't add more if you have your desired amount already(lastSeed)
    writeNewSeeds2(currentSeedNumber)

    # update the stored length of the current seed set(urls)
    seedSetLength = len(urls)

    # increment the current seed in the set by 1
    currentSeedNumber += 1

    # if you are at the last seed needed, stop the loop
    if currentSeedNumber == seedSetLength:
        notAtLastSeed = False

# write urls to seed set file
number = 0
for url in urls:
    # calls the code to write text of url's webpage to a file
    writeWebpageText(url, str(number))
    seedSet = open(seedFileName, "a", encoding="utf-8")

    # basically, if not the last url, add a newline after adding the url to the seed set
    if url != urls[lastSeed - 1]:
        seedSet.write(url)
        seedSet.write("\n")
    else:
        seedSet.write(url)
    number += 1
    seedSet.close()