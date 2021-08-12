import pandas as pd
from nltk import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import math
import string
import re





# This is the second recommended way of doing term frequency
# in tfidf. https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency%E2%80%93Inverse_document_frequency
# This is document term weight in the wiki article
# This is a formula which calculates log(1+[number of times a word appears])
def computeTFRec2(numOfWords___):
    tfDict = {}
    for word, count in numOfWords___.items():
        tfDict[word] = math.log(count+1)
    return tfDict


# This is the second recommended way of doing IDF
# in tfidf. https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency%E2%80%93Inverse_document_frequency
# This is query term weight in the wiki article
# This is a formula which calculates log(1+ ( [length of the document] / [number of times the word appears in the document] ))
def computeIDFRec2(document):
    N = len(document)

    idDict = dict.fromkeys(document.keys(), 0)

    for word, val in document.items():
        if val > 0:
            idDict[word] += 1

    for word, val in idDict.items():
        if val == 0:
            idDict[word] = 0
        else:
            idDict[word] = math.log((N / (float(val))) +1)
        #print('idDict[word]: ' + str(idDict[word]))
    return idDict




# The TF IDF is calculated by multiplying the idfs of a word by the value of the word
def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf


# Does the steps to doing TFIDF. This compiles the cleaning,
# the number of words in a document, the TF, the IDF, the TFIDF
# of both the tweets and webpage and returns those values
def getTweetAndWebpageTFIDF(tweet, webpage):
    #Cleans the data
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

    #Computes the term frequency in tweets and webpages

    tFtweets2 = computeTFRec2(numOfWordsTweets)
    tFwebpage2 = computeTFRec2(numOfWordsWebpage)


    #computes idfs

    TweetIDF = computeIDFRec2(numOfWordsTweets)
    WebpageIDF = computeIDFRec2(numOfWordsWebpage)

    #computes tfidf

    tfidfTweets2= computeTFIDF(tFtweets2,TweetIDF)
    tfidfWebpage2= computeTFIDF(tFwebpage2, WebpageIDF)

    return [tfidfTweets2, tfidfWebpage2]

# Does the final part and create a list of 100 words with the best scores
# in the method requested by the teachers.
def multTFIDscoresOfTweetsAndWebpage(tweets, webpages):
    # newCol is all the 10 words generated from each tweet, which will be put into a new column on the dataset
    newCol=[]

    for tweet in tweets:

        #These are just placeholders for multiplying all the values together
        w_tAndSw_doc = {}
        w_doc = {}

        #This will contain the final word values
        max_similar_doc = {}

        for webpage in webpages:

            results = getTweetAndWebpageTFIDF(tweet, webpage)
            uniqueWords = set(results[0])

            '''
            Was reccomended to do the following formula with the calculated TFIDFs:
            
            multiply the tf-idf score of the words between tweet-words and document-words
                        (formula: SUM (w_T * w_doc) / SUM (w_doc)) 
                        (here: I am trying to say,
                                w_T means the tf-idf score of a word in the tweet T and 
                                w_doc means the tf-idf score of a word in the document)
                                
            The next few for loops are simulating this code
            '''

            for word in uniqueWords:
                #Adds all the multiplied scores from tf-idf tweet words and multiplies it by tf-idf document words
                if w_tAndSw_doc.get(word) is not None:
                    w_tAndSw_doc[word] += results[0][word] * results[1][word]
                else:
                    w_tAndSw_doc[word] = results[0][word] * results[1][word]

                #Adds the values from all the document word tfidf scores
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


        #Sorts all words from greatest to least
        max_similar_doc_sorted = sorted(max_similar_doc, key=max_similar_doc.get, reverse=True)

        #Gets lowest value
        min_val= max_similar_doc[list(max_similar_doc_sorted)[-1]]

        #Removes all words that have the lowest value (this gets rid of any 'null' values, such as words from the document but not the tweet, and any words that did not appear in the document)
        your_dict = {k: v for k, v in max_similar_doc.items() if v != min_val}

        #        print(max_similar_doc.get(list(max_similar_doc)[-1]))

        #Grabs top 10 words gathered from the scores of the words that are non 'null' values
        first10=' '.join(map(str, list(your_dict)[:10]))

        newCol.append(first10.replace(" ", ","))

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

    #print(words[:10])
    return words



csvName=input("Name of the csv file you are reading from (do not include .csv): ")
df = pd.read_csv(csvName + '.csv', usecols=[2])
tweet = df.values
print(cleaningData(tweet[0][0]))
numOfDocuments = input('How many documents are you reading (This will read 1 - [the number you choose].txt for our documents):')
documents = []

#Grabs the seeds generated from one of our other codes
for i in range(int(numOfDocuments)):
    documents.append(open("pages/" + str(i+1) +'.txt', encoding="utf-8").read())
webpage = documents

cols = multTFIDscoresOfTweetsAndWebpage(tweet, webpage)

df = pd.read_csv(csvName + ".csv")
df['context_information'] = cols

#cannot append cols without brakets cause that is how the info is stored
print(df)
df.to_csv(csvName + ".csv", index=False)