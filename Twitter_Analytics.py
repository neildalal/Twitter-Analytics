#!/usr/bin/env python
# coding: utf-8

# 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐨𝐟 𝐓𝐰𝐢𝐭𝐭𝐞𝐫 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐨𝐟 𝐃𝐢𝐠𝐢𝐭 𝐈𝐧𝐬𝐮𝐫𝐚𝐧𝐜𝐞 (@𝐡𝐞𝐲𝐝𝐢𝐠𝐢𝐭)

# In[4]:


account = 'tag8_official' #enter twitter id

import tweepy
import pycountry
import pandas as pd
from matplotlib import pyplot as plt
from geopy.geocoders import Nominatim
import plotly.express as px

# Connect to the Twitter API
consumer_key= 'aCDpd0xMeBmzof2vITvOiMKeT'
consumer_secret= '84rzxwrekt6wpCKZ7CDYYW31x5zwclRo0h8gccYkjp0B6jpwpw'
access_token= '1489607100519297024-UUFseTpA9D3wcB61ow09g0SL8Cg5JI'
access_token_secret= 'O6xhnyNnToHJPkvEI1O4dLqK3yJzsLKCJop5NKp0oErJy'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Finding all the followers of the account
follower_ids = []
foll_follcount = []
temp_locations = []
for follower in tweepy.Cursor(api.get_followers, screen_name = account, count = 200).items():
    foll_follcount.append(follower.followers_count)
    follower_ids.append(follower.screen_name)
    temp_locations.append(follower.location)

print("Number of Followers", len(follower_ids)) # Print number of followers
print("\n")
print(follower_ids) #Print screen_name of all the followers

# Function used to geocode a location
def geocode_add(address):
    geopy = Nominatim(user_agent = "Student")
    try:
        return geopy.geocode(address,exactly_one=True)
    except:
       return None  

# Convert locations to a Geocoded Location 
new_list = []
for (i, x) in enumerate(temp_locations):
    if x == None:
        follower_ids[i] = None
        foll_follcount[i] = None
        new_list.append(None)
    else:
        #print(i)
        new_list.append(geocode_add(x))
   
# Get latitude and Longitude from geocoded address
user = []
followers_count = []
add = []    
lat=[]
long=[]
for (i, x) in enumerate(new_list):
    if x == None:
        user.append(None)
        followers_count.append(None)
        add.append(None)
        lat.append(None)
        long.append(None)
    else:
        user.append(follower_ids[i])
        followers_count.append(foll_follcount[i]) 
        add.append(x.address)
        lat.append(x.latitude)
        long.append(x.longitude)

df = pd.DataFrame({'add' : add, 'lat': lat,'long': long, 'user': user, 'followers': followers_count}) 


# In[5]:


#Plot the geographic distribution of the followers
fig = px.scatter_geo(df,lat='lat',lon='long', hover_name="add", hover_data=["user", "followers"])
fig.update_layout(title = 'Geographic Distribution of Twitter Followers', title_x=0.5)
fig.show()   


# In[6]:


import datetime
import pytz

#Set Timedate period (year, month, day, hr, min, sec, us, timezone info)
start = datetime.datetime(2016, 1, 4, 0, 0, 0, 0, pytz.UTC)
end =   datetime.datetime(2022, 2, 8, 0, 0, 0, 0, pytz.UTC)

req_tweets = [] #store in this all tweets extracted in the above time period

Get_Tweets = api.user_timeline(screen_name=account,count=200)
for tweet in Get_Tweets:
    if tweet.created_at > start and tweet.created_at < end:
        req_tweets.append(tweet)

checker = Get_Tweets[-1].created_at        
while (Get_Tweets[-1].created_at > start):
    Get_Tweets = api.user_timeline(screen_name=account, max_id = Get_Tweets[-1].id, count = 200)

    for tweet in Get_Tweets:
        if tweet.created_at > start and tweet.created_at < end:
            if not (tweet in req_tweets):
                req_tweets.append(tweet)
                
    if checker == Get_Tweets[-1].created_at:
        break
    else:
        checker = Get_Tweets[-1].created_at                
 
hashtags = {}
replied_users = {}
weekday = [0,0,0,0,0,0,0]
titles = {'Text':[], 'Time':[], 'Retweet Count':[], 'Likes Count':[]}
tweet_distribution = {'Reply':0, 'Quote':0, 'Retweet':0, 'Tweet':0}
df = pd.DataFrame(titles)
for tweet in req_tweets:
    entry = [tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
    df.loc[len(df.index)] = entry
        
    if tweet.is_quote_status:
        tweet_distribution['Quote'] += 1
    elif not (tweet.in_reply_to_status_id == None) :
        tweet_distribution['Reply'] += 1
        if tweet.in_reply_to_screen_name in replied_users:
            replied_users[tweet.in_reply_to_screen_name] += 1
        else :
            replied_users[tweet.in_reply_to_screen_name] = 1
    elif hasattr(tweet, 'retweeted_status'):
        tweet_distribution['Retweet'] += 1
    else:
        tweet_distribution['Tweet'] += 1
    
    for i in tweet.entities['hashtags']:
        if i['text'] in hashtags:
            hashtags[i['text']] += 1
        else:
            hashtags[i['text']] = 1
    
    weekday[tweet.created_at.weekday()] += 1
    
top_hash = pd.DataFrame(hashtags.items(),columns = ['Hashtags','Frequency'])

top_hash.sort_values(by = 'Frequency', ascending = False, inplace=True, ignore_index=True)
top_retweeted = df.sort_values(by = 'Retweet Count', ascending = False, ignore_index=True)
top_liked = df.sort_values(by = 'Likes Count', ascending = False, ignore_index=True)

display(top_retweeted[0:10])
display(top_liked[0:10])
display(top_hash[0:10])


# In[7]:


influencers = {'User':follower_ids, 'Followers Count':foll_follcount}
influencer = pd.DataFrame(influencers)
influencer.sort_values(by = 'Followers Count', ascending = False, inplace=True, ignore_index=True)
display(influencer)


# In[8]:


df = pd.DataFrame(tweet_distribution.items(),columns = ['Tweet_type','count'])
df2 = pd.DataFrame(replied_users.items(),columns = ['Replied to User','count'])

tweet_type = df['Tweet_type']
count = df['count']
 
# Figure Size
fig, ax = plt.subplots(figsize =(8, 5))
 
# Horizontal Bar Plot
ax.barh(tweet_type, count)
 
# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)
 
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
 
ax.invert_yaxis()

for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
ax.set_title('Tweet Type Distribution', loc ='left')
plt.show()

display(df2.sort_values(by = 'count', ascending = False, ignore_index=True))


# In[9]:


dict = {'Monday': weekday[0], 'Tuesday': weekday[1], 'Wednesday': weekday[2], 'Thursday': weekday[3], 'Friday': weekday[4], 'Saturday': weekday[5], 'Sunday': weekday[6]}
df = pd.DataFrame(dict.items(),columns = ['Day of the Week','Tweet count'])

weekday = df['Day of the Week']
count = df['Tweet count']
 
## Figure Size
fig, ax = plt.subplots(figsize =(8, 5))
 
# Horizontal Bar Plot
ax.barh(weekday, count)
 
# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)
 
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
 
ax.invert_yaxis()

for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
ax.set_title('No. of Tweets depending on the day of the week', loc ='left')
plt.show()

