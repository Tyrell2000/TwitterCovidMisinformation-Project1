# in pycharm, go to file, settings, project, project interpreter,
# click on the + and type in tweepy to install the tweepy library
import tweepy
import os

def tweetGetter(public_tweets, csv):
    # To summarize this section, I more or less just got every item in Status object
    # (the tweet) and am writing it to the CSV. https://www.geeksforgeeks.org/python-status-object-in-tweepy/
    for tweet in public_tweets:
        if not tweet.retweeted:
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

            if len(tweet.entities['urls']) > 0:
                urls = ""
                for i in range(len(tweet.entities['urls'])):
                    if i != len(tweet.entities['urls']) - 1:
                        urls = urls + \
                               str(tweet.entities['urls'][i]['url']).replace("\n", " ").replace('"', "'") + ', '
                    else:
                        urls = urls + \
                               str(tweet.entities['urls'][i]['url']).replace("\n", " ").replace('"', "'")
                csv.write('"' + urls + '",')
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

        else:
            retweets = retweets + 1



# The consumer_key, consumer_secret, access_token, and access_token_secret are here for testing purposes,
# we need to replace them later.
#  consumer_key and consumer_secret go here
auth = tweepy.OAuthHandler('4HHuvkoNWfvXsJ2yG1T7nIbtM', '0YM963puOMmDOwId3UuxtC6nRdZw1A3H6IZq9EorgRXO4TfTlG')

# access_token and access_token_secret go here
auth.set_access_token('2856969806-KuiNT2Gu8xT3vdJDhiM79ut7MPh8ximDbZYBmBy',
                      'Lm5P9zI48q2HCaV4viqU1U0Ue11rlgrcAv33RieYuChMw')

# Authorizes the tweepy api
api = tweepy.API(auth)

name = input("Enter the name of the CVS file you are writting data to (file does not have to exist): ")

# Make sure that when u open the csv file, it has encoding="utf-8"
# as it cant process tweets with emojis, ', and other stuff in it.
# The first slot in this is to make a file, the next slot is
# either 'w' (write), 'a' (append), or 'x' (create). https://www.w3schools.com/python/python_file_write.as
csv = open(str(name) + '.csv', 'a', encoding="utf-8")

csv.write('tweet_created_at, tweet_id_str, tweet_text, link_to_tweet, hashtags, urls_in_text, source, user_id_str,'
          'user_name, user_screen_name, location, profile_location, user_profile_description, url, protected,'
          'followers_count, friends_count, listed_count, profile_created_at, favorites_count, utc_offset, geo_enabled,'
          'verified, statuses_count, lang, status, contributors_enabled, is_translation_enabled, tweet_geo,'
          'tweet_coordinates, tweet_place, tweet_contributors, tweet_is_quote_status, tweet_retweet_count,'
          'tweet_favorite_count')

languages = ['en', 'es', 'ru', 'zh-cn', 'tr']
for lang in languages:
    print("\n"*2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("This is for the tweets that are in " + lang + ":")
    print(" ")
    print("NOTE: current version excludes retweets and replies. To remove this feature, get rid of the ' -filter:retweets -filter:replies' in line 43 along with any other filtering by retweets and replies: ")
    answer = input("What is the search term(s), hashtag(s), or query you would like to look up?: ")
    query = str(answer)


    #answer = input("How many tweets would you like? (MAX:200): ")
    num = 50

    # To my knowledge, we do user_timeline to get specific users. User_timeline
    # does BOTH tweets and retweets on the specific twitter handle.
    # The @____ is a twitter handle, count is number of tweets you want. There are more options.
    # Here is the documentation for this: https://docs.tweepy.org/en/stable/api.html#timeline-methods
    # Max number of tweets we can return is 200, unless we do a special method
    # in which case, it is 3200.
    public_tweets = tweepy.Cursor(api.search, q= query +' -filter:retweets -filter:replies',
                                  tweet_mode='extended', lang=lang).items(num)

    tweetGetter(public_tweets, csv)

csv.close()
