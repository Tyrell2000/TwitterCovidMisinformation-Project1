
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

#Test Runs
epochs = 1000
emb_dim = 156
#Number of datas / by
batch_size = 2

data = pd.read_csv('TwitterData.csv')
#data = pd.read_csv('uci-news-aggregator.csv')

#data.tweet_text.value_counts()


n_most_common_words = 8000
max_len = 130
tokenizer = Tokenizer(num_words=n_most_common_words, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
#tokenizer.fit_on_texts(data['TITLE'].values)
tokenizer.fit_on_texts(data['tweet_text'].values)
#sequences = tokenizer.texts_to_sequences(data['TITLE'].values)
sequences = tokenizer.texts_to_sequences(data['tweet_text'].values)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

X = pad_sequences(sequences, maxlen=max_len)
print(X)

#Y = pd.get_dummies(data['CATEGORY']).values
Y = pd.get_dummies(data['classification']).values
print(Y)

X_train, X_test, y_train, y_test = train_test_split(X , Y, test_size=0.3, random_state=42)
print((X_train.shape, y_train.shape, X_test.shape, y_test.shape))

decision_tree = DecisionTreeClassifier(criterion = "gini", random_state = 100, max_depth=4, min_samples_leaf=11)
decision_tree = decision_tree.fit(X_train, y_train)

score = decision_tree.score(X_test, y_test)
print(score)


