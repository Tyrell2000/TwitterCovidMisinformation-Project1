import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy
import sys
numpy.set_printoptions(threshold=sys.maxsize)
from nltk.corpus import stopwords

#This calculates the TFIDF using sklearn TfidfVectorizer
def computeTFIDF(stuff):
    tfidf = TfidfVectorizer(use_idf=True, lowercase=True, encoding='utf-8', stop_words=set(stopwords.words('turkish')))
    tfidfOfStuff = tfidf.fit_transform(stuff)
    tfidfScoreArray = tfidfOfStuff.toarray()
    return tfidfScoreArray



# This gets the feature words of the TFIDF. This is used to get the
# formatted words from the tfidf.
def TFIDFwords(stuff):
    tfidf = TfidfVectorizer(use_idf=True, lowercase=True, encoding='utf-8', stop_words=set(stopwords.words('turkish')))
    tfidfOfStuff = tfidf.fit_transform(stuff)
    feature_names = tfidf.get_feature_names()
    return feature_names


# Does the final part and create a list of 100 words with the best scores
# in the method requested by the teachers.
def multTFIDscoresOfTweetsAndWebpage(xColumn, yColumn):
    # newCol is all the 10 words generated from each tweet, which will be put into a new column on the dataset
    newCol = []

    # Gets the TFIDF of the tweets and webpages
    tweets = computeTFIDF(xColumn)
    webpages = computeTFIDF(yColumn)

    # Gets the formatted words from the TFIDF of the tweets and webpages
    tweetsWords = TFIDFwords(xColumn)
    webpageWords = TFIDFwords(yColumn)


    # Calculates the sum of the multiplication the tf-idf scores of words in all of the tweet and the tf-idf scores of words in the webpages
    W_tAndSw_docNewScores = computeW_tAndSw_docNewScore(tweets, webpages, tweetsWords, webpageWords, xColumn)
    # Calculates the sum of the tf-idf scores of tweet words in the webpages
    Sw_docNewScore = computeSw_docNewScore(tweets, webpages, webpageWords, xColumn)




    # Divides the W_tAndSw_docNewScores and Sw_docNewScore for every tweet
    for i in range(len(xColumn)):

        #for each array in this arrays, do a numpy divide then append the numpy array to an array
        newTFIDFScores = numpy.divide(
            W_tAndSw_docNewScores[i],
            Sw_docNewScore[i]
        )

        #Gets rid of the nan values caused by a division by 0, and replaces them with 0
        newTFIDFScoresWOnan = numpy.nan_to_num(newTFIDFScores, nan=0.0)

        #Reverses the order from least to greatest to greatest to least
        sortedTFIDFScores = numpy.sort(newTFIDFScoresWOnan)[::-1]

        #Adds the first 10 greatest values of the  W_tAndSw_docNewScores and Sw_docNewScore that has been turned into a string without the [ and ]
        newCol.append(numpy.array2string(sortedTFIDFScores[:10], separator=',').replace('[', '').replace(']', ''))

    print(newCol)

    return newCol


# Calculates the sum of the multiplication the tf-idf scores of words in all of the tweet and the tf-idf scores of words in the webpages
def computeW_tAndSw_docNewScore(tweets, webpages, tweetsWords, webpageWords, xColumn):

    # These are just placeholders for multiplying all the values together
    w_tAndSw_doc = []

    # For every tweet
    for i in range(len(tweets)):

        print('computeW_tAndSw_docNewScore: ' + str(i))
        tweetWordScores = []

        # Grabs only the words that could possible have values
        for word in TFIDFwords([xColumn[i]]):
            w_tAndSw_docValue = 0

            tweetValue=0

            if word in tweetsWords:
                tweetValue = tweets[i][tweetsWords.index(word)]


            for webpage in webpages:

                webpageValue=0

                # Only grabs only the words that exist in the webpages
                if word in webpageWords:
                    webpageValue = webpage[webpageWords.index(word)]

                w_tAndSw_docValue += webpageValue*tweetValue

            tweetWordScores.append(w_tAndSw_docValue)

        w_tAndSw_doc.append(tweetWordScores)

    return w_tAndSw_doc



# Calculates the sum of the tf-idf scores of tweet words in the webpages
def computeSw_docNewScore(tweets, webpages, webpageWords, xColumn):

    w_doc = []

    # For every tweet
    for i in range(len(tweets)):

        print('computeSw_docNewScore: ' + str(i))

        webpageWordScores = []

        # Grabs only the words that could possible have values
        for word in TFIDFwords([xColumn[i]]):
            w_docValue = 0

            for webpage in webpages:

                webpageValue = 0

                # Only grabs only the words that exist in the webpages
                if word in webpageWords:
                    webpageValue = webpage[webpageWords.index(word)]

                w_docValue += webpageValue

            webpageWordScores.append(w_docValue)

        w_doc.append(webpageWordScores)

    return w_doc


csvName=input("Name of the csv file you are reading from (do not include .csv): ")
df = pd.read_csv(csvName + '.csv')
tweet = df['tweet_text']

numOfDocuments = input('How many documents are you reading (This will read 1 - [the number you choose].txt for our documents):')
documents = []

#Grabs the seeds generated from one of our other codes
for i in range(int(numOfDocuments)):
    documents.append(open("pages/" + str(i+1) +'.txt', encoding="utf-8").read())

webpage = documents

cols = multTFIDscoresOfTweetsAndWebpage(tweet, webpage)
print(cols)
df = pd.read_csv(csvName + ".csv")
df['context_information'] = cols

#cannot append cols without brakets cause that is how the info is stored
print(df)
df.to_csv(csvName + ".csv", index=False)