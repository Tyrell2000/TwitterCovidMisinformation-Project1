
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from keras.models import Sequential
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
# from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus
import graphviz
from pydot import graph_from_dot_data
import io
from io import StringIO

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os


csvName = input('What is the name of the csv file you are opening?')
data = pd.read_csv(csvName +'.csv')


inputs = int(input('How many inputs will you be putting in (please type in number)?'))

n_most_common_words = 8000
max_len = 130

listOfSequences = []


# For every column that will be in the X axis, we clean the data and split the sentences into words, but excludes the stop words
listOfSequences = []
for i in range(inputs):

    columnName = input('What is the name of the column of input ' + str(i+1) + ' (X axis):')

    tokenizer = Tokenizer(num_words=n_most_common_words, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)

    tokenizer.fit_on_texts(data[columnName].values)

    sequences = tokenizer.texts_to_sequences(data[columnName].values)
    listOfSequences.append((pad_sequences(sequences, maxlen=max_len)))



# Turns all the columns in the listOfSequences into 1 column

yesno = input('Will you be adding context_information to the X-axis (y/n)?')

if yesno == 'Y' or 'y':
    tweetTFIDFs = []
    for row in data['context_information']:
        tweetTFIDF = np.array([])
        for value in row.split(','):
            tweetTFIDF = np.append(tweetTFIDF, float(value))
        tweetTFIDFs.append(tweetTFIDF)
    listOfSequences.append(np.stack(pad_sequences(tweetTFIDFs, dtype='float32'), axis=0))

X = np.concatenate(listOfSequences,axis=1)


# Turns 1 column into the Y axis
columnName = input('What is the name of the column of the output (Y axis)?')
Y = pd.get_dummies(data[columnName]).values

X_train, X_test, y_train, y_test = train_test_split(X , Y, test_size=0.3, random_state=42)

decision_tree = DecisionTreeClassifier(criterion = "gini", random_state = 100, max_depth=4, min_samples_leaf=11)
decision_tree = decision_tree.fit(X_train, y_train)

score = decision_tree.score(X_test, y_test)
print(score)


