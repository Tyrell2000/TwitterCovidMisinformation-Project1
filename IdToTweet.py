# in pycharm, go to file, settings, project, project interpreter,
# click on the + and type in tweepy to install the tweepy library
import tweepy

# The consumer_key, consumer_secret, access_token, and access_token_secret are here for testing purposes, we need to replace them later.
#  consumer_key and consumer_secret go here
auth = tweepy.OAuthHandler('4HHuvkoNWfvXsJ2yG1T7nIbtM', '0YM963puOMmDOwId3UuxtC6nRdZw1A3H6IZq9EorgRXO4TfTlG')

# access_token and access_token_secret go here
auth.set_access_token('2856969806-KuiNT2Gu8xT3vdJDhiM79ut7MPh8ximDbZYBmBy', 'Lm5P9zI48q2HCaV4viqU1U0Ue11rlgrcAv33RieYuChMw')

# Authorizes the tweepy api
api = tweepy.API(auth)


# Make sure that when u open the csv file, it has encoding="utf-8"
# as it cant process tweets with emojis, ', and other stuff in it.
# The first slot in this is to make a file, the next slot is
# either 'w' (write), 'a' (append), or 'x' (create). https://www.w3schools.com/python/python_file_write.as
csv = open('a.csv', 'a', encoding="utf-8")

answer = input("Please put in the text file name of the tweet IDs: ")
tweetIDs = open(answer + ".txt", "r")

for tweetID in tweetIDs:
    tweet = api.get_status(tweetID, tweet_mode='extended')
    csv.write('"' + str(tweet.created_at).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.id_str).replace("\n", " ").replace('"', "'") + '",')
    textFromTweet = tweet.full_text.replace("\n", " ").replace('"', "'")

    if len(tweet.entities.get("urls")) > 0:
        for url in tweet.entities.get("urls"):
            textFromTweet = textFromTweet.replace(str(url.get("url")), "")

    csv.write('"' + textFromTweet + '",')

    csv.write('"' + "https:\\twitter.com\\" + str(tweet.user.screen_name).replace("\n", " ").replace('"', "'") +
              "\\status\\" + str(tweet.id_str).replace("\n", " ").replace('"', "'") + '",')

    if len(tweet.entities['hashtags']) > 0:
        hashtags = ""
        for i in range(len(tweet.entities['hashtags'])):
            if i != len(tweet.entities['hashtags']) - 1:
                hashtags = hashtags + \
                           str(tweet.entities['hashtags'][i]['text']).replace("\n", " ").replace('"',
                                                                                                 "'") + ', '
            else:
                hashtags = hashtags + \
                           str(tweet.entities['hashtags'][i]['text']).replace("\n", " ").replace('"', "'")
        csv.write('"' + hashtags + '",')
    else:
        csv.write('"' + "N/A" + '",')


    csv.write('"' + str(tweet.source).replace("\n", " ").replace('"', "'") + '",')

    if hasattr(tweet.user, 'id_str'):
        csv.write('"' + str(tweet.user.id_str).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'name'):
        csv.write('"' + str(tweet.user.name).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'screen_name'):
        csv.write('"' + str(tweet.user.screen_name).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'location'):
        csv.write('"' + str(tweet.user.location).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_location'):
        csv.write('"' + str(tweet.user.profile_location).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'description'):
        csv.write('"' + str(tweet.user.description).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'url'):
        csv.write('"' + str(tweet.user.url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'protected'):
        csv.write('"' + str(tweet.user.protected).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'followers_count'):
        csv.write('"' + str(tweet.user.followers_count).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'friends_count'):
        csv.write('"' + str(tweet.user.friends_count).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'listed_count'):
        csv.write('"' + str(tweet.user.listed_count).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'created_at'):
        csv.write('"' + str(tweet.user.created_at).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'favourites_count'):
        csv.write('"' + str(tweet.user.favourites_count).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'utc_offset'):
        csv.write('"' + str(tweet.user.utc_offset).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'geo_enabled'):
        csv.write('"' + str(tweet.user.geo_enabled).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'verified'):
        csv.write('"' + str(tweet.user.verified).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'statuses_count'):
        csv.write('"' + str(tweet.user.statuses_count).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'lang'):
        csv.write('"' + str(tweet.user.lang).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'status'):
        # Not sure if there needs to be more division, as I havent seen
        csv.write('"' + str(tweet.user.status).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'contributors_enabled'):
        csv.write('"' + str(tweet.user.contributors_enabled).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'is_translation_enabled'):
        csv.write('"' + str(tweet.user.is_translation_enabled).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    csv.write('"' + str(tweet.geo).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.coordinates).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.place).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.contributors).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.is_quote_status).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.retweet_count).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.favorite_count).replace("\n", " ").replace('"', "'") + '"')
    csv.write("\n")


csv.close()

