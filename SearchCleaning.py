import bs4
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import datetime
import Search
import random


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


allLanguages = False

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/50.0.2661.102 Safari/537.36'}

urls = []

startingSeeds = open("StartingSeedLinks.txt", "r", encoding="utf-8")
for line in startingSeeds.readlines():
    urls.append(line[:-1])

random.shuffle(urls)

# Pick the language you want to gather text in. Will only gather text already in that language. If you set all to False,
# all five languages will be gathered.
english = False
turkish = False
chinese = False
russian = False
spanish = False

language = []
languageName = ""

if turkish:
    languageName = "Turkish"
    words = open("turkishStopwords.txt", "r", encoding="utf-8")
    for word in words.readlines():
        language.append(word[:-1])
elif english:
    languageName = "English"
    words = open("englishStopwords.txt", "r", encoding="utf-8")
    for word in words.readlines():
        language.append(word[:-1])
elif chinese:
    languageName = "Chinese"
    words = open("chineseStopwords.txt", "r", encoding="utf-8")
    for word in words.readlines():
        language.append(word[:-1])
elif russian:
    languageName = "Russian"
    words = open("russianStopwords.txt", "r", encoding="utf-8")
    for word in words.readlines():
        language.append(word[:-1])
elif spanish:
    languageName = "Spanish"
    words = open("spanishStopwords.txt", "r", encoding="utf-8")
    for word in words.readlines():
        language.append(word[:-1])
else:
    allLanguages = True

    languageName = "English, Chinese, Russian, Spanish, Turkish"
    words = open("englishStopwords.txt", "r", encoding="utf-8")
    englishLanguage = []
    for word in words.readlines():
        englishLanguage.append(word[:-1])
    words.close()

    words = open("turkishStopwords.txt", "r", encoding="utf-8")
    turkishLanguage = []
    for word in words.readlines():
        turkishLanguage.append(word[:-1])
    words.close()

    words = open("spanishStopwords.txt", "r", encoding="utf-8")
    spanishLanguage = []
    for word in words.readlines():
        spanishLanguage.append(word[:-1])
    words.close()

    words = open("russianStopwords.txt", "r", encoding="utf-8")
    russianLanguage = []
    for word in words.readlines():
        russianLanguage.append(word[:-1])
    words.close()

    words = open("chineseStopwords.txt", "r", encoding="utf-8")
    chineseLanguage = []
    for word in words.readlines():
        chineseLanguage.append(word[:-1])
    words.close()

print("Language(s):", languageName)

# Change this to True if the user want to enter their own keywords
haveOwnKeywords = False

if not haveOwnKeywords:
    # The list of keywords to use for deciding which website text to save to files
    keywords = []

    searchWords = open("coronavirusWords.txt", "r", encoding="utf-8")
    for line in searchWords.readlines():
        keywords.append(line[:-1])
else:
    keywords = []

    ## Allows the user to enter their own keywords to look for in webpages to save
    answer = input("Enter custom keyword to search for (Enter DONE when finished): ")

    while str(answer) != "DONE":
        keywords.append(str(answer))
        answer = input("Enter custom keyword to search for (Enter DONE when finished): ")

print("Starting Seeds:", urls)
print("Keywords:", keywords)
lastSeed = 0
while lastSeed == 0:
    # how many seeds you want
    seedAnswer = input("How many seeds would you like to gather(Multiple of 5)? ")
    if (int(seedAnswer) % 5) == 0:
        lastSeed = int(seedAnswer)
    else:
        print("Not a multiple of five.")
##lastSeed = int("10")
print("Seeds to Gather:", lastSeed)

# today's date
date = datetime.date.today().strftime('%Y-%m-%d')

# the name of the seed set file
seedFileName = "seedsset_" + str(date) + ".txt"

# clear the file, just in case there is anything inside of it
seedSet = open("pages/" + seedFileName, "w", encoding="utf-8")
seedSet.truncate(0)
seedSet.close()

seedSetUrls = []
textSaved = []
this = []
seedsSkipped = 0
documentLanguageWordsFound = {}
languageDocumentsSaved = {"English": 0, "Spanish": 0, "Turkish": 0, "Russian": 0, "Chinese": 0}


# Filter and write text of webpage from given url
def writeWebpageTextMultipleLanguages(url, languageCheckList):
    languageGathered = ""
    global seedsSkipped
    writeThisSeed = False
    isCorrectLanguage = False
    languageWordsFound = []

    urlCheck = open("urlCheck.txt", "a", encoding="utf-8")
    urlCheck.write(url)
    urlCheck.write("\n")
    urlCheck.close()

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

            for languageList in languageCheckList:
                for checkWord in languageList:
                    for line in text:
                        if checkWord in line.split(" "):
                            if checkWord not in languageWordsFound:
                                languageWordsFound.append(checkWord)
                                if len(languageWordsFound) == 5:
                                    if checkWord in englishLanguage:
                                        if languageDocumentsSaved["English"] < (lastSeed / 5):
                                            languageGathered = "English"
                                            isCorrectLanguage = True
                                    elif checkWord in spanishLanguage:
                                        if languageDocumentsSaved["Spanish"] < (lastSeed / 5):
                                            languageGathered = "Spanish"
                                            isCorrectLanguage = True
                                    elif checkWord in turkishLanguage:
                                        if languageDocumentsSaved["Turkish"] < (lastSeed / 5):
                                            languageGathered = "Turkish"
                                            isCorrectLanguage = True
                                    elif checkWord in chineseLanguage:
                                        if languageDocumentsSaved["Chinese"] < (lastSeed / 5):
                                            languageGathered = "Chinese"
                                            isCorrectLanguage = True
                                    elif checkWord in russianLanguage:
                                        if languageDocumentsSaved["Russian"] < (lastSeed / 5):
                                            languageGathered = "Russian"
                                            isCorrectLanguage = True

    if writeThisSeed and isCorrectLanguage:
        textSaved.append(here)
        seedSetUrls.append(url)
        languageDocumentsSaved[languageGathered] = languageDocumentsSaved[languageGathered] + 1
        print("Seed Gathered(" + languageGathered + " " + str(languageDocumentsSaved[languageGathered]) + "/" + str(int(
            lastSeed / 5)) + "):", str(len(seedSetUrls)) + "/" + str(lastSeed))

        try:
            # create/open file for this seed, named after position in the list of seeds(urls) starting from 0
            currentSeed = open("pages/" + str(len(seedSetUrls)) + ".txt", "w", encoding="utf-8")
            for lineOfText in textSaved[len(seedSetUrls) - 1]:
                if text != textSaved[-1:][0]:
                    currentSeed.write(lineOfText)
                    currentSeed.write("\n")
                else:
                    currentSeed.write(lineOfText)

            # close the file associated with this seed. we are done adding text to it
            currentSeed.close()

            if len(seedSetUrls) == 1:
                seedSet = open("pages/" + seedFileName, "w", encoding="utf-8")
                seedSet.write(url)
                seedSet.write("\n")
                seedSet.close()
            else:
                if len(seedSetUrls) != lastSeed:
                    seedSet = open("pages/" + seedFileName, "a", encoding="utf-8")
                    seedSet.write(url)
                    seedSet.write("\n")
                    seedSet.close()
                else:
                    seedSet = open("pages/" + seedFileName, "a", encoding="utf-8")
                    seedSet.write(url)
                    seedSet.close()
        except:
            print("A seed had a problem.")

        if str(len(seedSetUrls)) not in documentLanguageWordsFound:
            documentLanguageWordsFound[str(len(seedSetUrls))] = languageWordsFound

        # Uncomment the code below to get a txt file containing the language words used to identify a document of txt
        # to save as being the correct language.
        '''documentWords = open("pages/documentWords.txt", "w", encoding="utf-8")
        for docNum in documentLanguageWordsFound:
            toWrite = "Document " + docNum + ": " + str(", ".join(documentLanguageWordsFound[docNum]))
            documentWords.write(toWrite)
            documentWords.write("\n")
        documentWords.close()'''

    else:
        seedsSkipped += 1
        if isCorrectLanguage and not writeThisSeed:
            print("Seeds Skipped:", seedsSkipped, "        Reason: No Keyword in Text")
        elif not isCorrectLanguage and writeThisSeed:
            print("Seeds Skipped:", seedsSkipped, "        Reason: Text is Wrong Language")
            ##print(here)
        elif len(here) == 0:
            print("Seeds Skipped:", seedsSkipped, "        Reason: No Text Gathered")
        else:
            print("Seeds Skipped:", seedsSkipped, "        Reason: Wrong Language and No Keyword")
            ##print(here)


# Filter and write text of webpage from given url
def writeWebpageTextOneLanguage(url):
    global seedsSkipped
    writeThisSeed = False
    isCorrectLanguage = False
    languageWordsFound = []

    urlCheck = open("urlCheck.txt", "a", encoding="utf-8")
    urlCheck.write(url)
    urlCheck.write("\n")
    urlCheck.close()

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

                for checkWord in language:
                    for line in text:
                        if checkWord in line.split(" "):
                            if checkWord not in languageWordsFound:
                                languageWordsFound.append(checkWord)
                                if len(languageWordsFound) >= 5:
                                    isCorrectLanguage = True

    if writeThisSeed and isCorrectLanguage:
        textSaved.append(here)
        seedSetUrls.append(url)
        print("Seeds Gathered:", str(len(seedSetUrls)) + "/" + str(lastSeed))

        try:
            # create/open file for this seed, named after position in the list of seeds(urls) starting from 0
            currentSeed = open("pages/" + str(len(seedSetUrls)) + ".txt", "w", encoding="utf-8")
            for lineOfText in textSaved[len(seedSetUrls) - 1]:
                if text != textSaved[-1:][0]:
                    currentSeed.write(lineOfText)
                    currentSeed.write("\n")
                else:
                    currentSeed.write(lineOfText)

            # close the file associated with this seed. we are done adding text to it
            currentSeed.close()

            if len(seedSetUrls) == 1:
                seedSet = open("pages/" + seedFileName, "w", encoding="utf-8")
                seedSet.write(url)
                seedSet.write("\n")
                seedSet.close()
            else:
                if len(seedSetUrls) != lastSeed:
                    seedSet = open("pages/" + seedFileName, "a", encoding="utf-8")
                    seedSet.write(url)
                    seedSet.write("\n")
                    seedSet.close()
                else:
                    seedSet = open("pages/" + seedFileName, "a", encoding="utf-8")
                    seedSet.write(url)
                    seedSet.close()
        except:
            print("A seed had a problem.")

        if str(len(seedSetUrls)) not in documentLanguageWordsFound:
            documentLanguageWordsFound[str(len(seedSetUrls))] = languageWordsFound

        # Uncomment the code below to get a txt file containing the language words used to identify a document of txt
        # to save as being the correct language.
        '''documentWords = open("pages/documentWords.txt", "w", encoding="utf-8")
        for docNum in documentLanguageWordsFound:
            toWrite = "Document " + docNum + ": " + str(", ".join(documentLanguageWordsFound[docNum]))
            documentWords.write(toWrite)
            documentWords.write("\n")
        documentWords.close()'''

    else:
        seedsSkipped += 1
        if isCorrectLanguage and not writeThisSeed:
            print("Seeds Skipped:", seedsSkipped, "        Reason: No Keyword in Text")
        elif not isCorrectLanguage and writeThisSeed:
            print("Seeds Skipped:", seedsSkipped, "        Reason: Text is Wrong Language")
            ##print(here)
        elif len(here) == 0:
            print("Seeds Skipped:", seedsSkipped, "        Reason: No Text Gathered")
        else:
            print("Seeds Skipped:", seedsSkipped, "        Reason: Wrong Language and No Keyword")
            ##print(here)


# gather the seeds and add them to the list: urls, until you have *lastSeed* amount
def writeNewSeedsOneLanguage(currentSeedNumber):
    if len(seedSetUrls) < lastSeed:
        # add seeds you want to put in the seed set to this list and they will be added later for processing
        try:
            nextSeeds = Search.get5Seeds(urls[currentSeedNumber], urls)
        except Exception as e:
            print(e)
            print("This link just threw an error:", str(urls[currentSeedNumber]) + ".", "It will not be used to "
                                                                                        "collect more seeds.")
            nextSeeds = []
        ##print(nextSeeds, "\n")
    else:
        nextSeeds = []

    # for adding the next seed(s) to be added to the set
    for seed in nextSeeds:
        ##print(len(urls))
        ##print("next seed:", seed)
        if len(seedSetUrls) < lastSeed and seed not in urls:
            urls.append(seed)
            writeWebpageTextOneLanguage(seed)
            ##print(len(urls))


# gather the seeds and add them to the list: urls, until you have *lastSeed* amount
def writeNewSeedsMultipleLanguages(currentSeedNumber, languages):
    if len(seedSetUrls) < lastSeed:
        # add seeds you want to put in the seed set to this list and they will be added later for processing
        try:
            nextSeeds = Search.get5Seeds(urls[currentSeedNumber], urls)
        except:
            print("This link just threw an error:", str(urls[currentSeedNumber]) + ".", "It will not be used to "
                                                                                        "collect more seeds.")
            nextSeeds = []
        ##print(nextSeeds, "\n")
    else:
        nextSeeds = []

    # for adding the next seed(s) to be added to the set
    for seed in nextSeeds:
        ##print(len(urls))
        ##print("next seed:", seed)
        if len(seedSetUrls) < lastSeed and seed not in urls:
            urls.append(seed)
            writeWebpageTextMultipleLanguages(seed, languages)
            ##print(len(urls))


initialUrlsLength = len(urls)

try:
    seedSetLength = len(seedSetUrls)
    currentSeedNumber = -1
    notAtLastSeed = True
    if allLanguages:
        allLanguageList = [englishLanguage, russianLanguage, chineseLanguage, turkishLanguage, spanishLanguage]

        # run until you have all the seeds needed
        while notAtLastSeed:
            try:
                # increment the current seed in the set by 1
                currentSeedNumber += 1

                # call the code to add more seeds, won't add more if you have your desired amount already(lastSeed)
                writeNewSeedsMultipleLanguages(currentSeedNumber, allLanguageList)

                # update the stored length of the current seed set(urls)
                seedSetLength = len(seedSetUrls)

                # if you are at the last seed needed, stop the loop
                if lastSeed == seedSetLength:
                    notAtLastSeed = False
            except:
                print("This link threw an error: " + str(urls[currentSeedNumber]) + ". Skipping this iteration of the "
                                                                                    "while-loop!")
                continue

    else:
        # run until you have all the seeds needed
        while notAtLastSeed:

            # call the code to add more seeds, won't add more if you have your desired amount already(lastSeed)
            writeNewSeedsOneLanguage(currentSeedNumber)

            # update the stored length of the current seed set(urls)
            seedSetLength = len(seedSetUrls)

            # increment the current seed in the set by 1
            currentSeedNumber += 1

            # if you are at the last seed needed, stop the loop
            if lastSeed == seedSetLength:
                notAtLastSeed = False

except Exception as e:
    seedSet = open("pages/" + seedFileName, "w", encoding="utf-8")
    for seedUrl in seedSetUrls:
        if seedSetUrls[len(seedSetUrls) - 1] == seedUrl:
            seedSet.write(seedUrl)
        else:
            seedSet.write(seedUrl)
            seedSet.write("\n")
    seedSet.close()
    print("Couldn't finish the loop:", e)

'''seedSet = open("pages/" + seedFileName, "w", encoding="utf-8")
for seedUrl in seedSetUrls:
    if seedSetUrls[len(seedSetUrls) - 1] == seedUrl:
        seedSet.write(seedUrl)
    else:
        seedSet.write(seedUrl)
        seedSet.write("\n")
seedSet.close()'''

foundLanguageWords = open(languageName + ".txt", "w", encoding="utf-8")
for document in documentLanguageWordsFound:
    for word in documentLanguageWordsFound[document]:
        try:
            foundLanguageWords.write(word)
            foundLanguageWords.write("\n")
        except:
            try:
                print("Write Error: ", word)
            except:
                continue
foundLanguageWords.close()

##print(textSaved[0])

'''
try:
    currentSeedNum = 0
    seedSet = open("pages/" + seedFileName, "w", encoding="utf-8")
    for text in textSaved:
        # create/open file for this seed, named after position in the list of seeds(urls) starting from 0
        currentSeed = open("pages/" + str(currentSeedNum) + ".txt", "w", encoding="utf-8")
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

except Exception as e:
    seedSet = open("pages/" + seedFileName, "w", encoding="utf-8")
    for seedUrl in seedSetUrls:
        if seedSetUrls[len(seedSetUrls) - 1] == seedUrl:
            seedSet.write(seedUrl)
        else:
            seedSet.write(seedUrl)
            seedSet.write("\n")
    seedSet.close()
    try:
        currentSeed.close()
    except:
        p = 0

    print("Error! Stopping seed text gathering.")

seedSet.close()
'''
