import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from keras.models import Sequential
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import sys
np.set_printoptions(threshold=sys.maxsize)
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os

#Test Runs
epochs = 10000

#The fixed length of the vector
emb_dim = 100

#Number of datas / by
batch_size = 2

csvName = input('What is the name of the csv file you are opening?')
data = pd.read_csv(csvName +'.csv')

# Turns ___ column into the X axis
inputs = int(input('How many inputs will you be putting in that are not the context_information (please type in number)?'))

n_most_common_words = 8000
max_len = 130


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

if len(listOfSequences) >1:
    X = np.concatenate(listOfSequences,axis=1)
else:
    X =listOfSequences[0]


# Turns 1 column into the Y axis
columnName = input('What is the name of the column of the output (Y axis)?')
Y = pd.get_dummies(data[columnName]).values

#Turning the X and Y column data into test and training data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

model = Sequential()
model.add(Embedding(n_most_common_words, emb_dim, input_length=X.shape[1]))
model.add(SpatialDropout1D(0.7))
model.add(LSTM(64, dropout=0.7, recurrent_dropout=0.7))
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=0,
                    callbacks=[EarlyStopping(monitor='val_loss', patience=7, min_delta=0.0001)])

accr = model.evaluate(X_test, y_test, verbose=0)
print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))