from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),

    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),

    path('dashboard1', views.dashboard1, name='dashboard1'),
    path('dashboard2', views.dashboard2, name='dashboard2'),
    path('update_twitter_analysis', views.test_update_twitter_analysis, name='update_twitter_analysis'),

    path('lf_filter', views.lf_filter, name='lf_filter'),
    path('lf_ac_filter', views.lf_ac_filter, name='lf_ac_filter'),
    path('lf_ht_filter', views.lf_ht_filter, name='lf_ht_filter'),
    path('lfchart_filter', views.lfchart_filter, name='lfchart_filter'),

    path('nf_filter', views.nf_filter, name='nf_filter'),
    path('tt_filter', views.tt_filter, name='tt_filter'),
    path('th_filter', views.th_filter, name='th_filter'),
    path('ml_filter', views.ml_filter, name='ml_filter'),

]