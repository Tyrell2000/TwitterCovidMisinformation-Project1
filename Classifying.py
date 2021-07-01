from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
from sklearn import svm
from IPython.display import display
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import plot_confusion_matrix, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.feature_selection import chi2
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from matplotlib.pyplot import figure

# Followed this tutorial: https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f

twitterData = "C:\\Users\\tyrel\\OneDrive\\Desktop\\TwitterCovidMisinformation-Project1\\TwitterDataset.csv"

here = ['tweet_created_at', 'id_str', 'labelled', 'tweet_text', 'hashtags', 'source', 'user_id_str', 'user_name',
        'user_screen_name', 'location', 'profile_location', 'user_profile_description', 'url', 'protected',
        'followers_count', 'friends_count', 'listed_count', 'profile_created_at', 'favorites_count', 'utc_offset',
        'geo_enabled', 'verified', 'statuses_count', 'lang', 'status', 'contributors_enabled', 'is_translation_enabled',
        'tweet_geo', 'tweet_coordinates', 'tweet_place', 'tweet_contributors', 'tweet_is_quote_status',
        'tweet_retweet_count', 'tweet_favorite_count']

data = pd.read_csv(twitterData, names=['tweet_created_at', 'id_str', 'labelled', 'tweet_text', 'hashtags', 'source',
                                       'user_id_str', 'user_name', 'user_screen_name', 'location', 'profile_location',
                                       'user_profile_description', 'url', 'protected', 'followers_count',
                                       'friends_count', 'listed_count', 'profile_created_at', 'favorites_count',
                                       'utc_offset', 'geo_enabled', 'verified', 'statuses_count', 'lang', 'status',
                                       'contributors_enabled', 'is_translation_enabled', 'tweet_geo',
                                       'tweet_coordinates', 'tweet_place', 'tweet_contributors',
                                       'tweet_is_quote_status', 'tweet_retweet_count', 'tweet_favorite_count'],
                   encoding='latin-1')

##print(data.columns)
##print(data.isnull().sum())

##print(data.head())

col = ["tweet_text", "labelled"]

df = data[col]
df.columns = ["text", "label"]

##print(df.head)

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2),
                        stop_words='english')

features = tfidf.fit_transform(df.text).toarray()
labels = df.label

df['category_id'] = df['label'].factorize()[0]
category_id_df = df[['label', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'label']].values)

X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], train_size=0.3, random_state=0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)

models = [
    RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
    LinearSVC(max_iter=10000),
    MultinomialNB(),
    LogisticRegression(random_state=0),
]
CV = 5
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
    model_name = model.__class__.__name__
    accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
    for fold_idx, accuracy in enumerate(accuracies):
        entries.append((model_name, fold_idx, accuracy))
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

sns.boxplot(x='model_name', y='accuracy', data=cv_df)
sns.stripplot(x='model_name', y='accuracy', data=cv_df,
              size=8, jitter=True, edgecolor="gray", linewidth=2)
##plt.show()

model = LinearSVC()
X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index,
                                                                                 test_size=0.7, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=category_id_df.label.values, yticklabels=category_id_df.label.values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

'''for predicted in category_id_df.category_id:
    ##print(category_id_df)
    ##print(category_id_df.category_id)
    for actual in category_id_df.category_id:
        if predicted != actual:
            print(category_id_df['text'])
            print("'{}' predicted as '{}' : {} examples.".format(id_to_category[actual], id_to_category[predicted],
                                                                 conf_mat[actual, predicted]))
            display(df.loc[indices_test[(y_test == actual) & (y_pred == predicted)]][['label', 'text']])
            print(conf_mat[actual, predicted])
            print('')

        if predicted == actual:
            print("'{}' predicted correctly: {} examples.".format(id_to_category[actual], id_to_category[predicted],
                                                                 conf_mat[actual, predicted]))
            display(df.loc[indices_test[(y_test == actual) & (y_pred == predicted)]][['label', 'text']])
            print('')'''

'''
X = np.array(data["tweet_text"])
##for thing in data['tweet_favorite_count']:
    ##print(thing)
##print(data['labelled'])
y = np.array(data['labelled'])
##X = np.delete(X, [0, 1, 2, 3, 5, 7, 10, 11, 12, 13], axis=1)


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


scores = []
scores2 = []
classification_methods = []
classification_methods2 = []
'''
'''
results = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)
score = results.score(X_test, y_test)
score2 = cross_val_score(KNeighborsClassifier(n_neighbors=3), X_test, y_test, cv=5)

scores.append(np.mean(score))
scores2.append(np.mean(score2))
classification_methods.append('KNeighbors')
classification_methods2.append('KNeighbors2')


results = LogisticRegression(max_iter=10000000).fit(X_train, y_train)
score = results.score(X_test, y_test)
score2 = cross_val_score(LogisticRegression(max_iter=10000000), X_test, y_test, cv=5)

scores.append(np.mean(score))
scores2.append(np.mean(score2))
classification_methods.append('LogisticRegression')
classification_methods2.append('LogisticRegression2')


results = MultinomialNB().fit(X_train, y_train)
score = results.score(X_test, y_test)
score2 = cross_val_score(MultinomialNB(), X_test, y_test, cv=5)

scores.append(np.mean(score))
scores2.append(np.mean(score2))
classification_methods.append('MultinomialNB')
classification_methods2.append('MultinomialNB2')


results = BernoulliNB().fit(X_train, y_train)
score = results.score(X_test, y_test)
score2 = cross_val_score(BernoulliNB(), X_test, y_test, cv=5)

scores.append(np.mean(score))
scores2.append(np.mean(score2))
classification_methods.append('BernoulliNB')
classification_methods2.append('BernoulliNB2')


results = DecisionTreeClassifier().fit(X_train, y_train)
score = results.score(X_test, y_test)
score2 = cross_val_score(DecisionTreeClassifier(), X_test, y_test, cv=5)

scores.append(np.mean(score))
scores2.append(np.mean(score2))
classification_methods.append('DecisionTree')
classification_methods2.append('DecisionTree2')


results = LinearSVC(max_iter=1000).fit(X_train, y_train)
score = results.score(X_test, y_test)
score2 = cross_val_score(LinearSVC(max_iter=1000), X_test, y_test, cv=5)

scores.append(np.mean(score))
scores2.append(np.mean(score2))
classification_methods.append('LinearSVC')
classification_methods2.append('LinearSVC2')


results = MLPClassifier(max_iter=1000).fit(X_train, y_train)
score = results.score(X_test, y_test)
score2 = cross_val_score(MLPClassifier(max_iter=100), X_test, y_test, cv=5)

scores.append(np.mean(score))
scores2.append(np.mean(score2))
classification_methods.append('MLP')
classification_methods2.append('MLP2')


count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X)
X_train_counts.shape

tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape

classifier = svm.SVC(kernel='linear', C=1, max_iter=10000).fit(X_train_tf, y_train)
disp = plot_confusion_matrix(classifier, X_test, y_test, normalize='true')
scoresy = [disp.confusion_matrix[0][0], disp.confusion_matrix[1][1]]
score3 = np.average(scoresy)


figure(num=None, figsize=(100, 100), dpi=200, facecolor='w', edgecolor='k')

xpos = np.arange(start=1, stop=(len(classification_methods) * 2) + 1, step=2)
xpo2 = np.arange(start=2, stop=(len(classification_methods2) * 2) + 1, step=2)

plt.xticks(xpos, classification_methods)

for i in range(len(classification_methods)):
    if i == 0:
        plt.bar(classification_methods[i], scores[i], label='Test', align='center', color='green')
        plt.bar(classification_methods2[i], scores2[i], label='K-Fold', color='cyan')
    else:
        plt.bar(classification_methods[i], scores[i], align='center', color='green')
        plt.bar(classification_methods2[i], scores2[i], color='cyan')

plt.bar('ConfusionMatrix', score3, label='Confusion Matrix', color='blue')

plt.legend()
plt.show()
'''
