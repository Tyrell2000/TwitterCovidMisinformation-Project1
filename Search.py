import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
from urllib.parse import urlparse
import datetime


# Here is a link to learn BeautifulSoup: https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/
# Basically this is transforming a url into html and then we do things to extract certain parts of html

# Will return a list of the names of the 5 seeds Url is a url, listOfLinks is the links you will be comparing to a
# generated link to make sure there are no duplicate links in the generated list
def get5Seeds(url, listOfLinks):
    # To my knowledge, this is what gets the url page
    page = requests.get(url.strip())
    # To my knowledge, this is what process the url page into html
    soup = BeautifulSoup(page.content, 'html.parser')

    # Root of links (like cnn.com, thehill.com, ect). Only accepts a link if it is form the root link.
    # If root link is cnn.com, twitter.com/cnn will not be accepted, but cnn.com/twitter will
    baseLink = urlparse(url).netloc

    # Make sure we are getting at most 5 seeds
    counter = 0
    fiveOrLessSeedsGenerated = []

    # Took me a minute to figure out, im pretty sure this is fining all instances of <a> in the html
    for link in soup.find_all('a'):
        # Checks if the href is actually a word
        if link.get('href') is not None:

            # Checks if the href is actually there (at least one letter)
            if len(link.get('href')) > 0:

                if "pdf" not in link.get('href') and "zIp" not in link.get('href') and "zip" not in link.get('href') \
                        and "win" not in link.get('href') and "mp3" not in link.get('href') and "mp4" not in \
                        link.get('href') and "jpg" not in link.get('href') and "JPEG" not in link.get('href') and \
                        "jpeg" not in link.get('href') and "docx" not in link.get('href') and "pptx" not in \
                        link.get('href') and "png" not in link.get('href'):

                    # Checks to see if one of the terms in the file of terms we made is in the \blahblahblah
                    if coronaTermChecker(link.get('href'), 'coronavirusWords'):
                        getLink = link.get('href')

                        # Just some formatting because most hrefs come out as /something instead of stuff.com/something
                        if getLink[0] == '/':
                            getLink = 'http://' + baseLink + getLink
                            # This is how we make sure that duplicates are not made
                            if getLink not in listOfLinks and getLink not in fiveOrLessSeedsGenerated and "#bottom-story-socials" not in getLink:
                                ##print(getLink in listOfLinks)
                                # print(list(open(txtName + '.txt', 'r')))
                                ##print(listOfLinks[0])
                                ##print(getLink)
                                fiveOrLessSeedsGenerated.append(getLink)
                                # Adds 1 to counter to make sure that we are getting 5 or less seeds from a seed (as
                                # requested from teachers)
                                counter += 1
                            if counter == 5:
                                break
    ##print(fiveOrLessSeedsGenerated)
    return fiveOrLessSeedsGenerated


# This is for the auto generator of 1000 seeds
# Url is a url, txtName is the text file name
def add5SeedsToList(url, txtName):
    # To my knowlege, this is what gets the url page
    page = requests.get(url.strip(), allow_redirects=False)
    # To my knowlege, this is what process the url page into html
    soup = BeautifulSoup(page.content, 'html.parser')

    # Root of links (like twitter.com, thehill.com, ect)
    baseLink = urlparse(url).netloc

    # Make sure we are getting at most 5 seeds
    counter = 0

    # Took me a minute to figure out, im pretty sure this is fining all instances of <a> in the html
    for link in soup.find_all('a'):
        # Checks if the href is actually a word
        if link.get('href') is not None:

            # Checks if the href is actually there (at least one letter)
            if len(link.get('href')) > 0:

                # Checks to see if one of the terms in the file of terms we made is in the \blahblahblah
                if coronaTermChecker(link.get('href'), 'coronavirusWords'):

                    txt = open(txtName + '.txt', 'a', encoding="utf-8")
                    getLink = link.get('href')

                    # Just some formatting because most hrefs come out as /something instead of stuff.com/something
                    if getLink[0] == '/':
                        getLink = 'http://' + baseLink + getLink
                        # This is how we make sure that duplicates are not made
                        if getLink + '\n' not in list(open(txtName + '.txt', 'r', encoding="utf-8")):
                            # print(list(open(txtName + '.txt', 'r')))
                            print(getLink)
                            txt.write('http://' + urlparse(url).netloc + link.get('href'))

                            # Adds 1 to counter to make sure that we are getting 5 or less seeds from a seed (as
                            # requested from teachers)
                            counter = counter + 1
                            txt.write('\n')
                            txt.close()
                        if counter == 5:
                            break


# Reads the links in the link file continously, until 1000 links are made
def thousandSeedGenerator():
    # This is just for the file format. We should be doing seedsset_date (date being todays date)
    date = datetime.date.today().strftime('%Y-%m-%d')
    txtName = 'seedsset' + '_' + str(date)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}

    # url = "https://thehill.com/policy/healthcare/public-global-health/561627-pfizer-vaccine-less-effective-against
    # -delta-variant"
    url = input("Please type in your starting seed (needs https:// at the start of the link): ")

    txt = open(txtName + '.txt', "w", encoding="utf-8")
    txt.write(url)
    txt.close()
    counter = 0

    # For every line in file. This is how we continously get the links from the file.
    for URL in open(txtName + '.txt', 'r'):
        # print('url: '+ URL)
        # If every line in file is less than 1000. This is how we get exactly 1000 or less urls.
        if len(list(open(txtName + '.txt', 'r', encoding="utf-8"))) >= 1000:
            break
        add5SeedsToList(URL, txtName)


# Will check to see if any words relating to covid and the vaccines appear in the links Link is the link that is
# being checked, fileName1 is the file with all the words that relate to the coronavirus and the vaccines in it
def coronaTermChecker(link, fileName1):
    # This removes the \n in the lists (as they stay in when turning the file into a list of words for whatever reason)
    fileName1Words = [j.rstrip() for j in list(open(fileName1 + '.txt', 'r', encoding="utf-8"))]
    for word in fileName1Words:
        try:
            if word.lower() in link.lower():
                return True
        except:
            if word in link:
                return True
    return False


# #get5Seeds('https://thehill.com/policy/healthcare/public-global-health/561627-pfizer-vaccine-less-effective-against
# -delta-variant', list(open('seedsset_2021-07-08' + '.txt', 'r')))


'''
def coronaTermChecker(fileName1, fileName2):
        fileName1Words = [j.rstrip() for j in list(open(fileName1 + '.txt', 'r'))]
        fileName2Words = [k.rstrip() for k in list(open(fileName2 + '.txt', 'r'))]

        for word in fileName1Words:
                for link in fileName2Words:
                        if word.lower() in link.lower():
                                return True
        return False
        
        
        
        
def get5Seeds(url, txtName):
        # To my knowlege, this is what gets the url page
        page = requests.get(url.strip())
        # To my knowlege, this is what process the url page into html
        soup = BeautifulSoup(page.content, 'html.parser')

        # Root of links (like twitter.com, thehill.com, ect)
        baseLink = urlparse(url).netloc

        #Make sure we are getting at most 5 seeds
        counter = 0

        #Took me a minute to figure out, im pretty sure this is fining all instances of <a> in the html
        for link in soup.find_all('a'):
                # Checks if the href is actually there (at least one letter)
                if len(link.get('href')) > 0:

                        if coronaTermChecker(link.get('href'), 'coronavirusWords') == True:

                                txt = open(txtName + '.txt', 'a', encoding="utf-8")
                                getLink = link.get('href')


                                # Just some formatting because most hrefs come out as /something instead of stuff.com/something
                                if getLink[0] == '/':
                                        getLink = 'http://' + baseLink + getLink

                                #This is how we make sure that duplicates are not made
                                if getLink + '\n' not in list(open(txtName + '.txt', 'r')):
                                        # print(list(open(txtName + '.txt', 'r')))

                                        #If what we are getting is actually a link (there are instances of # and stuff for whatever reason)
                                        if link.get('href')[0] == '/' or 'http://' in link.get('href'):
                                                print(getLink)

                                                # Formats the /stuff into link and writes it to file
                                                if link.get('href')[0] == '/':
                                                        # print('if / is in link:' + urlparse(url).netloc + link.get('href'))
                                                        txt.write('http://' + urlparse(url).netloc + link.get('href'))

                                                #Write link to file
                                                elif 'http://' in link.get('href'):
                                                        # print('if / is not in link:' + urlparse(url).netloc + link.get('href'))
                                                        txt.write(link.get('href'))

                                                #Adds 1 to counter to make sure that we are getting 5 or less seeds from a seed (as requested from teachers)
                                                counter = counter + 1
                                                txt.write('\n')
                                                txt.close()
                                if counter == 5:
                                        break



'''
