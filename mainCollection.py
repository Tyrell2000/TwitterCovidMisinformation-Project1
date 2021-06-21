# in pycharm, go to file, settings, project, project interpreter,
# click on the + and type in tweepy to install the tweepy library
import tweepy

# The consumer_key, consumer_secret, access_token, and access_token_secret are here for testing purposes, we need to replace them later.
#  consumer_key and consumer_secret go here
auth = tweepy.OAuthHandler('', '')

# access_token and access_token_secret go here
auth.set_access_token('', '')

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
public_tweets = api.user_timeline(screen_name='@fema', count=200)

# Here is a list of all the data we are collecting/how the data is being stored in the CSV
csv.write('created_at,id,id_str,text,entities,source,source_url,in_reply_to_status_id,in_reply_to_status_id_str,in_reply_to_user_id,in_reply_to_user_id,in_reply_to_screen_name,user_id ,user_id_str ,user_name ,user_screen_name ,user_location ,user_profile_location ,user_description ,user_url ,user_entities ,user_protected ,user_followers_count ,user_friends_count ,user_listed_count ,user_created_at ,user_favourites_count ,user_utc_offset ,user_geo_enabled ,user_verified ,user_statuses_count ,user_lang ,user_status ,user_contributors_enabled ,user_is_translator ,user_is_translation_enabled ,user_profile_background_color ,user_profile_background_image_url ,user_profile_background_image_url_https ,user_profile_background_tile ,user_profile_image_url ,user_profile_image_url_https ,user_profile_banner_url ,user_profile_link_color ,user_profile_sidebar_border_color ,user_profile_sidebar_fill_color ,user_profile_text_color ,user_profile_use_background_image ,user_has_extended_profile ,user_default_profile ,user_default_profile_image ,user_following ,user_follow_request_sent, user_notifications,geo,coordinates,place,contributors,is_quote_status,retweet_count,favorite_count,favorited,retweeted,possibly_sensitive,lang')
csv.write('\n \n')


# To summarize this section, I more or less just got every item in Status object
# (the tweet) and am writing it to the CSV. https://www.geeksforgeeks.org/python-status-object-in-tweepy/
for tweet in public_tweets:
    csv.write('"' + str(tweet.created_at).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.id).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.id_str).replace("\n", " ").replace('"', "'") + '",')
    # Need to replace \n (newlines) in text as it will cause a new line in the CSV file
    # Need to convert " into ' in the text, as in order to keep commas in the text, we
    # have to put the sentence in "". Thus, if there are any sentences with a single "
    # (I ran into one during this), it will mess up the formatting
    csv.write('"' + tweet.text.replace("\n", " ").replace('"', "'") + '",')

    # Entities is an object with variation in the number of elements
    # after doing a few hours of work on this, it has been decided
    # that the best way to go about having this in the data is
    # to keep the data unedited (its gonna be a dict with an array in it, ect)
    csv.write('"' + str(tweet.entities).replace("\n", " ").replace('"', "'") + '",')

    csv.write('"' + str(tweet.source).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.source_url).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_status_id).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_status_id_str).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_user_id).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_user_id_str).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_screen_name).replace("\n", " ").replace('"', "'") + '",')

    # User is the other object with variation. However, this one we can
    # just check if certain attributes are here, and mark none if they aren't
    # present. This also has entities, so we will just have to leave that unedited.
    # anyways, you can skip the next like 200 lines or so, cause its all tweet.user.
    # This gives us data about the user. Source: https://www.geeksforgeeks.org/python-user-object-in-tweepy/
    # The original code for writing this to a file is below:
    # csv.write(str(tweet.user) + ",")

    if hasattr(tweet.user, 'id'):
        csv.write('"' + str(tweet.user.id).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

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

    # Tested to see if there was any way I could process the data consistently
    # with this. I could not find a way after a few hours, thus, this is
    # unedited data.
    if hasattr(tweet.user, 'entities'):
        csv.write('"' + str(tweet.user.entities).replace("\n", " ").replace('"', "'") + '",')
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

    if hasattr(tweet.user, 'is_translator'):
        csv.write('"' + str(tweet.user.is_translator).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'is_translation_enabled'):
        csv.write('"' + str(tweet.user.is_translation_enabled).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_background_color'):
        csv.write('"' + str(tweet.user.profile_background_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_background_image_url'):
        csv.write('"' + str(tweet.user.profile_background_image_url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_background_image_url_https'):
        csv.write('"' + str(tweet.user.profile_background_image_url_https).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_background_tile'):
        csv.write('"' + str(tweet.user.profile_background_tile).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_image_url'):
        csv.write('"' + str(tweet.user.profile_image_url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_image_url_https'):
        csv.write('"' + str(tweet.user.profile_image_url_https).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_banner_url'):
        csv.write('"' + str(tweet.user.profile_banner_url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_link_color'):
        csv.write('"' + str(tweet.user.profile_link_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_sidebar_border_color'):
        csv.write('"' + str(tweet.user.profile_sidebar_border_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_sidebar_fill_color'):
        csv.write('"' + str(tweet.user.profile_sidebar_fill_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_text_color'):
        csv.write('"' + str(tweet.user.profile_text_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_use_background_image'):
        csv.write('"' + str(tweet.user.profile_use_background_image).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'has_extended_profile'):
        csv.write('"' + str(tweet.user.has_extended_profile).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'default_profile'):
        csv.write('"' + str(tweet.user.default_profile).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'default_profile_image'):
        csv.write('"' + str(tweet.user.default_profile_image).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'following'):
        csv.write('"' + str(tweet.user.following).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'follow_request_sent'):
        csv.write('"' + str(tweet.user.follow_request_sent).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'notifications'):
        csv.write('"' + str(tweet.user.notifications).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

   # This is the end of tweet.user data

    csv.write('"' + str(tweet.geo).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.coordinates).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.place).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.contributors).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.is_quote_status).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.retweet_count).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.favorite_count).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.favorited).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.retweeted).replace("\n", " ").replace('"', "'") + '",')

    # Possibly_Sensitive throws us an error, so we cannot use it currently.
    if hasattr(tweet, 'possibly_sensitive'):
        csv.write('"' + str(tweet.possibly_sensitive) + '",')
    else:
        csv.write('"NoData",')
    csv.write('"' + str(tweet.lang).replace("\n", " ").replace('"', "'") + '"')

    csv.write("\n")

csv.close()

# backup of code in case testing something, and we need to get back to the original
"""
    csv.write('"' + str(tweet.created_at).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.id).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.id_str).replace("\n", " ").replace('"', "'") + '",')
    # Need to replace \n (newlines) in text as it will cause a new line in the CSV file
    # Need to convert " into ' in the text, as in order to keep commas in the text, we
    # have to put the sentence in "". Thus, if there are any sentences with a single "
    # (I ran into one during this), it will mess up the formatting
    csv.write('"' + tweet.text.replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.source).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.source_url).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_status_id).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_status_id_str).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_user_id).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_user_id_str).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.in_reply_to_screen_name).replace("\n", " ").replace('"', "'") + '",')

    # User is the other object with variation. This one is the trickiest
    # so basically we either do tweet.user or we access the stuff in the json.
    # Unfortunately, the _json is sensitive.
    # This gives us data about the user. Source: https://www.geeksforgeeks.org/python-user-object-in-tweepy/
    # The original code for writing this to a file is below:
    # csv.write(str(tweet.user) + ",")
    #for data in tweet.user._json:
    #    csv.write('"' + str(tweet.user._json.get(data)).replace("\n", " ").replace('"', "'") + '",')

    if hasattr(tweet.user, 'id'):
        csv.write('"' + str(tweet.user.id).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

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

    if hasattr(tweet.user, 'entities'):
        csv.write('"' + str(tweet.user.entities).replace("\n", " ").replace('"', "'") + '",')
        print(tweet.user.entities)
#        print(tweet.user.entities.get('url'))
#        print(tweet.user.entities.get('description').get('urls'))
#        print(tweet.user.entities.get('url').get('urls'))

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
        #Not sure if there needs to be more division, as I havent seen
        csv.write('"' + str(tweet.user.status).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'contributors_enabled'):
        csv.write('"' + str(tweet.user.contributors_enabled).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'is_translator'):
        csv.write('"' + str(tweet.user.is_translator).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'is_translation_enabled'):
        csv.write('"' + str(tweet.user.is_translation_enabled).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_background_color'):
        csv.write('"' + str(tweet.user.profile_background_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_background_image_url'):
        csv.write('"' + str(tweet.user.profile_background_image_url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_background_image_url_https'):
        csv.write('"' + str(tweet.user.profile_background_image_url_https).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_background_tile'):
        csv.write('"' + str(tweet.user.profile_background_tile).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_image_url'):
        csv.write('"' + str(tweet.user.profile_image_url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_image_url_https'):
        csv.write('"' + str(tweet.user.profile_image_url_https).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_banner_url'):
        csv.write('"' + str(tweet.user.profile_banner_url).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_link_color'):
        csv.write('"' + str(tweet.user.profile_link_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_sidebar_border_color'):
        csv.write('"' + str(tweet.user.profile_sidebar_border_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_sidebar_fill_color'):
        csv.write('"' + str(tweet.user.profile_sidebar_fill_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_text_color'):
        csv.write('"' + str(tweet.user.profile_text_color).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'profile_use_background_image'):
        csv.write('"' + str(tweet.user.profile_use_background_image).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'has_extended_profile'):
        csv.write('"' + str(tweet.user.has_extended_profile).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'default_profile'):
        csv.write('"' + str(tweet.user.default_profile).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'default_profile_image'):
        csv.write('"' + str(tweet.user.default_profile_image).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'following'):
        csv.write('"' + str(tweet.user.following).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'follow_request_sent'):
        csv.write('"' + str(tweet.user.follow_request_sent).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    if hasattr(tweet.user, 'notifications'):
        csv.write('"' + str(tweet.user.notifications).replace("\n", " ").replace('"', "'") + '",')
    else:
        csv.write('"' + "NONE" + '",')

    csv.write('"' + str(tweet.geo).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.coordinates).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.place).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.contributors).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.is_quote_status).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.retweet_count).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.favorite_count).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.favorited).replace("\n", " ").replace('"', "'") + '",')
    csv.write('"' + str(tweet.retweeted).replace("\n", " ").replace('"', "'") + '",')

    # Possibly_Sensitive throws us an error, so we cannot use it currently.
    # csv.write('"' + str(tweet.possibly_sensitive) + '",')
    csv.write('"' + str(tweet.lang).replace("\n", " ").replace('"', "'") + '"')


    # Entities is at the end cause it has variations in number
    # Entities is the first object that has variation to the number of things in it
    # so I split up all of the items in it. The original code for this (for the raw dict object) is:
    # csv.write(str(tweet.entities) + ",")
    for x in tweet.entities.get('user_mentions'):
        for y in x:
            csv.write('"' + str(x.get(y)).replace("\n", " ").replace('"', "'") + '",')


    csv.write("\n")


    """

# All possible things in tweet.user
"""
    tweet.user
    tweet.user.id
    tweet.user.id_str
    tweet.user.name
    tweet.user.screen_name
    tweet.user.location
    tweet.user.profile_location
    tweet.user.description
    tweet.user.url
    tweet.user.entities
    tweet.user.protected
    tweet.user.followers_count
    tweet.user.friends_count
    tweet.user.listed_count
    tweet.user.created_at
    tweet.user.favourites_count
    tweet.user.utc_offset
    tweet.user.geo_enabled
    tweet.user.verified
    tweet.user.statuses_count
    tweet.user.lang
    tweet.user.status
    tweet.user.contributors_enabled
    tweet.user.is_translator
    tweet.user.is_translation_enabled
    tweet.user.profile_background_color
    tweet.user.profile_background_image_url
    tweet.user.profile_background_image_url_https
    tweet.user.profile_background_tile
    tweet.user.profile_image_url
    tweet.user.profile_image_url_https
    tweet.user.profile_banner_url
    tweet.user.profile_link_color
    tweet.user.profile_sidebar_border_color
    tweet.user.profile_sidebar_fill_color
    tweet.user.profile_text_color
    tweet.user.profile_use_background_image
    tweet.user.has_extended_profile
    tweet.user.default_profile
    tweet.user.default_profile_image
    tweet.user.following
    tweet.user.follow_request_sent
    tweet.user.notifications
"""