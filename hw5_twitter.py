from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk


## SI 206 - HW
## COMMENT WITH:
## Your section day/time: 004 19:00-20:30 Mon
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

CACHE_FNAME = "twitter_cache.json"

try:
	cache_file = open(CACHE_FNAME, "r")
	cache_content = cache_file.read()
	CACHE_DICTION = json.loads(cache_content)
	cache_file.close()
except:
	CACHE_DICTION = {}

def uniq_id(base_url, params_dic):
	r = []
	for key in sorted(params_dic.keys()):
		r.append("{}={}".format(key,params_dic[key]))
	unique_id = base_url + "?" + "&".join(r)
	return unique_id

base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
param = {}
param["screen_name"] = username
param["count"] = num_tweets

unique_id = uniq_id(base_url, param)

if uniq_id in CACHE_DICTION:
	print("Fetching cached data...")
	tweets = CACHE_DICTION[unique_id]
else:
	print("Making a new data request...")
	response = requests.get(base_url, params=param, auth = auth)
	CACHE_DICTION[unique_id] = json.loads(response.text)
	dumped_json = json.dumps(CACHE_DICTION)
	cf = open(CACHE_FNAME, "w")
	cf.write(dumped_json)
	cf.close()
	tweets = CACHE_DICTION[unique_id]



#Code for Part 1:Get Tweets
base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params ={}
params["screen_name"] = username
params["count"] = num_tweets
r = requests.get(base_url, params=params, auth = auth)
umsi = json.loads(r.text)

f = open("tweet.json", "w")
f.write(json.dumps(umsi, indent=4))
f.close()

#Code for Part 2:Analyze Tweets
list_all = []
for t in tweets:
	tokenized_text = nltk.word_tokenize(t["text"])
	for w in tokenized_text:
		list_all.append(w)

list_sort = []
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
list_ignore = ["http", "https", "RT"]
for word in list_all:
	if word[0] not in alphabet:
		continue
	if word in list_ignore:
		continue
	else:
		list_sort.append(word)

sorted_word_dic = nltk.FreqDist(list_sort)

print("From", num_tweets, "tweets in", str(username) + "'s pofile, the 5 most common words are: ")
for word, freq in sorted_word_dic.most_common(5):
	print(word, ":", freq)


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
