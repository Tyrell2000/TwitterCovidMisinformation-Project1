import pandas as pd
from nltk import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import math
import string
import re


'''
ft,d is the raw count of a term in a document, i.e., the number of times that term t occurs in document d

N: total number of documents in the corpus 

nt: number of documents where the term appears 
'''





def computeTFRec1(numOfWords___, documents):
    tfDict = {}
    for word, count in numOfWords___.items():
        tfDict[word] = count

    N = len(documents)

    idDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idDict[word] += 1

    for word, val in idDict.items():
        idDict[word] = tfDict[word] * math.log(N / float(val))

    return idDict

def computeIDFRec1(numOfWords___, documents):
    tfDict = {}
    for word, count in numOfWords___.items():
        tfDict[word] = count

    N = len(documents)

    idDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idDict[word] += 1

    for word, val in idDict.items():
        idDict[word] = (0.5+(0.5 *(tfDict[word]/max(tfDict.values())) )  ) * math.log(N / float(val))

    return idDict



# This is the second recommended way of doing term frequency
# in tfidf. https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency%E2%80%93Inverse_document_frequency
# This is document term weight in the wiki article
# This is a fomula which calculates log(1+[number of times a word appears])
def computeTFRec2(numOfWords___, documents):
    tfDict = {}
    for word, count in numOfWords___.items():
        tfDict[word] = math.log(count+1)
    return tfDict


# This is the second recommended way of doing IDF
# in tfidf. https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency%E2%80%93Inverse_document_frequency
# This is query term weight in the wiki article
# This is a fomula which calculates log(1+ ( [length of the document] / [number of times the word appears in the document] ))
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






def computeTFRec3(numOfWords___, documents):
    tfDict = {}
    for word, count in numOfWords___.items():
        tfDict[word] = count

    N = len(documents)

    idDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idDict[word] += 1

    for word, val in idDict.items():
        idDict[word] = (1 + math.log(tfDict[word])) * math.log(N / float(val))

    return idDict

def computeIDFRec3(numOfWords___, documents):
    tfDict = {}
    for word, count in numOfWords___.items():
        tfDict[word] = count

    N = len(documents)

    idDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idDict[word] += 1

    for word, val in idDict.items():
        idDict[word] = (1 + math.log(tfDict[word]) ) * math.log(N / float(val))

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

    tFtweets1 = computeTFRec1(numOfWordsTweets, [numOfWordsTweets, numOfWordsWebpage])
    tFwebpage1 = computeTFRec1(numOfWordsWebpage, [numOfWordsTweets, numOfWordsWebpage])

    tFtweets2 = computeTFRec2(numOfWordsTweets, [numOfWordsTweets, numOfWordsWebpage])
    tFwebpage2 = computeTFRec2(numOfWordsWebpage, [numOfWordsTweets, numOfWordsWebpage])

#    tFtweets3 = computeTFRec3(numOfWordsTweets, [numOfWordsTweets, numOfWordsWebpage])
#    tFwebpage3 = computeTFRec3(numOfWordsWebpage, [numOfWordsTweets, numOfWordsWebpage])


    #computes idfs
    idfs1 = computeIDFRec1(numOfWordsTweets, [numOfWordsTweets, numOfWordsWebpage])
    idfs2 = computeIDFRec2([numOfWordsTweets, numOfWordsWebpage])
#    idfs3 = computeIDFRec3([numOfWordsTweets, numOfWordsWebpage])

    #computes tfidf
    tfidfTweets1= computeTFIDF(tFtweets1,idfs1)
    tfidfWebpage1= computeTFIDF(tFwebpage1, idfs1)

    tfidfTweets2= computeTFIDF(tFtweets2,idfs2)
    tfidfWebpage2= computeTFIDF(tFwebpage2, idfs2)

#    tfidfTweets3= computeTFIDF(tFtweets3,idfs3)
#    tfidfWebpage3= computeTFIDF(tFwebpage3, idfs3)

    #print(tfidfTweets)
    #print(tfidfWebpage)

    return [tfidfTweets2, tfidfWebpage2]

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
            #uniqueWords = set(results[0]).union(set(results[1]))
            uniqueWords = set(results[0])
            #print(results[0])
            for word in uniqueWords:
                if w_tAndSw_doc.get(word) is not None:
                    w_tAndSw_doc[word] += results[0][word] * results[1][word]
                else:
                    w_tAndSw_doc[word] = results[0][word] * results[1][word]

                if w_doc.get(word) is not None:
                    w_doc[word] += results[1][word]
                else:
                    w_doc[word] = results[1][word]

        listOfWords = set(w_tAndSw_doc).union(set(w_doc))
        for word in listOfWords:
            if w_doc[word] != 0:
                max_similar_doc[word] = w_tAndSw_doc[word] / w_doc[word]
            else:
                max_similar_doc[word] = 0.0


        max_similar_doc_sorted = sorted(max_similar_doc, key=max_similar_doc.get, reverse=True)

        min_val= max_similar_doc[list(max_similar_doc_sorted)[-1]]

        your_dict = {k: v for k, v in max_similar_doc.items() if v != min_val}

        #        print(max_similar_doc.get(list(max_similar_doc)[-1]))

        first100=' '.join(map(str, list(your_dict)[:100]))

        #TwitterDataWithTFIDF3

        #print(first100)
        newCol.append(tweet + " " + first100.replace(" ", ","))
        #print(newCol)

    return newCol


#Cleans a scentence
def cleaningData(scentence):
    #print('starting scentence: ' + scentence)
    scentence = re.sub(r'http\S+', '', scentence)
    tknzr = TweetTokenizer()
    tokens = tknzr.tokenize(scentence)
    # convert to lower case
    tokens = [w.lower() for w in tokens]

    # filter out stop words
    table = str.maketrans('', '', string.punctuation)
    stop_words = set(stopwords.words('english'))
    words = [w for w in tokens if not w in stop_words]

    stop_words_WOpunc = [w.translate(table) for w in stop_words]
    words = [w for w in words if not w in stop_words_WOpunc]

    # remove punctuation from each word
    stripped = [w.translate(table) for w in words]

    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]

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
cols = multTFIDscoresOfTweetsAndWebpage(tweet, webpage)
#print(len(cols))
df = pd.read_csv(csvName + ".csv")
df['context_information'] = cols
print(df)
df.to_csv(csvName + ".csv", index=False)



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



#Cleans a scentence
def cleaningData(scentence):
    print('starting scentence: ' + scentence)
    scentence = re.sub(r'http\S+', '', scentence)
    print('Hyperlink out scentence: ' + scentence)
    tokens = word_tokenize(scentence)
    print('Hyperlink out scentence: ' + scentence)
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
   
   
   
       #Computes the term frequency in tweets and webpages

    tFtweets1 = computeTFRec1(numOfWordsTweets, [numOfWordsTweets, numOfWordsWebpage])
    tFwebpage1 = computeTFRec1(numOfWordsWebpage, [numOfWordsTweets, numOfWordsWebpage])

    tFtweets2 = computeTFRec2(numOfWordsTweets, [numOfWordsTweets, numOfWordsWebpage])
    tFwebpage2 = computeTFRec2(numOfWordsWebpage, [numOfWordsTweets, numOfWordsWebpage])

    tFtweets3 = computeTFRec3(numOfWordsTweets, [numOfWordsTweets, numOfWordsWebpage])
    tFwebpage3 = computeTFRec3(numOfWordsWebpage, [numOfWordsTweets, numOfWordsWebpage])


    #computes idfs
    idfs1 = computeIDFRec1([numOfWordsTweets, numOfWordsWebpage])
    idfs2 = computeIDFRec2([numOfWordsTweets, numOfWordsWebpage])
    idfs3 = computeIDFRec3([numOfWordsTweets, numOfWordsWebpage])

    #computes tfidf
    tfidfTweets= computeTFIDF(tFtweets,idfs)
    tfidfWebpage= computeTFIDF(tFwebpage, idfs)y
    
'''