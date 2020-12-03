import tweepy
from telmtcp.module.telmtcp import constant as mcs
from telmtcp.module.telmtcp import common as mcm
from telmtcp.database.orm.models import *
from django.http import HttpResponse
from datetime import datetime, timedelta, date
from dateutil import relativedelta
import time
import collections


#get twitter api handler
def get_twitter_api():
    auth = tweepy.OAuthHandler(mcs.twitter_consumerKey, mcs.twitter_consumerSecret)
    api = tweepy.API(auth)
    return api

#get new followers timeline data for days for specific user
def get_twitter_nf_chart(request, days_offset = 7, user_id = None):
    try:
        if user_id == None:
            user = list(tweet_user.objects.all().values())
            user_id = user[0]['id']
        today = date.today()
        follow_graph_info = []
        for i in range(0, days_offset):
            new_params = {}
            x_date = today - timedelta(days=i)
            x_befor_date = today - timedelta(days=i+1)
            new_params['x_date'] = x_date.strftime("%Y-%m-%d")

            user_day_tw_info = list(tweet_user_analysis.objects.filter(created_date=x_date, userid=user_id).values())
            if user_day_tw_info == []:
                user_day_tw_info = {'followers_count': 0, 'favourites_count': 0}
            else:
                user_day_tw_info = user_day_tw_info[0]

            user_day_before_tw_info = list(tweet_user_analysis.objects.filter(created_date=x_befor_date, userid=user_id).values())
            if user_day_before_tw_info == []:
                user_day_before_tw_info = {'followers_count': 0, 'favourites_count': 0}
            else:
                user_day_before_tw_info = user_day_before_tw_info[0]

            new_params['new_followers_cn'] = user_day_tw_info['followers_count'] - user_day_before_tw_info['followers_count']
            if new_params['new_followers_cn'] < 0:
                new_params['new_followers_cn'] = 0
            follow_graph_info.append(new_params)
    except:
        follow_graph_info = []
    follow_graph_info.reverse()
    return follow_graph_info, user_id


#get the top liked tweets by specific hashtag for days
def get_twitter_tltweet_chart(request, days_offset=7, hashtag_name=None):
    try:
        if hashtag_name == None:
            hashtags = get_hashtag_arrya_in_db()
            hashtag_name = hashtags[0]

        today = date.today()
        last_day = today - timedelta(days=days_offset)
        last_day = datetime(last_day.year, last_day.month, last_day.day)
        last_day = last_day.strftime("%Y-%m-%d %H:%M:%S.000000")
        range_last = today + timedelta(days=1)
        range_last = datetime(range_last.year, range_last.month, range_last.day)
        range_last = range_last.strftime("%Y-%m-%d %H:%M:%S.000000")

        period_tweet_obj = tweet_user_timeline.objects.filter(tweet_created_date__range=(last_day, range_last)).exclude(hashtag_array='')
        tweets_res = list(period_tweet_obj.values())
        htag_anal = get_tweet_array_by_hashtag(tweets_res, hashtag_name)

        grouped = collections.defaultdict(list)
        for item in htag_anal:
            grouped[item['tweet_text']].append(item)
        new_htag_anal = []
        for model, group in grouped.items():
            new_htag_anal.append(group[0])

        toplikedtweets = sorted(new_htag_anal, key=lambda i: i['liked_count'], reverse=True)
        if len(toplikedtweets) > 5:
            toplikedtweets = toplikedtweets[:5]

        for tweet in toplikedtweets:
            tweet['tweet_text'] = tweet['tweet_text'].replace('\n', ' ')

    except:
        toplikedtweets = []
    return toplikedtweets, hashtag_name

#get the top trending hashtags for days,by tweet liked count
def get_twitter_tthashtag_chart(request, days_offset=7):
    try:
        hashtaginfo = get_twitter_hashtag_info(request, days_offset=days_offset)
        newhashtaginfo = []
        for item in hashtaginfo:
            if item['hashtag'] in mcs.remove_list:
                continue
            newhashtaginfo.append(item)
        toptrendinghashtags = sorted(newhashtaginfo, key=lambda i: i['likes_count'], reverse=True)
        if len(toptrendinghashtags) > 5:
            toptrendinghashtags = toptrendinghashtags[:5]
    except:
        toptrendinghashtags = []
    return toptrendinghashtags


#get the person with most likes everyday for period
def get_twitter_mlperson(request, days_offset=7):
    try:
        users = list(tweet_user.objects.all().values())
        today = date.today()
        likes_graph_info = []
        for i in range(0, days_offset):
            x_date = today - timedelta(days=i)

            tmp_array = []
            for user in users:
                userid = user['id']
                username = user['twitter_name']

                new_params = {}
                new_params['x_date'] = x_date.strftime("%Y-%m-%d")

                user_day_tw_info = list(tweet_user_analysis.objects.filter(created_date=x_date, userid=userid).values())
                if user_day_tw_info == []:
                    user_day_tw_info = {'followers_count': 0, 'favourites_count': 0}
                else:
                    user_day_tw_info = user_day_tw_info[0]

                new_params['new_favourites_count_cn'] = user_day_tw_info['favourites_count']
                new_params['twitter_name'] = username
                tmp_array.append(new_params)
            array = sorted(tmp_array, key=lambda i: i['new_favourites_count_cn'], reverse=True)
            likes_graph_info.append(array[0])
    except:
        likes_graph_info = []
    likes_graph_info.reverse()
    return likes_graph_info

#get data of every users follower counts and favourite count
def get_twitter_anlysis(request, days_offset = 7):
    try:
        users = list(tweet_user.objects.all().values())
        for user in users:
            today = date.today()
            last_day = today - timedelta(days=days_offset)

            user_tw_info = list(tweet_user_analysis.objects.filter(userid=user['id']).values())
            user_current_tw_info = user_tw_info[len(user_tw_info)-1]
            user_last_tw_info = list(tweet_user_analysis.objects.filter(created_date=last_day, userid=user['id']).values())
            if user_last_tw_info == []:
                user_last_tw_info = {'followers_count': 0, 'favourites_count': 0}
            else:
                user_last_tw_info = user_last_tw_info[0]

            user['followers_count'] = user_current_tw_info['followers_count'] - user_last_tw_info['followers_count']
            if user['followers_count'] < 0:
                user['followers_count'] = 0
            user['favourites_count'] = user_current_tw_info['favourites_count'] - user_last_tw_info['favourites_count']
            if user['favourites_count'] < 0:
                user['favourites_count'] = 0
        return users
    except:
        return []

#get data of every users tweet counts and favourite count
def get_twitter_act_info(request, days_offset = 7):
    try:
        users = list(tweet_user.objects.all().values())
        for user in users:
            today = date.today()
            last_day = today - timedelta(days=days_offset)

            user_tw_info = list(tweet_user_analysis.objects.filter(userid=user['id']).values())
            user_current_tw_info = user_tw_info[len(user_tw_info) - 1]
            user_last_tw_info = list(tweet_user_analysis.objects.filter(created_date=last_day, userid=user['id']).values())
            if user_last_tw_info == []:
                user_last_tw_info = {'favourites_count': 0, 'tweet_count': 0}
            else:
                user_last_tw_info = user_last_tw_info[0]

            user['favourites_count'] = user_current_tw_info['favourites_count'] - user_last_tw_info['favourites_count']
            if user['favourites_count'] < 0:
                user['favourites_count'] = 0
            user['tweet_count'] = user_current_tw_info['tweet_count'] - user_last_tw_info['tweet_count']
            if user['tweet_count'] < 0:
                user['tweet_count'] = 0
        return users
    except:
        return []


#get hashtag based tweets' count,retweet count ,favourie count data
def get_twitter_hashtag_info(request, days_offset = 7):
    try:
        today = date.today()
        last_day = today - timedelta(days=days_offset)
        last_day = datetime(last_day.year, last_day.month, last_day.day)
        last_day = last_day.strftime("%Y-%m-%d %H:%M:%S.000000")
        range_last = today + timedelta(days=1)
        range_last = datetime(range_last.year, range_last.month, range_last.day)
        range_last = range_last.strftime("%Y-%m-%d %H:%M:%S.000000")

        period_tweet_obj = tweet_user_timeline.objects.filter(tweet_created_date__range=(last_day, range_last)).exclude(hashtag_array='')
        tweets_res = list(period_tweet_obj.values())
        hashtags = get_hashtag_array_in_tweets(tweets_res)

        new_array = []
        for hashtag in hashtags:
            htag_anal = get_tweet_array_by_hashtag(tweets_res, hashtag)

            grouped = collections.defaultdict(list)
            for item in htag_anal:
                grouped[item['tweet_text']].append(item)
            new_htag_anal = []
            for model, group in grouped.items():
                new_htag_anal.append(group[0])

            tlike_cn = 0
            tretweet_cn = 0
            for item in new_htag_anal:
                tlike_cn += item['liked_count']
                tretweet_cn += item['retweet_count']
            new_params = {}
            new_params['hashtag'] = hashtag
            new_params['tweet_count'] = len(new_htag_anal)
            new_params['likes_count'] = tlike_cn
            new_params['retweet_count'] = tretweet_cn
            new_array.append(new_params)
        return new_array
    except:
        return []

#users likes count and follower count timeline for days
def get_twitter_lf_graph(request, days_offset = 7, user_A_id = None, user_B_id = None, y_axis = 'L'):
    if (user_A_id == None and user_B_id == None):
        user = list(tweet_user.objects.all().values())
        if len(user) == 0:
            return []
        user_A_id = user[0]['id']
        user_B_id = user[0]['id']

    today = date.today()
    graph_info = []
    for i in range(0, days_offset):
        new_params = {}

        x_date = today - timedelta(days=i)
        new_params['x_date'] = x_date.strftime("%Y-%m-%d")

        user_A_infos = list(tweet_user_analysis.objects.filter(created_date=x_date, userid=user_A_id).values())
        if len(user_A_infos) > 0:
            user_A_info = user_A_infos[len(user_A_infos) - 1]
            if y_axis == 'F':
                new_params['y_axis_A'] = user_A_info['followers_count']
            elif y_axis == 'L':
                new_params['y_axis_A'] = user_A_info['favourites_count']
        else:
            new_params['y_axis_A'] = 0

        user_B_infos = list(tweet_user_analysis.objects.filter(created_date=x_date, userid=user_B_id).values())
        if len(user_B_infos) > 0:
            user_B_info = user_B_infos[len(user_B_infos) - 1]
            if y_axis == 'F':
                new_params['y_axis_B'] = user_B_info['followers_count']
            elif y_axis == 'L':
                new_params['y_axis_B'] = user_B_info['favourites_count']
        else:
            new_params['y_axis_B'] = 0

        graph_info.append(new_params)
    return graph_info, days_offset, user_A_id, user_B_id, y_axis


#update database from twitter api daily
def update_twitter_analysis():
    api = get_twitter_api()
    tscreens = mcm.get_tweet_screen_names()

    for tscreen in tscreens:
        try:

            tscreen = tscreen.replace("\n", '')
            infoarray = tscreen.split(", ")
            tscreen_name = infoarray[0]
            tscreen_name = tscreen_name[1:]
            hashtag_array = infoarray[1:]
            hashtags = ", ".join(hashtag_array)
            print("=====> " + tscreen_name + " 's info updating...")
            time.sleep(mcs.basic_request_interval)
            user = api.get_user(screen_name=tscreen_name)

            defaults = {}
            defaults['hashtags'] = hashtags
            defaults['twitter_id'] = user.id_str
            defaults['twitter_name'] = user.name
            defaults['profile_image_url'] = user.profile_image_url_https

            tw, created = tweet_user.objects.update_or_create(
                twitter_screen_name=tscreen_name,
                defaults=defaults,
            )
            new_params = {}
            new_params['userid'] = tw.id
            new_params['followers_count'] = user.followers_count
            new_params['friends_count'] = user.friends_count
            new_params['tweet_count'] = user.statuses_count
            new_params['favourites_count'] = user.favourites_count
            tw_user_ans_obj = tweet_user_analysis(**new_params)
            tw_user_ans_obj.save()
            print("=====> " + tscreen_name + " 's info updated")
        except:
            pass

    users = list(tweet_user.objects.all().values())
    for user in users:
        print("=====> " + user['twitter_screen_name'] + " 's tweet timeline info updating...")
        screen_name = user['twitter_screen_name']
        user_id = user['id']
        try:
            if tweet_user_timeline.objects.filter(userid=user_id).count() == 0:
                time.sleep(mcs.usertimeline_request_interval)
                tweet_res = api.user_timeline(screen_name=screen_name, count=200)
                total_tweets = list(tweet_res)
            else:
                user_tweets = list(tweet_user_timeline.objects.filter(userid=user_id).values())
                user_tweets = sorted(user_tweets, key=lambda i: i['tweet_id'], reverse=True)
                last_tweet_id = user_tweets[0]['tweet_id']

                cursor = -1
                total_tweets = []
                cn = 0
                while cursor != None:
                    time.sleep(mcs.usertimeline_request_interval)
                    cn += 1
                    if cursor == -1:
                        tweet_res = api.user_timeline(screen_name=screen_name, count=200, since_id=last_tweet_id)
                    else:
                        tweet_res = api.user_timeline(screen_name=screen_name, count=200, max_id=cursor, since_id=last_tweet_id)
                    total_tweets += list(tweet_res)
                    cursor = tweet_res.max_id
                    if cn >= 10:
                        break

            total_tweets.reverse()
            for i in range(0, len(total_tweets)):
                new_param = {}
                new_param['userid'] = user_id
                new_param['tweet_id'] = total_tweets[i].id
                new_param['tweet_text'] = total_tweets[i].text
                new_param['liked_count'] = total_tweets[i].favorite_count
                new_param['retweet_count'] = total_tweets[i].retweet_count
                new_param['tweet_created_date'] = total_tweets[i].created_at
                new_param['hashtag_array'] = get_hashtag_array(total_tweets[i].entities['hashtags'])
                tweet_user_timeline_obj = tweet_user_timeline(**new_param)
                tweet_user_timeline_obj.save()
            print("=====> " + user['twitter_screen_name'] + " 's tweet timeline info updated")
        except:
            pass


    return 0

#convert hashtag_array in tweet object of API respone to str
# ['FL21', 'FL20'] -> 'FL21|FL20'
def get_hashtag_array(hashtags):
    try:
        hashtag_array = []
        for tag in hashtags:
            hashtag_array.append(tag['text'])
        hashtag_array_str = "|".join(hashtag_array)
        return hashtag_array_str
    except:
        return ''


#get total hashtagarray in tweets saved in database
def get_hashtag_arrya_in_db():
    tweetres = list(tweet_user_timeline.objects.all().exclude(hashtag_array='').values())
    res = get_hashtag_array_in_tweets(tweetres)
    return res

#get non repeated hashtag array from tweets
def get_hashtag_array_in_tweets(tweets):
    try:
        hashtag_array = []
        for tweet in tweets:
            array = tweet['hashtag_array'].split('|')
            hashtag_array += array

        grouped = collections.defaultdict(list)
        for item in hashtag_array:
            grouped[item].append(item)

        new_hashtag_array = []
        for model, group in grouped.items():
            new_hashtag_array.append(group[0])

        return new_hashtag_array
    except:
        return []

#get tweet array including specific hashtag from tweet array of database
def get_tweet_array_by_hashtag(tweets_res, hashtag):
    try:
        tweet_array = []
        for tweet in tweets_res:
            array = tweet['hashtag_array'].split('|')
            if hashtag in array:
                tweet_array.append(tweet)

        return tweet_array
    except:
        return []