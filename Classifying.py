from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import svm
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from matplotlib.pyplot import figure

twitterData = "C:\\Users\\tyrel\\OneDrive\\Desktop\\TwitterCovidMisinformation-Project1\\TwitterDataset.csv"

here = ['tweet_created_at', 'id_str', 'labelled', 'tweet_text', 'hashtags', 'source', 'user_id_str', 'user_name', 'user_screen_name', 'location', 'profile_location', 'user_profile_description', 'url', 'protected', 'followers_count', 'friends_count', 'listed_count', 'profile_created_at', 'favorites_count', 'utc_offset', 'geo_enabled', 'verified', 'statuses_count', 'lang', 'status', 'contributors_enabled', 'is_translation_enabled', 'tweet_geo', 'tweet_coordinates', 'tweet_place', 'tweet_contributors', 'tweet_is_quote_status', 'tweet_retweet_count', 'tweet_favorite_count']

data = pd.read_csv(twitterData, names=['tweet_created_at', 'id_str', 'labelled', 'tweet_text', 'hashtags', 'source',
                                       'user_id_str', 'user_name', 'user_screen_name', 'location', 'profile_location',
                                       'user_profile_description', 'url', 'protected', 'followers_count',
                                       'friends_count', 'listed_count', 'profile_created_at', 'favorites_count',
                                       'utc_offset', 'geo_enabled', 'verified', 'statuses_count', 'lang', 'status',
                                       'contributors_enabled', 'is_translation_enabled', 'tweet_geo',
                                       'tweet_coordinates', 'tweet_place', 'tweet_contributors',
                                       'tweet_is_quote_status', 'tweet_retweet_count', 'tweet_favorite_count'],
                   encoding='utf-8-sig')

##print(data.columns)
print(data.isnull().sum())

X = np.array(data.drop(columns='labelled'))
##for thing in data['tweet_favorite_count']:
    ##print(thing)
##print(data['labelled'])
y = np.array(data['labelled'])
##X = np.delete(X, [0, 1, 2, 3, 5, 7, 10, 11, 12, 13], axis=1)

'''
old_content_ratings = X[:, 1]
new_content_ratings = []
l = 0
for t in range(len(X[:, 1])):
    try:
        if new_content_ratings.index(old_content_ratings[t]) > -1:
            t = t
    except:
        if (old_content_ratings[t] != old_content_ratings[t]) and l != 1:
            new_content_ratings.append("Null")
            l = 1
        else:
            if old_content_ratings[t] != old_content_ratings[t]:
                l = l
            else:
                new_content_ratings.append(old_content_ratings[t])

improved_content_ratings = []
for e in range(len(old_content_ratings)):
    if old_content_ratings[e] != old_content_ratings[e]:
        improved_content_ratings.append(new_content_ratings.index("Null"))
    else:
        improved_content_ratings.append(new_content_ratings.index(old_content_ratings[e]))

X[:, 1] = improved_content_ratings

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


scores = []
scores2 = []
classification_methods = []
classification_methods2 = []


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


classifier = svm.SVC(kernel='linear', C=1, max_iter=10000).fit(X_train, y_train)
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