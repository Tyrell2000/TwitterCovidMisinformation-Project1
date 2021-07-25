import bs4
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
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

lastSeed = 10

# today's date
date = datetime.date.today().strftime('%Y-%m-%d')

# the name of the seed set file
seedFileName = "seedsset_" + str(date) + ".txt"

# clear the file, just in case there is anything inside of it
seedSet = open("SeedTexts/" + seedFileName, "w", encoding="utf-8")
seedSet.truncate(0)
seedSet.close()

seedSetLength = len(urls)
currentSeedNumber = 0
notAtLastSeed = True
this = []
# run until you have all the seeds needed
while notAtLastSeed:
    # call the code to add more seeds, won't add more if you have your desired amount already(lastSeed)
    if len(urls) < lastSeed:
        # add seeds you want to put in the seed set to this list and they will be added later for processing
        nextSeeds = Search.get5Seeds(urls[currentSeedNumber], urls)
        ##print(nextSeeds, "\n")
    else:
        nextSeeds = []

    # for adding the next seed(s) to be added to the set
    for seed in nextSeeds:
        if len(urls) < lastSeed and seed not in urls:
            urls.append(seed)
            print("Seeds left to gather: ", lastSeed - len(urls) + 1)
            ##print(len(urls))

    keywords = ["Fauci", "coronavirus", "COVID-19", "delta", "Pfizer"]

    # create/open file for this seed, named after position in the list of seeds(urls) starting from 0
    currentSeed = open("SeedTexts/" + str(currentSeedNumber) + ".txt", "w", encoding="utf-8")

    # open web page
    page = requests.get(urls[currentSeedNumber].strip())

    # set soup equal to the webpage html contents
    soup = BeautifulSoup(page.content, 'html.parser')

    # get all text from the webpage
    texts = soup.findAll('p')

    # filter out invisible text in the html
    visible_texts = filter(tag_visible, texts)

    here = []
    for line in visible_texts:
        text = []
        for x in line:
            if isinstance(x, bs4.element.NavigableString):
                text.append(x.strip())

        if " ".join(text) not in here and " ".join(text) not in this:
            keywordHere = False
            for keyword in keywords:
                if keyword in " ".join(text):
                    keywordHere = True

            if keywordHere:
                here.append(" ".join(text))
                this.append(" ".join(text))
                currentSeed.write(" ".join(text))
                currentSeed.write("\n")

    # close the file associated with this seed. we are done adding text to it
    currentSeed.close()

    seedSet = open(seedFileName, "a", encoding="utf-8")

    # update the stored length of the current seed set(urls)
    seedSetLength = len(urls)

    # increment the current seed in the set by 1
    currentSeedNumber += 1

    # if you are at the last seed needed, stop the loop
    if currentSeedNumber == seedSetLength:
        seedSet.close()
        notAtLastSeed = False
    else:
        seedSet.write(urls[currentSeedNumber])
        if currentSeedNumber != seedSetLength - 1:
            seedSet.write("\n")

for url in urls:
    print(url)
