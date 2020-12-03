from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
class tbl_user(AbstractUser):
    uid = models.BigIntegerField(default=0)
    s_password = models.CharField(default='', max_length=512)
    phone = models.CharField(max_length=255, blank=True)

class tweet_user(models.Model):
    twitter_screen_name = models.CharField(max_length=255, blank=True)
    hashtags = models.CharField(max_length=255, blank=True)
    twitter_id = models.CharField(max_length=255, blank=True)
    twitter_name = models.CharField(max_length=255, blank=True)
    profile_image_url = models.CharField(max_length=255, blank=True)

class tweet_user_analysis(models.Model):
    userid = models.IntegerField(blank=True, default=0)
    followers_count = models.BigIntegerField(blank=True, default=0)
    friends_count = models.BigIntegerField(blank=True, default=0)
    tweet_count = models.BigIntegerField(blank=True, default=0)
    favourites_count = models.BigIntegerField(blank=True, default=0)
    created_date = models.DateField(blank=True, auto_now_add=True)
    
class tweet_hashtag_analysis(models.Model):
    hashtag = models.CharField(max_length=255, blank=True)
    tweet_id = models.BigIntegerField(blank=True, default=0)
    tweet_text = models.TextField(blank=True)
    liked_count = models.BigIntegerField(blank=True, default=0)
    retweet_count = models.BigIntegerField(blank=True, default=0)
    hashtag_has = models.IntegerField(blank=True, default=0)
    created_date = models.DateField(blank=True, auto_now_add=True)
    tweet_created_date = models.DateTimeField(blank=True, auto_now_add=True)

class tweet_hashtag(models.Model):
    hashtag = models.CharField(max_length=255, blank=True)

class tweet_user_timeline(models.Model):
    userid = models.IntegerField(blank=True, default=0)
    tweet_id = models.BigIntegerField(blank=True, default=0)
    tweet_text = models.TextField(blank=True)
    liked_count = models.BigIntegerField(blank=True, default=0)
    retweet_count = models.BigIntegerField(blank=True, default=0)
    tweet_created_date = models.DateTimeField(blank=True, auto_now_add=True)
    hashtag_array = models.TextField(blank=True)