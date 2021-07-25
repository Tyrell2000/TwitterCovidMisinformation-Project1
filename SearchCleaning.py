import bs4
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import datetime
import Search


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

haveOwnKeywords = False

if not haveOwnKeywords:
    keywords = ["Fauci", "coronavirus", "COVID-19", "delta", "Pfizer"]
else:
    keywords = []

    ## Allows the user to enter their own keywords to look for in webpages to save
    answer = input("Enter custom keyword to search for (Enter DONE when finished): ")

    while str(answer) != "DONE":
        keywords.append(str(answer))
        answer = input("Enter custom keyword to search for (Enter DONE when finished): ")

print("Keywords:", keywords)
# how many seeds you want
seedAnswer = input("How many seeds would you like to gather? ")
lastSeed = int(seedAnswer)
print("Seeds to Gather:", lastSeed)

# today's date
date = datetime.date.today().strftime('%Y-%m-%d')

# the name of the seed set file
seedFileName = "seedsset_" + str(date) + ".txt"

# clear the file, just in case there is anything inside of it
seedSet = open("SeedTexts/" + seedFileName, "w", encoding="utf-8")
seedSet.truncate(0)
seedSet.close()

seedSetUrls = []

textSaved = []

this = []

firstSeedValid = False


# write text of webpage from given url to the given file name
def writeWebpageText(url):
    writeThisSeed = False

    # open web page
    page = requests.get(url.strip())
    ##print(currentSeedNumber)
    ##print(urls[currentSeedNumber])

    # set soup equal to the webpage html contents
    soup = BeautifulSoup(page.content, 'html.parser')

    # get all text from the webpage
    texts = soup.findAll('p')

    # filter out invisible text in the html
    visible_texts = filter(tag_visible, texts)

    here = []
    # cleaning the text that's added to this seed's file
    for lineOfText in visible_texts:
        if lineOfText != "\n" and lineOfText != " ":
            # if you want the tags (<p>, <div>, ect still in, remove .get_text)

            text = []
            for x in lineOfText:
                if isinstance(x, bs4.element.NavigableString):
                    text.append(x.strip())

            for keyword in keywords:
                if keyword in " ".join(text):
                    if " ".join(text) not in here and " ".join(text) not in this:
                        ##print(keyword)
                        here.append(" ".join(text))
                        this.append(" ".join(text))
                        writeThisSeed = True

    if writeThisSeed:
        textSaved.append(here)
        seedSetUrls.append(url)
        if len(urls) != 1:
            del urls[-1]
        else:
            global firstSeedValid
            firstSeedValid = True
        print("Seeds Gathered:", str(len(seedSetUrls)) + "/" + str(lastSeed))
    else:
        if not writeThisSeed and firstSeedValid:
            print("Seeds Skipped:", str(len(urls) - 1))
        else:
            print("Seeds Skipped:", str(len(urls)))


# gather the seeds and add them to the list: urls, until you have *lastSeed* amount
def writeNewSeeds2(currentSeedNumber):
    if len(seedSetUrls) < lastSeed:
        # add seeds you want to put in the seed set to this list and they will be added later for processing
        nextSeeds = Search.get5Seeds(urls[currentSeedNumber], urls)
        ##print(nextSeeds, "\n")
    else:
        nextSeeds = []

    # for adding the next seed(s) to be added to the set
    for seed in nextSeeds:
        ##print(len(urls))
        ##print("next seed:", seed)
        if len(seedSetUrls) < lastSeed and seed not in urls:
            urls.append(seed)
            writeWebpageText(seed)
            ##print(len(urls))


seedSetLength = len(urls)
currentSeedNumber = 0
notAtLastSeed = True
writeWebpageText(urls[0])
# run until you have all the seeds needed
while notAtLastSeed:
    # call the code to add more seeds, won't add more if you have your desired amount already(lastSeed)
    writeNewSeeds2(currentSeedNumber)

    # update the stored length of the current seed set(urls)
    seedSetLength = len(seedSetUrls)

    # increment the current seed in the set by 1
    currentSeedNumber += 1

    # if you are at the last seed needed, stop the loop
    if lastSeed == seedSetLength:
        notAtLastSeed = False

##print(textSaved[0])

if firstSeedValid:
    del urls[0]

currentSeedNum = 0
seedSet = open("SeedTexts/" + seedFileName, "w", encoding="utf-8")
for text in textSaved:
    # create/open file for this seed, named after position in the list of seeds(urls) starting from 0
    currentSeed = open("SeedTexts/" + str(currentSeedNum) + ".txt", "w", encoding="utf-8")
    for lineOfText in text:
        if text != textSaved[-1:][0]:
            currentSeed.write(lineOfText)
            currentSeed.write("\n")
        else:
            currentSeed.write(lineOfText)
    if currentSeedNum == lastSeed - 1:
        seedSet.write(seedSetUrls[currentSeedNum])
    else:
        seedSet.write(seedSetUrls[currentSeedNum])
        seedSet.write("\n")
    currentSeedNum += 1

    # close the file associated with this seed. we are done adding text to it
    currentSeed.close()

seedSet.close()
