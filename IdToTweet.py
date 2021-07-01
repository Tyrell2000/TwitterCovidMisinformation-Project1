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
csv = open('TwitterData.csv', 'a', encoding="utf-8")

# To my knowledge, we do user_timeline to get specific users. User_timeline
# does BOTH tweets and retweets on the specific twitter handle.
# The @____ is a twitter handle, count is number of tweets you want. There are more options.
# Here is the documentation for this: https://docs.tweepy.org/en/stable/api.html#timeline-methods
# Max number of tweets we can return is 200, unless we do a special method
# in which case, it is 3200.
#public_tweets = tweepy.Cursor(api.search, q='#covid blood clots -filter:retweets -filter:replies', tweet_mode='extended', lang='en').items(20)
public_tweets =  api.get_status(1339660498636333056, tweet_mode='extended')

# Here is a list of all the data we are collecting/how the data is being stored in the CSV
# csv.write('tweet_created_at, id_str, tweet_text, hashtags, source, user_id_str, user_name, user_screen_name, location, profile_location, user_profile_description, url, protected, followers_count, friends_count, listed_count, profile_created_at, favorites_count, utc_offset, geo_enabled, verified, statuses_count, lang, status, contributors_enabled, is_translation_enabled, tweet_geo, tweet_coordinates, tweet_place, tweet_contributors, tweet_is_quote_status, tweet_retweet_count, tweet_favorite_count,  tweet_link, hashtags, tweet_urls')
csv.write('\n \n')

retweets = 0

# To summarize this section, I more or less just got every item in Status object
# (the tweet) and am writing it to the CSV. https://www.geeksforgeeks.org/python-status-object-in-tweepy/
if public_tweets:
    if not public_tweets.retweeted:
        print(public_tweets.full_text.replace("\n", " ").replace('"', "'"))
        print(public_tweets.entities)
        csv.write('"' + str(public_tweets.created_at).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(public_tweets.id).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.id_str).replace("\n", " ").replace('"', "'") + '",')

        # Need to replace \n (newlines) in text as it will cause a new line in the CSV file
        # Need to convert " into ' in the text, as in order to keep commas in the text, we
        # have to put the sentence in "". Thus, if there are any sentences with a single "
        # (I ran into one during this), it will mess up the formatting
        textFromTweet=public_tweets.full_text.replace("\n", " ").replace('"', "'")

        if len(public_tweets.entities.get("urls")) > 0:
            i=0
            for url in public_tweets.entities.get("urls"):
                textFromTweet=textFromTweet.replace(str(url.get("url")), "")

        csv.write('"' + textFromTweet + '",')
        # Entities is an object with variation in the number of elements
        # after doing a few hours of work on this, it has been decided
        # that the best way to go about having this in the data is
        # to keep the data unedited (its gonna be a dict with an array in it, ect)
        ##csv.write('"' + str(public_tweets.entities).replace("\n", " ").replace('"', "'") + '",')
        ##print('"' + str(public_tweets.entities).replace("\n", " ").replace('"', "'") + '",')

        if len(public_tweets.entities['hashtags']) > 0:
            csv.write('"' + str(public_tweets.entities['hashtags'][0]['text']).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "N/A" + '",')
        ##csv.write('"' + str(public_tweets.entities['hashtag'][0]).replace("\n", " ").replace('"', "'") + '",')

        csv.write('"' + str(public_tweets.source).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(public_tweets.source_url).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(public_tweets.in_reply_to_status_id).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(public_tweets.in_reply_to_status_id_str).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(public_tweets.in_reply_to_user_id).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(public_tweets.in_reply_to_user_id_str).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(public_tweets.in_reply_to_screen_name).replace("\n", " ").replace('"', "'") + '",')

        # User is the other object with variation. However, this one we can
        # just check if certain attributes are here, and mark none if they aren't
        # present. This also has entities, so we will just have to leave that unedited.
        # anyways, you can skip the next like 200 lines or so, cause its all public_tweets.user.
        # This gives us data about the user. Source: https://www.geeksforgeeks.org/python-user-object-in-tweepy/
        # The original code for writing this to a file is below:
        # csv.write(str(public_tweets.user) + ",")

        ##if hasattr(public_tweets.user, 'id'):
            ##csv.write('"' + str(public_tweets.user.id).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

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

        # Tested to see if there was any way I could process the data consistently
        # with this. I could not find a way after a few hours, thus, this is
        # unedited data.
        ##if hasattr(public_tweets.user, 'entities'):
            ##csv.write('"' + str(public_tweets.user.entities).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

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

        ##if hasattr(public_tweets.user, 'is_translator'):
            ##csv.write('"' + str(public_tweets.user.is_translator).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        if hasattr(public_tweets.user, 'is_translation_enabled'):
            csv.write('"' + str(public_tweets.user.is_translation_enabled).replace("\n", " ").replace('"', "'") + '",')
        else:
            csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_background_color'):
            ##csv.write('"' + str(public_tweets.user.profile_background_color).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_background_image_url'):
            ##csv.write('"' + str(public_tweets.user.profile_background_image_url).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_background_image_url_https'):
            ##csv.write('"' + str(public_tweets.user.profile_background_image_url_https).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_background_tile'):
            ##csv.write('"' + str(public_tweets.user.profile_background_tile).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_image_url'):
            ##csv.write('"' + str(public_tweets.user.profile_image_url).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_image_url_https'):
            ##csv.write('"' + str(public_tweets.user.profile_image_url_https).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_banner_url'):
            ##csv.write('"' + str(public_tweets.user.profile_banner_url).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_link_color'):
            ##csv.write('"' + str(public_tweets.user.profile_link_color).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_sidebar_border_color'):
            ##csv.write('"' + str(public_tweets.user.profile_sidebar_border_color).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_sidebar_fill_color'):
            ##csv.write('"' + str(public_tweets.user.profile_sidebar_fill_color).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_text_color'):
            ##csv.write('"' + str(public_tweets.user.profile_text_color).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'profile_use_background_image'):
            ##csv.write('"' + str(public_tweets.user.profile_use_background_image).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'has_extended_profile'):
            ##csv.write('"' + str(public_tweets.user.has_extended_profile).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'default_profile'):
            ##csv.write('"' + str(public_tweets.user.default_profile).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'default_profile_image'):
            ##csv.write('"' + str(public_tweets.user.default_profile_image).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'following'):
            ##csv.write('"' + str(public_tweets.user.following).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'follow_request_sent'):
            ##csv.write('"' + str(public_tweets.user.follow_request_sent).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

        ##if hasattr(public_tweets.user, 'notifications'):
            ##csv.write('"' + str(public_tweets.user.notifications).replace("\n", " ").replace('"', "'") + '",')
        ##else:
            ##csv.write('"' + "NONE" + '",')

       # This is the end of public_tweets.user data

        csv.write('"' + str(public_tweets.geo).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.coordinates).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.place).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.contributors).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.is_quote_status).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.retweet_count).replace("\n", " ").replace('"', "'") + '",')
        csv.write('"' + str(public_tweets.favorite_count).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(public_tweets.favorited).replace("\n", " ").replace('"', "'") + '",')
        ##csv.write('"' + str(public_tweets.retweeted).replace("\n", " ").replace('"', "'") + '",')

        # Possibly_Sensitive throws us an error, so we cannot use it currently.
        ##if hasattr(tweet, 'possibly_sensitive'):
            ##csv.write('"' + str(public_tweets.possibly_sensitive) + '",')
        ##else:
            ##csv.write('"NoData",')
        ##csv.write('"' + str(public_tweets.lang).replace("\n", " ").replace('"', "'") + '"')

        csv.write('"twitter.com/anyuser/status/' + str(public_tweets.id_str).replace("\n", " ").replace('"', "'") + '",')




        print(hasattr(public_tweets.entities, 'hashtags'))
        if len(public_tweets.entities.get("hashtags")) > 0:
            csv.write('"')
            i=0
            for hashtag in public_tweets.entities.get("hashtags"):
                print(i)
                if (i == len(public_tweets.entities.get("hashtags")) - 1):
                    csv.write('#' + hashtag.get("text"))
                else:
                    csv.write('#' + hashtag.get("text") + ',')
                i=i+1
            csv.write('",')
        else:
            csv.write('"No hashtags",')


        if len(public_tweets.entities.get("urls")) > 0:
            csv.write('"')
            i=0
            for url in public_tweets.entities.get("urls"):
                print(i)
                if (i == len(public_tweets.entities.get("urls")) - 1):
                    csv.write('#' + url.get("expanded_url"))
                else:
                    csv.write('#' + url.get("expanded_url") + ',')
                i=i+1
            csv.write('"')
        else:
            csv.write('"No url"')


        csv.write("\n")

    else:
        retweets = retweets + 1

csv.close()

# backup of code in case testing something, and we need to get back to the original
"""
    csv.write('"' + str(public_tweets.created_at).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.id).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.id_str).replace("\n", " ").replace('"', "'") + '",')
    # Need to replace \n (newlines) in text as it will cause a new line in the CSV file
    # Need to convert " into ' in the text, as in order to keep commas in the text, we
    # have to put the sentence in "". Thus, if there are any sentences with a single "
    # (I ran into one during this), it will mess up the formatting
    csv.write('"' + public_tweets.text.replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.source).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.source_url).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.in_reply_to_status_id).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.in_reply_to_status_id_str).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.in_reply_to_user_id).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.in_reply_to_user_id_str).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.in_reply_to_screen_name).replace("\n", " ").replace('"', "'") + '",')

    # User is the other object with variation. This one is the trickiest
    # so basically we either do public_tweets.user or we access the stuff in the json.
    # Unfortunately, the _json is sensitive.
    # This gives us data about the user. Source: https://www.geeksforgeeks.org/python-user-object-in-tweepy/
    # The original code for writing this to a file is below:
    # csv.write(str(public_tweets.user) + ",")
    #for data in public_tweets.user._json:
    #    csv.write('"' + str(public_tweets.user._json.get(data)).replace("\n", " ").replace('"', "'") + '",')

    if hasattr(public_tweets.user, 'id'):
        csv.write('"' + str(public_tweets.user.id).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

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

    if hasattr(public_tweets.user, 'entities'):
        csv.write('"' + str(public_tweets.user.entities).replace("\n", " ").replace('"', "'") + '",')
        print(public_tweets.user.entities)
#        print(public_tweets.user.entities.get('url'))
#        print(public_tweets.user.entities.get('description').get('urls'))
#        print(public_tweets.user.entities.get('url').get('urls'))

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
        #Not sure if there needs to be more division, as I havent seen
        csv.write('"' + str(public_tweets.user.status).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'contributors_enabled'):
        csv.write('"' + str(public_tweets.user.contributors_enabled).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'is_translator'):
        csv.write('"' + str(public_tweets.user.is_translator).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'is_translation_enabled'):
        csv.write('"' + str(public_tweets.user.is_translation_enabled).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_background_color'):
        csv.write('"' + str(public_tweets.user.profile_background_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_background_image_url'):
        csv.write('"' + str(public_tweets.user.profile_background_image_url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_background_image_url_https'):
        csv.write('"' + str(public_tweets.user.profile_background_image_url_https).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_background_tile'):
        csv.write('"' + str(public_tweets.user.profile_background_tile).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_image_url'):
        csv.write('"' + str(public_tweets.user.profile_image_url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_image_url_https'):
        csv.write('"' + str(public_tweets.user.profile_image_url_https).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_banner_url'):
        csv.write('"' + str(public_tweets.user.profile_banner_url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_link_color'):
        csv.write('"' + str(public_tweets.user.profile_link_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_sidebar_border_color'):
        csv.write('"' + str(public_tweets.user.profile_sidebar_border_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_sidebar_fill_color'):
        csv.write('"' + str(public_tweets.user.profile_sidebar_fill_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_text_color'):
        csv.write('"' + str(public_tweets.user.profile_text_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'profile_use_background_image'):
        csv.write('"' + str(public_tweets.user.profile_use_background_image).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'has_extended_profile'):
        csv.write('"' + str(public_tweets.user.has_extended_profile).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'default_profile'):
        csv.write('"' + str(public_tweets.user.default_profile).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'default_profile_image'):
        csv.write('"' + str(public_tweets.user.default_profile_image).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'following'):
        csv.write('"' + str(public_tweets.user.following).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'follow_request_sent'):
        csv.write('"' + str(public_tweets.user.follow_request_sent).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(public_tweets.user, 'notifications'):
        csv.write('"' + str(public_tweets.user.notifications).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    csv.write('"' + str(public_tweets.geo).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.coordinates).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.place).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.contributors).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.is_quote_status).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.retweet_count).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.favorite_count).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.favorited).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(public_tweets.retweeted).replace("\n", " ").replace('"', "'") + '",')

    # Possibly_Sensitive throws us an error, so we cannot use it currently.
    # csv.write('"' + str(public_tweets.possibly_sensitive) + '",')
    csv.write('"' + str(public_tweets.lang).replace("\n", " ").replace('"', "'") + '"')


    # Entities is at the end cause it has variations in number
    # Entities is the first object that has variation to the number of things in it
    # so I split up all of the items in it. The original code for this (for the raw dict object) is:
    # csv.write(str(public_tweets.entities) + ",")
    for x in public_tweets.entities.get('user_mentions'):
        for y in x:
            csv.write('"' + str(x.get(y)).replace("\n", " ").replace('"', "'") + '",')


    csv.write("\n")


    """

# All possible things in public_tweets.user
"""
    public_tweets.user
    public_tweets.user.id
    public_tweets.user.id_str
    public_tweets.user.name
    public_tweets.user.screen_name
    public_tweets.user.location
    public_tweets.user.profile_location
    public_tweets.user.description
    public_tweets.user.url
    public_tweets.user.entities
    public_tweets.user.protected
    public_tweets.user.followers_count
    public_tweets.user.friends_count
    public_tweets.user.listed_count
    public_tweets.user.created_at
    public_tweets.user.favourites_count
    public_tweets.user.utc_offset
    public_tweets.user.geo_enabled
    public_tweets.user.verified
    public_tweets.user.statuses_count
    public_tweets.user.lang
    public_tweets.user.status
    public_tweets.user.contributors_enabled
    public_tweets.user.is_translator
    public_tweets.user.is_translation_enabled
    public_tweets.user.profile_background_color
    public_tweets.user.profile_background_image_url
    public_tweets.user.profile_background_image_url_https
    public_tweets.user.profile_background_tile
    public_tweets.user.profile_image_url
    public_tweets.user.profile_image_url_https
    public_tweets.user.profile_banner_url
    public_tweets.user.profile_link_color
    public_tweets.user.profile_sidebar_border_color
    public_tweets.user.profile_sidebar_fill_color
    public_tweets.user.profile_text_color
    public_tweets.user.profile_use_background_image
    public_tweets.user.has_extended_profile
    public_tweets.user.default_profile
    public_tweets.user.default_profile_image
    public_tweets.user.following
    public_tweets.user.follow_request_sent
    public_tweets.user.notifications
"""

