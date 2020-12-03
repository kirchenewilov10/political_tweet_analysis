from django.shortcuts import render, redirect

from django.http import HttpResponse

from telmtcp.module.telmtcp import common as mcm
from telmtcp.module.telmtcp import constant as mcs
from telmtcp.module.telmtcp import email as mce
from telmtcp.module.telmtcp import twitter as mtw
from telmtcp.module.glb.ret_code import *
from telmtcp.database.orm.models import *
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telmtcp.module.telmtcp import twitter as mtw

import json
import random
import time
# Create your views here.

#view landing page
def welcome(request):
	return render(request, 'welcome/index.html')

#view login page or sign up a customer
def register(request, template_name='welcome/sign-up.html'):
	try:
		params = request.POST
		key_ary = ['username', 'password', 'first_name', 'last_name', 'phone', 'email']
		if mcm.check_keys(key_ary, params) == False:
			return render(request, template_name)
		new_params = {}
		new_params['first_name'] = params['first_name']
		new_params['last_name'] = params['last_name']
		new_params['email'] = params['email']
		new_params['phone'] = params['phone']
		new_params['username'] = params['username']
		new_params['s_password'] = params['password']

		if tbl_user.objects.filter(username=new_params['username']).count() > 0:
			data = {'alert_str': 'Username exists'}
			return render(request, template_name, data)
		if tbl_user.objects.filter(email=new_params['email']).count() > 0:
			data = {'alert_str': 'Email exists'}
			return render(request, template_name, data)
		user_obj = tbl_user(**new_params)
		user_obj.set_password(params['password'])
		user_obj.save()
		return redirect('/login')
	except:
		mcm.print_exception()
		alert_str = AUTH_ALERT_STRING[AUTH_UNKOWN_ERROR]
		data = {'alert_str': alert_str}
		return render(request, template_name, data)

#login a customer by username and password
def login(request, template_name='welcome/login.html'):
	try:
		time.sleep(1)
		key_ary = ['username', 'password']
		if mcm.check_keys(key_ary, request.POST) == False:
			return render(request, template_name)

		if request.user.is_authenticated:
			return redirect('/dashboard1')

		username = request.POST['username']
		password = request.POST['password']
		ret_code, user_obj = mcm.authenticate_user(username, password)

		if ret_code != AUTH_SUCCESS:
			alert_str = AUTH_ALERT_STRING[ret_code]
			data = {
				'alert_str': alert_str
			}
			return render(request, template_name, data)

		django_login(request, user_obj)

		request.session['username'] = username
		request.session.save()
		return redirect('/dashboard1')

	except Exception as e:
		return render(request, template_name)

#logout a user
def logout(request):
	django_logout(request)
	request.session.clear()
	return redirect('/login')

#view help page
def about(request):
	return render(request, 'welcome/about.html')

@login_required
#view dashboard1 menu
def dashboard1(request):
	users = list(tweet_user.objects.all().values())
	twitter_analysis = mtw.get_twitter_anlysis(request)
	twitter_act_info = mtw.get_twitter_act_info(request)
	twitter_lf_graph_info, days_offset, user_A_id, user_B_id, y_axis = mtw.get_twitter_lf_graph(request)
	twitter_hashtag_info = mtw.get_twitter_hashtag_info(request)
	twitter_lf_graph_info.reverse()
	data = {
		"menu_data": mcm.get_user_menu_data(),
		"menu_id": 1,
		"page_title": "Dashboard1",
		"twitter_analysis": twitter_analysis,
		"twitter_act_info": twitter_act_info,
		"twitter_lf_graph_info": twitter_lf_graph_info,
		"twitter_hashtag_info": twitter_hashtag_info,
		"days_offset": days_offset,
		"user_B_id": user_B_id,
		"user_A_id": user_A_id,
		"y_axis": y_axis,
		"users": users,
		"basedata": mcm.get_user_data(request)
	}
	return render(request, 'user/dashboard1.html', data)

#view dashboard2 menu
@login_required()
def dashboard2(request):
	users = list(tweet_user.objects.all().values())
	twitter_new_followers, userid = mtw.get_twitter_nf_chart(request)
	twitter_topliked_tweets, hashtag_id = mtw.get_twitter_tltweet_chart(request)
	mlperson = mtw.get_twitter_mlperson(request)
	hashtags = mtw.get_hashtag_arrya_in_db()
	data = {
		"menu_data": mcm.get_user_menu_data(),
		"menu_id": 2,
		"page_title": "Dashboard2",
		"twitter_new_followers": twitter_new_followers,
		"userid": userid,
		"twitter_topliked_tweets": twitter_topliked_tweets,
		"hashtag_id": hashtag_id,
		"twitter_tthashtag_chart": mtw.get_twitter_tthashtag_chart(request),
		"twitter_mlperson": mlperson,
		"users": users,
		"hashtags": hashtags,
		"basedata": mcm.get_user_data(request)
	}
	return render(request, 'user/dashboard2.html', data)

#filter action by period on table that is showing users having most new likes and followers
@login_required()
def lf_filter(request):
	param = request.POST
	lf_days_offset = int(param['lf_days_offset'])
	twitter_analysis = mtw.get_twitter_anlysis(request, days_offset=lf_days_offset)
	return HttpResponse(json.dumps(twitter_analysis))

#filter action by period on table that is showing most active users
@login_required()
def lf_ac_filter(request):
	param = request.POST
	ac_days_offset = int(param['ac_days_offset'])
	twitter_ac_analysis = mtw.get_twitter_act_info(request, days_offset=ac_days_offset)
	return HttpResponse(json.dumps(twitter_ac_analysis))

#filter action by period on table that is showing most active users
@login_required()
def lf_ht_filter(request):
	param = request.POST
	ht_days_offset = int(param['ht_days_offset'])
	twitter_ht_analysis = mtw.get_twitter_hashtag_info(request, days_offset=ht_days_offset)
	return HttpResponse(json.dumps(twitter_ht_analysis))

#filter action by period, persion on chart that is showing likes and followers timeline
@login_required()
def lfchart_filter(request):
	param = request.POST
	lfchart_days_offset = int(param['lfchart_days_offset'])
	user_A_id = int(param['user_A_id'])
	user_B_id = int(param['user_B_id'])
	chart_f_or_l = param['chart_f_or_l']
	res, days_offset, user_A_id, user_B_id, y_axis = mtw.get_twitter_lf_graph(request, lfchart_days_offset, user_A_id, user_B_id, chart_f_or_l)
	return HttpResponse(json.dumps(res))

#filter action by period on chart that is showing person with the most likes everyday
@login_required()
def ml_filter(request):
	param = request.POST
	ml_days_offset = int(param['ml_days_offset'])
	res = mtw.get_twitter_mlperson(request, ml_days_offset)
	return HttpResponse(json.dumps(res))

#filter action by period,hashtag on bar that is showing Top 5 most likes
@login_required()
def tt_filter(request):
	param = request.POST
	tt_days_offset = int(param['tt_days_offset'])
	tt_hashtag_id = param['tt_hashtag_id']
	res, hashtagid = mtw.get_twitter_tltweet_chart(request, tt_days_offset, tt_hashtag_id)
	for item in res:
		del item['tweet_created_date']
	return HttpResponse(json.dumps(res))

#filter action by period on bar that is showing Trending Hashtag
@login_required()
def th_filter(request):
	param = request.POST
	th_days_offset = int(param['th_days_offset'])
	res = mtw.get_twitter_tthashtag_chart(request, th_days_offset)
	return HttpResponse(json.dumps(res))

#filter action by period, person on chart that is new followers timeline
@login_required()
def nf_filter(request):
	param = request.POST
	nf_days_offset = int(param['nf_days_offset'])
	nf_userid = int(param['nf_userid'])
	res, userid = mtw.get_twitter_nf_chart(request, nf_days_offset, nf_userid)
	return HttpResponse(json.dumps(res))


#run background function to update database by twitter api using manual http request
def test_update_twitter_analysis(request):
	mtw.update_twitter_analysis()
	return HttpResponse('ok')