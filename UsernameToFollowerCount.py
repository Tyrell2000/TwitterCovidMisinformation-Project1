import tweepy

auth = tweepy.OAuthHandler('4HHuvkoNWfvXsJ2yG1T7nIbtM', '0YM963puOMmDOwId3UuxtC6nRdZw1A3H6IZq9EorgRXO4TfTlG')

auth.set_access_token('2856969806-KuiNT2Gu8xT3vdJDhiM79ut7MPh8ximDbZYBmBy', 'Lm5P9zI48q2HCaV4viqU1U0Ue11rlgrcAv33RieYuChMw')

api = tweepy.API(auth)

#Put usernames of accounts in here to  get ids from
ids=[]

followerCount=[]

for id in ids:

    # fetching the user
    user = api.get_user(id)

    #Adding user follower count to list
    followerCount.append(user.followers_count)

print(followerCount)

