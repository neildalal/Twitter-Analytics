# Twitter-Analytics

The code Twitter_Analytics.py extracts and analyses the data of any Twitter User. Specifically:
1) It prints the number of followers and the list of screen names of each of the followers.
2) Visualises the geographic distribution of the followers on a world map. One can zoom in/out and hover on the map to see the location, user id and no. of followers of that user.
3) Extract all the tweets from the user between any datetime period.
4) Resolve the Top 10 re-tweets, Top 10 most liked tweets, Top 10 most referenced Hashtags from this pool of tweets extracted in 3).
5) Check the number of followers of each follower of the user and print the top 10 most followed followers. (Helps to check if there is any influential person following that user).
6) Segregate and plot number of the tweets of the user into the types -> Retweet, Quote, Reply, Tweet.
7) Find the top 10 accounts to whom the user has replied to.
8) Calculate and plot the number of tweets depending on the day of the week on which they were tweeted

Inputs (Variables) to set in code:
1) The twitter user ('account')
2) The start and end date between which we want to extract the tweets ('start' and 'end')


Limitations:
1) Twitter allows a maximum of ~3000 followers to be extracted of a user in a 15min period. The code will wait for 15 minutes if the number of followers exceeds this.
2) Twitter allows a maximum of ~3200 tweets to be pulled in a 15min period. The code will wait for 15 minutes if the number of tweets exceeds this. 
3) I have used 'Nominatim' as the service provider to geocode the user locations. As it is free, it has a limitation of 1-2 requests/sec. One can use paid version of Google/Bing Maps instead to increase the speed of execution of code.
