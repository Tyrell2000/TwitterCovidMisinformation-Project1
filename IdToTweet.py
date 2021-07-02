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


name = input("Enter the name of the CVS file you are writting data to (file does not have to exist): ")

# Make sure that when u open the csv file, it has encoding="utf-8"
# as it cant process tweets with emojis, ', and other stuff in it.
# The first slot in this is to make a file, the next slot is
# either 'w' (write), 'a' (append), or 'x' (create). https://www.w3schools.com/python/python_file_write.as
csv = open(str(name) + '.csv', 'w', encoding="utf-8")

answer = input("Please put in the tweet ID which you would like to look up?: ")
tweetID = str(answer)




# Get the numbers from the tweet hyperlink and place them behind the comma
# For example my link is:
# https://twitter.com/Jane01010/status/1408413309112553476
# So my numbers are 1408413309112553476
# So public_tweets looks like:
# api.get_status(1339660498636333056, tweet_mode='extended')
public_tweets = api.get_status(tweetID, tweet_mode='extended')
#This will extract data and put it in the way we formatted it.
#The data will be placed in a file and it will be a CSV file, TwitterData.csv (text is printed for the retweets and likes in this)
#Also after doing 1 tweet, you can comment out line 50, as that is just to tell you what the columns represent







answer = input("Would you like a row of text that describes what is in each column? (Y/N): ")
YN = str(answer)

if YN == ('y' or 'Y'):
    # Here is a list of all the data we are collecting/how the data is being stored in the CSV
    csv.write('tweet_created_at, tweet_id_str, tweet_text, link_to_tweet, hashtags, urls_in_text, source, user_id_str,'
          'user_name, user_screen_name, location, profile_location, user_profile_description, url, protected,'
          'followers_count, friends_count, listed_count, profile_created_at, favorites_count, utc_offset, geo_enabled,'
          'verified, statuses_count, lang, status, contributors_enabled, is_translation_enabled, tweet_geo,'
          'tweet_coordinates, tweet_place, tweet_contributors, tweet_is_quote_status, tweet_retweet_count,'
          'tweet_favorite_count')
    csv.write('\n \n')


# To summarize this section, I more or less just got every item in Status object
# (the tweet) and am writing it to the CSV. https://www.geeksforgeeks.org/python-status-object-in-tweepy/
if public_tweets:
    ##Not collecting retweets currently
        ##print(tweet.full_text.replace("\n", " ").replace('"', "'"))
        ##print(tweet.entities)
        csv.write('"' + str(public_tweets.created_at).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(tweet.id).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.id_str).replace("\n", " ").replace('"', "'") + '",')

        # Need to replace \n (newlines) in text as it will cause a new line in the CSV file
        # Need to convert " into ' in the text, as in order to keep commas in the text, we
        # have to put the sentence in "". Thus, if there are any sentences with a single "
        # (I ran into one during this), it will mess up the formatting
        textFromTweet=public_tweets.full_text.replace("\n", " ").replace('"', "'")

        if len(public_tweets.entities.get("urls")) > 0:
            for url in public_tweets.entities.get("urls"):
                textFromTweet=textFromTweet.replace(str(url.get("url")), "")

        csv.write('"' + textFromTweet + '",')


        csv.write('"' + "https:\\twitter.com\\" + str(public_tweets.user.screen_name).replace("\n", " ").replace('"', "'") +
                  "\\status\\" + str(public_tweets.id_str).replace("\n", " ").replace('"', "'") + '",')

        # Entities is an object with variation in the number of elements
        # after doing a few hours of work on this, it has been decided
        # that the best way to go about having this in the data is
        # to keep the data unedited (its gonna be a dict with an array in it, ect)
        ##csv.write('"' + str(tweet.entities).replace("\n", " ").replace('"', "'") + '",')
        ##print('"' + str(tweet.entities).replace("\n", " ").replace('"', "'") + '",')

        if len(public_tweets.entities['hashtags']) > 0:
            hashtags = ""
            for i in range(len(public_tweets.entities['hashtags'])):
                if i != len(public_tweets.entities['hashtags']) - 1:
                    hashtags = hashtags +\
                               str(public_tweets.entities['hashtags'][i]['text']).replace("\n", " ").replace('"', "'") + ', '
                else:
                    hashtags = hashtags + \
                               str(public_tweets.entities['hashtags'][i]['text']).replace("\n", " ").replace('"', "'")
            csv.write('"' + hashtags + '",')
        else:
            csv.write('"' + "N/A" + '",')

        ##print(tweet.entities)
        if len(public_tweets.entities['urls']) > 0:
            urls = ""
            for i in range(len(public_tweets.entities['urls'])):
                if i != len(public_tweets.entities['urls']) - 1:
                    urls = urls +\
                               str(public_tweets.entities['urls'][i]['url']).replace("\n", " ").replace('"', "'") + ', '
                else:
                    urls = urls + \
                               str(public_tweets.entities['urls'][i]['url']).replace("\n", " ").replace('"', "'")
            csv.write('"' + urls + '",')
        else:
            csv.write('"' + "N/A" + '",')
        ##csv.write('"' + str(tweet.entities['hashtag'][0]).replace("\n", " ").replace('"', "'") + '",')

        csv.write('"' + str(public_tweets.source).replace("\n", " ").replace('"', "'") + '",')

        if hasattr(public_tweets.user, 'id_str'):
            csv.write('"' + str(public_tweets.user.id_str).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'name'):
            csv.write('"' + str(public_tweets.user.name).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'screen_name'):
            csv.write('"' + str(public_tweets.user.screen_name).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'location'):
            csv.write('"' + str(public_tweets.user.location).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'profile_location'):
            csv.write('"' + str(public_tweets.user.profile_location).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'description'):
            csv.write('"' + str(public_tweets.user.description).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'url'):
            csv.write('"' + str(public_tweets.user.url).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')


        if hasattr(public_tweets.user, 'protected'):
            csv.write('"' + str(public_tweets.user.protected).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'followers_count'):
            csv.write('"' + str(public_tweets.user.followers_count).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'friends_count'):
            csv.write('"' + str(public_tweets.user.friends_count).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'listed_count'):
            csv.write('"' + str(public_tweets.user.listed_count).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'created_at'):
            csv.write('"' + str(public_tweets.user.created_at).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'favourites_count'):
            csv.write('"' + str(public_tweets.user.favourites_count).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'utc_offset'):
            csv.write('"' + str(public_tweets.user.utc_offset).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'geo_enabled'):
            csv.write('"' + str(public_tweets.user.geo_enabled).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'verified'):
            csv.write('"' + str(public_tweets.user.verified).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'statuses_count'):
            csv.write('"' + str(public_tweets.user.statuses_count).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'lang'):
            csv.write('"' + str(public_tweets.user.lang).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'status'):
            # Not sure if there needs to be more division, as I havent seen
            csv.write('"' + str(public_tweets.user.status).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'contributors_enabled'):
            csv.write('"' + str(public_tweets.user.contributors_enabled).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')


        if hasattr(public_tweets.user, 'is_translation_enabled'):
            csv.write('"' + str(public_tweets.user.is_translation_enabled).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        csv.write('"' + str(public_tweets.geo).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.coordinates).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.place).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.contributors).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.is_quote_status).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.retweet_count).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.favorite_count).replace("\n", " ").replace('"', "'") + '"')

        csv.write("\n")


csv.close()

