import pandas as pd
import tweepy


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

print(df["username"])

#  consumer_key and consumer_secret go here
auth = tweepy.OAuthHandler('4HHuvkoNWfvXsJ2yG1T7nIbtM', '0YM963puOMmDOwId3UuxtC6nRdZw1A3H6IZq9EorgRXO4TfTlG')

# access_token and access_token_secret go here
auth.set_access_token('2856969806-KuiNT2Gu8xT3vdJDhiM79ut7MPh8ximDbZYBmBy',
                      'Lm5P9zI48q2HCaV4viqU1U0Ue11rlgrcAv33RieYuChMw')

# Authorizes the tweepy api
api = tweepy.API(auth)

'''for name in df["username"]:
    # the screen_name of the targeted user
    screen_name = str(name)

    # printing the latest 20 followers of the user
    for follower in api.followers(screen_name):
        print(follower.screen_name)

'''
for name in df["username"]:
    screen_name = str(name)
    c = tweepy.Cursor(api.followers, screen_name)

    k = list(c.items())
    print(k[0])

    # counting the number of followers
    '''count = 0
    for follower in c.items():
        count += 1
    print(screen_name + " has " + str(count) + " followers.")'''

thisdict = {
  "brand": ["Ford", "hello"],
  "model": ["Mustang", "ketchup"],
  "year": [9086, 83456]
}
print(thisdict["model"])
