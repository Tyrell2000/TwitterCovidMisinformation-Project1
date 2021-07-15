import pandas as pd
from nltk.corpus import stopwords
import math



def computeTermFrequency(numOfWords___, bagOfWords___):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords___)
    for word, count in numOfWords___.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict


def computeIDF(documents):
    N = len(documents)

    idDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idDict[word] += 1

    for word, val in idDict.items():
        idDict[word] = math.log(N / float(val))
    return idDict

def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf


def getTweetAndWebpageTFIDF(tweet, webpage):
    bagOfWordsTweets = tweet.split(' ')
    bagOfWordsWebpage = webpage.split(' ')

    uniqueWords = set(bagOfWordsTweets).union(set(bagOfWordsWebpage))

    numOfWordsTweets = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsTweets:
        numOfWordsTweets[word] += 1
    numOfWordsWebpage = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsWebpage:
        numOfWordsWebpage[word] += 1

    #print(numOfWordsTweets)
    #print(numOfWordsWebpage)

    stopwords.words('english')

    tFtweets = computeTermFrequency(numOfWordsTweets, bagOfWordsTweets)
    tFwebpage = computeTermFrequency(numOfWordsWebpage, bagOfWordsWebpage)
    #print(tFtweets)
    #print(tFwebpage)

    idfs = computeIDF([numOfWordsTweets, numOfWordsWebpage])

    tfidfTweets= computeTFIDF(tFtweets,idfs)
    tfidfWebpage= computeTFIDF(tFwebpage, idfs)

    #print(tfidfTweets)
    #print(tfidfWebpage)

    return [tfidfTweets, tfidfWebpage]

def multTFIDscoresOfTweetsAndWebpage(tweets, webpages):
    w_tAndSw_doc = {}
    w_doc = {}
    max_similar_doc = {}
    for tweet in tweets:
        for webpage in webpages:
            results = getTweetAndWebpageTFIDF(tweet, webpage)
            uniqueWords = set(results[0]).union(set(results[1]))
            for word in uniqueWords:
                if w_tAndSw_doc.get(word):
                    w_tAndSw_doc[word] += results[0][word] * results[1][word]
                    print(word +": " + 'w_tAndSw_doc[word]')
                else:
                    w_tAndSw_doc[word] = results[0][word] * results[1][word]
                    #print(results[0][word])
                    #print(results[1][word])
                    #print(results[0][word] * results[1][word])
                    #print(word +": " + str(w_tAndSw_doc[word]))
                if w_doc.get(word):
                    w_doc[word] += results[1][word]
                else:
                    w_doc[word] = results[1][word]

    listOfWords = set(w_tAndSw_doc).union(set(w_doc))
    for word in listOfWords:
        if w_doc[word] != 0:
            print(w_tAndSw_doc[word])
            print(w_doc[word])
            max_similar_doc[word] = w_tAndSw_doc[word] / w_doc[word]
        else:
            max_similar_doc[word]=0.0

    print("Unedited : "+ str(max_similar_doc))
    max_similar_doc = sorted(max_similar_doc, key=max_similar_doc.get, reverse=False)
    print("Max to min: "+ str(max_similar_doc))
    print("First 100 : " + str(list(max_similar_doc)[:100]))
    return list(max_similar_doc)[:100]


tweet = ['I hae a red dog ow', 'I have a blue dog whoa']
webpage = ['I hve a blue blue dog wha', 'I hae red red dog wo', 'I have a blue dog whoa',]
multTFIDscoresOfTweetsAndWebpage(tweet, webpage)