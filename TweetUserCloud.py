import time
import pandas as pd
import tweepy
from tweepy import API

# Followed this tutorial: https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f


twitterData = "C:\\Users\\tyrel\\OneDrive\\Desktop\\TwitterCovidMisinformation-Project1\\TwitterDataset.csv"

data = pd.read_csv(twitterData, names=['tweet_created_at', 'id_str', 'labelled', 'tweet_text', 'hashtags', 'source',
                                       'user_id_str', 'user_name', 'user_screen_name', 'location', 'profile_location',
                                       'user_profile_description', 'url', 'protected', 'followers_count',
                                       'friends_count', 'listed_count', 'profile_created_at', 'favorites_count',
                                       'utc_offset', 'geo_enabled', 'verified', 'statuses_count', 'lang', 'status',
                                       'contributors_enabled', 'is_translation_enabled', 'tweet_geo',
                                       'tweet_coordinates', 'tweet_place', 'tweet_contributors',
                                       'tweet_is_quote_status', 'tweet_retweet_count', 'tweet_favorite_count'],
                   encoding='latin-1')

col = ["user_id_str", "user_screen_name"]

df = data[col]
df.columns = ["id", "username"]

##print(df["username"])

#  consumer_key and consumer_secret go here
auth = tweepy.OAuthHandler('4HHuvkoNWfvXsJ2yG1T7nIbtM', '0YM963puOMmDOwId3UuxtC6nRdZw1A3H6IZq9EorgRXO4TfTlG')

# access_token and access_token_secret go here
auth.set_access_token('2856969806-KuiNT2Gu8xT3vdJDhiM79ut7MPh8ximDbZYBmBy',
                      'Lm5P9zI48q2HCaV4viqU1U0Ue11rlgrcAv33RieYuChMw')

# Authorizes the tweepy api
api = tweepy.API(auth, wait_on_rate_limit=True)

'''for name in df["username"]:
    # the screen_name of the targeted user
    screen_name = str(name)

    # printing the latest 20 followers of the user
    for follower in api.followers(screen_name):
        print(follower.screen_name)

'''
for name in df["username"]:
    for userName in df["username"]:
        k = 0

listOfUsers = df["username"]

tweetUserCloud = {}
tweetUserCloudPreliminary = {}

'''thisdict = {
    "brand": ["Ford"],
    "model": ["Mustang"],
    "jen": ["hello", "okau"]
}

for item in thisdict:
    for person in thisdict[item]:
        print(person)
        if person == thisdict[item][-1]:
            print("okayyyyyyy")

print("brand" in thisdict)'''

start = time.time()


def get_following(screen_name):
    print('Getting Following list of ', screen_name)
    users = tweepy.Cursor(api.friends, screen_name='@' + screen_name,
                          wait_on_rate_limit=True)
    try:
        for user in users.items():
            try:
                if screen_name not in tweetUserCloudPreliminary:
                    tweetUserCloudPreliminary[screen_name] = [str(user.screen_name)]
                else:
                    tweetUserCloudPreliminary[screen_name].append(str(user.screen_name))
                time.sleep(5)
            except tweepy.TweepError as e:
                print("Going to sleep:", e)
                time.sleep(60)
    except tweepy.TweepError as e:
        print("Going to sleep:", e)
        time.sleep(60)

    for following in tweetUserCloudPreliminary[screen_name]:
        if following in listOfUsers:
            if name not in tweetUserCloud:
                tweetUserCloud[name] = [following]
            else:
                tweetUserCloud[name].append(following)
            print(name, "follows", following)

    print('Fetched number of following for ' + screen_name + ' : ', len(tweetUserCloudPreliminary[screen_name]))


for user in df["username"][:-106]:
    get_following(user)

'''
start = time.time()

for name in df["username"]:
    print("Currently searching", name)
    for following in tweepy.Cursor(api.friends, screen_name=str(name)).items():
        if str(following.screen_name) in listOfUsers:
            if str(name) not in tweetUserCloud:
                tweetUserCloud[str(name)] = [str(following.screen_name)]
            else:
                tweetUserCloud[str(name)].append(str(following.screen_name))
            print(str(name), "follows", following.screen_name)

'''

userCloudFile = open("TweetUserCloud.txt", "w", encoding="utf-8")

try:
    for user in listOfUsers:
        if user in tweetUserCloud:
            for neighbor in tweetUserCloud[user]:
                if neighbor != tweetUserCloud[user][-1]:
                    userCloudFile.write(str(neighbor) + ", ")
                else:
                    userCloudFile.write(str(neighbor))
                    userCloudFile.write("\n")
        else:
            userCloudFile.write("N/A")
            userCloudFile.write("\n")
except():
    print("Error Happened!")

userCloudFile.close()

end = time.time()

print("Time Taken:", str(end - start))
