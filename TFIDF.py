import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import math
import string



# This is the second recommended way of doing term frequency
# in tfidf. https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency%E2%80%93Inverse_document_frequency
# This is document term weight in the wiki article
# This is a fomula which calculates log(1+[number of times a word appears])
def computeTFRec2(numOfWords___, bagOfWords___):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords___)
    for word, count in numOfWords___.items():
        tfDict[word] = math.log(count+1)
    return tfDict



# This is the second recommended way of doing IDF
# in tfidf. https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency%E2%80%93Inverse_document_frequency
# This is query term weight in the wiki article
# This is a fomula which calculates log(1+ ( [length of the document] / [the value of the word from term frequency] ))
def computeIDFRec2(documents):
    N = len(documents)

    idDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idDict[word] += 1

    for word, val in idDict.items():
        idDict[word] = math.log((N / (float(val))) +1)
        #print('idDict[word]: ' + str(idDict[word]))
    return idDict


# The TF IDF is calculated by multiplying the idfs of a word by the value of the word
def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
        #print(word +": " + str(tfidf[word]))
    return tfidf

# Does the steps to doing TFIDF. This compiles the cleaning,
# the number of words in a document, the TF, the IDF, the TFIDF
# of both the tweets and webpage and returns those values
def getTweetAndWebpageTFIDF(tweet, webpage):
    #Cleans the data
    #print(tweet[0])
    bagOfWordsTweets = cleaningData(tweet[0])
    bagOfWordsWebpage = cleaningData(webpage)

    #Makes a dic of the unique words
    uniqueWords = set(bagOfWordsTweets).union(set(bagOfWordsWebpage))

    #Counts the number of each word in the tweets and documents
    numOfWordsTweets = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsTweets:
        numOfWordsTweets[word] += 1
    numOfWordsWebpage = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsWebpage:
        numOfWordsWebpage[word] += 1

    #print(numOfWordsTweets)
    #print(numOfWordsWebpage)

    #Computes the term frequency in tweets and webpages
    tFtweets = computeTFRec2(numOfWordsTweets, bagOfWordsTweets)
    tFwebpage = computeTFRec2(numOfWordsWebpage, bagOfWordsWebpage)
    #print(tFtweets)
    #print(tFwebpage)

    #computes idfs
    idfs = computeIDFRec2([numOfWordsTweets, numOfWordsWebpage])

    #computes tfidf
    tfidfTweets= computeTFIDF(tFtweets,idfs)
    tfidfWebpage= computeTFIDF(tFwebpage, idfs)

    #print(tfidfTweets)
    #print(tfidfWebpage)

    return [tfidfTweets, tfidfWebpage]

# Does the final part and create a list of 100 words with the best scores
# in the method requested by the teachers.
# **********VALUES NEED TO BE APPENDED TO CSV FILE STILL**********
def multTFIDscoresOfTweetsAndWebpage(tweets, webpages):
    newCol=[]
    for tweet in tweets:
        w_tAndSw_doc = {}
        w_doc = {}
        max_similar_doc = {}
        for webpage in webpages:
            results = getTweetAndWebpageTFIDF(tweet, webpage)
            #print('result 0:' + str(results[0]))
            #print('result 1:' + str(results[1]))
            uniqueWords = set(results[0]).union(set(results[1]))
            for word in uniqueWords:
                #print(w_tAndSw_doc.get(word))
                if w_tAndSw_doc.get(word) is not None:
                    #print('got in here')
                    w_tAndSw_doc[word] += results[0][word] * results[1][word]
                    #print(word +": " + 'w_tAndSw_doc[word]')
                else:
                    w_tAndSw_doc[word] = results[0][word] * results[1][word]

                if w_doc.get(word) is not None:
                    w_doc[word] += results[1][word]
                else:
                    w_doc[word] = results[1][word]

        listOfWords = set(w_tAndSw_doc).union(set(w_doc))
        for word in listOfWords:
            if w_doc[word] != 0:
                # print(w_tAndSw_doc[word])
                # print(w_doc[word])
                max_similar_doc[word] = w_tAndSw_doc[word] / w_doc[word]
            else:
                max_similar_doc[word] = 0.0

        #print("Unedited : " + str(max_similar_doc))
        max_similar_doc = sorted(max_similar_doc, key=max_similar_doc.get, reverse=True)
        #print("Max to min: " + str(max_similar_doc))
        #print("First 100 : " + str(list(max_similar_doc)[:100]))
        newCol.append(list(max_similar_doc)[:100])

    print(newCol)


#Cleans a scentence
def cleaningData(scentence):
    tokens = word_tokenize(scentence)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    #print(words[:100])
    return words

csvName=input("Name of the csv file you are reading from (do not include .csv): ")
df = pd.read_csv(csvName + '.csv', usecols=[2])
#print(df.values)
tweet = df.values


numOfDocuments = input('How many documents are you reading (This will read 0 - [the number you choose-1].txt for our documents):')
documents = []
for i in range(int(numOfDocuments)):
    documents.append(open(str(i) +'.txt', encoding="utf-8").read())

webpage = documents
#print(webpage)
multTFIDscoresOfTweetsAndWebpage(tweet, webpage)


'''
def multTFIDscoresOfTweetsAndWebpage(tweets, webpages):
    w_tAndSw_doc = {}
    w_doc = {}
    max_similar_doc = {}
    for tweet in tweets:
        for webpage in webpages:
            results = getTweetAndWebpageTFIDF(tweet, webpage)
            #print('result 0:' + str(results[0]))
            #print('result 1:' + str(results[1]))
            uniqueWords = set(results[0]).union(set(results[1]))
            for word in uniqueWords:
                #print(w_tAndSw_doc.get(word))
                if w_tAndSw_doc.get(word) is not None:
                    #print('got in here')
                    w_tAndSw_doc[word] += results[0][word] * results[1][word]
                    #print(word +": " + 'w_tAndSw_doc[word]')
                else:
                    w_tAndSw_doc[word] = results[0][word] * results[1][word]

                if w_doc.get(word) is not None:
                    w_doc[word] += results[1][word]
                else:
                    w_doc[word] = results[1][word]

    #print(w_tAndSw_doc)
    #print(w_doc)
    listOfWords = set(w_tAndSw_doc).union(set(w_doc))
    for word in listOfWords:
        if w_doc[word] != 0:
            #print(w_tAndSw_doc[word])
            #print(w_doc[word])
            max_similar_doc[word] = w_tAndSw_doc[word] / w_doc[word]
        else:
            max_similar_doc[word]=0.0

    print("Unedited : "+ str(max_similar_doc))
    max_similar_doc = sorted(max_similar_doc, key=max_similar_doc.get, reverse=True)
    print("Max to min: "+ str(max_similar_doc))
    print("First 100 : " + str(list(max_similar_doc)[:100]))
    return list(max_similar_doc)[:100]

    
    
    
    
    
    
    
    
    
    
    def computeIDF(documents):
    N = len(documents)

    idDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idDict[word] += 1

    for word, val in idDict.items():
        idDict[word] = math.log(N / float(val))
        #print('idDict[word]: ' + str(idDict[word]))
    return idDict


def computeIDFSmooth(documents):
    N = len(documents)

    idDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idDict[word] += 1

    for word, val in idDict.items():
        idDict[word] = math.log(N / (float(val)+1))+1
        #print('idDict[word]: ' + str(idDict[word]))
    return idDict
def computeTFTermFrequency(numOfWords___, bagOfWords___):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords___)
    for word, count in numOfWords___.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

    
'''