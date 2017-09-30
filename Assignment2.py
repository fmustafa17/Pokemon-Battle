# -*- coding: cp1252 -*-
## Farhana Mustafa
## My code is under all these pound signs!

import twitter
import networkx as nx
import operator
import sys
import datetime
import time

############################################################################ 
def oauth_login():
    CONSUMER_KEY = 'Els9Ab9OjdgLSJSDWcypZ8IW0'
    CONSUMER_SECRET = '5eIMZKPUCrGJU5gc7hT8QKeCdSGrlm6luvYromRPivCnWojyxV'
    OAUTH_TOKEN = '742382169801252864-kNe1u25gVwsZUs7o2ibIzWQA0ZZN39U'
    OAUTH_TOKEN_SECRET = 'p2eqnfdlFx0VswpzF6NuFI8zdpSbsgjD2c8YlaPExcBuV'

    auth = twitter.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                         CONSUMER_KEY,CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

# COOKBOOK.PY
def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
    
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
    
        if wait_period > 3600: # Seconds
            print >> sys.stderr, 'Too many retries. Quitting.'
            raise e
    
        # See https://dev.twitter.com/docs/error-codes-responses for common codes
    
        if e.e.code == 401:
            print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
            return None
        elif e.e.code == 404:
            print >> sys.stderr, 'Encountered 404 Error (Not Found)'
            return None
        elif e.e.code == 429: 
            print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
            if sleep_when_rate_limited:
                print >> sys.stderr, "Retrying in 15 minutes...ZzZ..."
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print >> sys.stderr, '...ZzZ...Awake now and trying again.'
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print >> sys.stderr, 'Encountered %i Error. Retrying in %i seconds' %                 (e.e.code, wait_period)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function
    
    wait_period = 2 
    error_count = 0 

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError, e:
            error_count = 0 
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError, e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print >> sys.stderr, "URLError encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise
        except BadStatusLine, e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print >> sys.stderr, "BadStatusLine encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise

# COOKBOOK.PY
def get_user_profile(twitter_api, screen_names=None, user_ids=None):
   
    # Must have either screen_name or user_id (logical xor)
    assert (screen_names != None) != (user_ids != None),     "Must have screen_names or user_ids, but not both"
    
    items_to_info = {}

    items = screen_names or user_ids
    
    while len(items) > 0:

        # Process 100 items at a time per the API specifications for /users/lookup.
        # See https://dev.twitter.com/docs/api/1.1/get/users/lookup for details.
        
        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]

        if screen_names:
            response = make_twitter_request(twitter_api.users.lookup, 
                                            screen_name=items_str)
        else: # user_ids
            response = make_twitter_request(twitter_api.users.lookup, 
                                            user_id=items_str)
    
        for user_info in response:
            if screen_names:
                items_to_info[user_info['screen_name']] = user_info
            else: # user_ids
                items_to_info[user_info['id']] = user_info

    return items_to_info

# COOKBOOK.PY
from functools import partial
from sys import maxint

def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None,
                              friends_limit=maxint, followers_limit=maxint):
    
    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None),     "Must have screen_name or user_id, but not both"
    
    # See https://dev.twitter.com/docs/api/1.1/get/friends/ids and
    # https://dev.twitter.com/docs/api/1.1/get/followers/ids for details
    # on API parameters
    
    get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids, 
                              count=5000)
    get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids, 
                                count=5000)

    friends_ids, followers_ids = [], []
    
    for twitter_api_func, limit, ids, label in [
                    [get_friends_ids, friends_limit, friends_ids, "friends"], 
                    [get_followers_ids, followers_limit, followers_ids, "followers"]
                ]:
        
        if limit == 0: continue
        
        cursor = -1
        while cursor != 0:
        
            # Use make_twitter_request via the partially bound callable...
            if screen_name: 
                response = twitter_api_func(screen_name=screen_name, cursor=cursor)
            else: # user_id
                response = twitter_api_func(user_id=user_id, cursor=cursor)

            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']
        
            print >> sys.stderr, 'Fetched {0} total {1} ids for {2}'.format(len(ids), 
                                                    label, (user_id or screen_name))
        
            # XXX: You may want to store data during each iteration to provide an 
            # an additional layer of protection from exceptional circumstances
        
            if len(ids) >= limit or response is None:
                break

    # Do something useful with the IDs, like store them to disk...
    return friends_ids[:friends_limit], followers_ids[:followers_limit]


twitter_api = oauth_login()

############################################################################

## 1. Starting Point
screen_name = 'farheezyx3'

## 2. Retrieve friends; Max = 5000
response = make_twitter_request(twitter_api.friends.ids,
                                screen_name=screen_name, count = 5000)
friends = response["ids"]
response = make_twitter_request(twitter_api.followers.ids,
                                screen_name=screen_name, count = 5000)
followers = response["ids"]

## 3. reciprocal friends - distance-1 friends.

reciprocal_friends = set(friends).intersection(set(followers))
recip = list(reciprocal_friends)

## 4. select 5 most popular friends, followers_count; get_user_profile()
dict = {}

response = get_user_profile(twitter_api, user_ids=recip)
for id in response:
    for metadata in response[id]: #Go through every single meta data...
        if metadata == "followers_count": #...until you find 'followers_count'
            dict[id] = response[id][metadata] #key: user_id value: followers_count

sorted_dict = sorted(dict.items(),               #sorts amount of followers in descending order
                     key=operator.itemgetter(1), #but now it's a list
                     reverse=True)               #with tuples

popular_friends = []
for i in range(0,5):
    popular_friends.append(sorted_dict[i]) #Creates list of tuples. [(user_id, follower_count)]

follower_values = []
popular_ids = []
for i in range (0,5):
    follower_values.append(popular_friends[i][1])
    popular_ids.append(popular_friends[i][0])
print "Popular friends' user IDs: ", popular_ids #List of the popular friends' user ids
print "Popular friends' follower counts: ", follower_values #List of the popular friends' follower counts

## 5. Repeat 2, 3 & 4 for each of the distance-1 friends, distance-2 friends, etc, so on
##    until at least 100 users/nodes for your social network are gathered

usernames = []

response = get_user_profile(twitter_api, user_ids=popular_ids)
for j in response:
    for metadata in response[j]: #Go through every single meta data...
        if metadata == "screen_name": #...until you find 'screen_name'
            usernames.append(response[j][metadata])
print usernames

def simplified_crawler(twitter_api, screen_name, limit=1000000, depth=5):

    G = nx.Graph()
    seed_id = str(twitter_api.users.show(screen_name=screen_name)['id'])

    response = make_twitter_request(twitter_api.friends.ids, screen_name=screen_name, count = 5000)
    friends = response["ids"]
    response = make_twitter_request(twitter_api.followers.ids, screen_name=screen_name, count = 5000)
    followers = response["ids"]
  
    G.add_node(seed_id,followers=len(followers))

    reciprocal_friends = set(friends).intersection(set(followers))
    recip = list(reciprocal_friends)
    
    response = get_user_profile(twitter_api, user_ids=recip)
    for id in response:
        for metadata in response[id]: #Go through every single meta data...
            if metadata == "followers_count": #...until you find 'followers_count'
                dict[id] = response[id][metadata] #key: user_id value: followers_count

    sorted_dict = sorted(dict.items(),               #sorts amount of followers in descending order
                         key=operator.itemgetter(1), #but now it's a list
                         reverse=True)               #with tuples

    popular_friends = []
    for i in range(0,5):
        popular_friends.append(sorted_dict[i]) #Creates list of tuples. [(user_id, follower_count)]

    follower_values = []
    popular_ids = []
    for i in range (0,5):
        follower_values.append(popular_friends[i][1])
        popular_ids.append(popular_friends[i][0])
    print popular_ids
##    for id in popular_ids:
##        G.add_node(id,followers=popular_ids[id])
##        G.add_edge(seed_id,id)
##
##    d = 1
##    while d < depth:
##        d += 1
##        (queue, next_queue) = (next_recip, [])
##        for fid in queue:
##            friends_id, follower_ids = get_friends_followers_ids(twitter_api, user_id=fid, friends_limit=limit, followers_limit=limit)
##            
##            next_queue += follower_ids
    
# COOKBOOK.PY BUT MODIFIED
##def crawl_followers(twitter_api, screen_name, limit=1000000, depth=5):
##    
##    # Resolve the ID for screen_name and start working with IDs for consistency 
##    # in storage
##    seed_id = str(twitter_api.users.show(screen_name=screen_name)['id'])
##    
##    next_friend, next_follow = get_friends_followers_ids(twitter_api, user_id=seed_id, 
##                                                         friends_limit=limit, followers_limit=limit)
##
##    next_recip = list(set(next_follow).intersection(set(next_friend))) #all recip
##    response = get_user_profile(twitter_api, user_ids=next_recip)
##    for id in response:
##        for metadata in response[id]: #Go through every single meta data...
##            if metadata == "followers_count": #...until you find 'followers_count'
##                dict[id] = response[id][metadata] #key: user_id value: followers_count
##
##    sorted_dict = sorted(dict.items(),               #sorts amount of followers in descending order
##                         key=operator.itemgetter(1), #but now it's a list
##                         reverse=True)               #with tuples
##
##    popular_friends = []
##    for i in range(0,5):
##        popular_friends.append(sorted_dict[i]) #List of tuples. [(user_id, follower_count)]
##    
##    
##    d = 1
##    while d < depth:
##        d += 1
##        (queue, next_queue) = (next_recip, [])
##        for fid in queue:
##            friends_id, follower_ids = get_friends_followers_ids(twitter_api, user_id=fid, 
##                                                        friends_limit=limit, 
##                                                        followers_limit=limit)
##            
##            
##            next_queue += follower_ids

##    G.add_node(i,usernames[i])
##    G.add_edge(seed_id,i)
##    print "Nodes: ", G.nodes()
##    print "Edges: ", G.edges()    


    
## 6. Create social network using Networkx package
for i in range (0,30):
    simplified_crawler(twitter_api, usernames[i], depth=2, limit=10)

## 7. Calculate the diameter and average distance of your network
nodes = nx.number_of_nodes(G)
edges = nx.number_of_edges(G)
diameter = nx.diameter(G)
average_distance = nx.average_shortest_path_length(G)
print "Number of nodes: " + str(nodes)
print "Number of edges: " + str(edges)
print "Diameter: " + str(diameter)
print "Average Distance: " + str(average_distance)
