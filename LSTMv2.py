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
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os

#Test Runs
epochs = 10000
emb_dim = 100
#Number of datas / by
batch_size = 2

csvName = input('What is the name of the csv file you are opening?')
data = pd.read_csv(csvName +'.csv')


inputs = int(input('How many inputs will you be putting in (please type in number)?'))

n_most_common_words = 8000
max_len = 130

listOfSequences = []
for i in range(inputs):

    columnName = input('What is the name of the column of input ' + str(i+1) + ' (X axis):')

    tokenizer = Tokenizer(num_words=n_most_common_words, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)

    #tokenizer.fit_on_texts(data['tweet_text'].values)
    tokenizer.fit_on_texts(data[columnName].values)

    #sequences = tokenizer.texts_to_sequences(data['tweet_text'].values)
    sequences = tokenizer.texts_to_sequences(data[columnName].values)
    listOfSequences.append((pad_sequences(sequences, maxlen=max_len)))

X = np.concatenate(listOfSequences,axis=1)
#print(X)

columnName = input('What is the name of the column of the output (Y axis)?')
Y = pd.get_dummies(data[columnName]).values
#print(Y)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

print((X_train.shape, y_train.shape, X_test.shape, y_test.shape))

model = Sequential()
model.add(Embedding(n_most_common_words, emb_dim, input_length=X.shape[1]))
model.add(SpatialDropout1D(0.7))
model.add(LSTM(64, dropout=0.7, recurrent_dropout=0.7))
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

accr = model.evaluate(X_test,y_test)
print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))