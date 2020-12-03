from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import tbl_user, tweet_user, tweet_hashtag_analysis, tweet_user_timeline, tweet_hashtag, tweet_user_analysis

class tweet_userAdmin(admin.ModelAdmin):
    list_display = [field.name for field in tweet_user._meta.get_fields()]
admin.site.register(tweet_user, tweet_userAdmin)

admin.site.register(tbl_user, UserAdmin)

class tweet_user_analysisAdmin(admin.ModelAdmin):
    list_display = [field.name for field in tweet_user_analysis._meta.get_fields()]
admin.site.register(tweet_user_analysis, tweet_user_analysisAdmin)

class tweet_hashtagAdmin(admin.ModelAdmin):
    list_display = [field.name for field in tweet_hashtag._meta.get_fields()]
admin.site.register(tweet_hashtag, tweet_hashtagAdmin)

class tweet_hashtag_analysisAdmin(admin.ModelAdmin):
    list_display = [field.name for field in tweet_hashtag_analysis._meta.get_fields()]
admin.site.register(tweet_hashtag_analysis, tweet_hashtag_analysisAdmin)

class tweet_user_timelineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in tweet_user_timeline._meta.get_fields()]
admin.site.register(tweet_user_timeline, tweet_user_timelineAdmin)