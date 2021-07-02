# TwitterCovidMisinformation-Project1
Collection and classification of covid twitter data

mainCollection.py: Used to collect and store tweets

    near top of file:

    csv = open('filename.csv', 'edit mode(w = write(overwrites), a = append(adds to end of file, no overwrite)', encoding="utf-8")

    example usage: csv = open('TwitterData.csv', 'w', encoding="utf-8")

    ------------------------------------------------------------------------------------------------

    public_tweets = tweepy.Cursor(api.search, q='your search criteria -filter:retweets -filter:replies', tweet_mode='extended', lang='language here').items(x = how many tweets you want to gather(grabs last x tweets tweeted that match search criteria))

    example usage: public_tweets = tweepy.Cursor(api.search, q='#Coronavirus OR #COVID -filter:retweets -filter:replies', tweet_mode='extended', lang='en').items(100)

