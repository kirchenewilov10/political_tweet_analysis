import sys
from sty import fg, bg, ef, rs
from telmtcp.module.telmtcp import constant as mcs
from telmtcp.database.orm.models import *
from telmtcp.module.glb.ret_code import *
from django.contrib.auth import authenticate
import threading
import smtplib


#print error line and message on console
def print_exception():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    error_msg = bg.red
    error_msg += str(exc_obj) + ", File: " + str(exc_tb.tb_frame.f_code.co_filename) + ", Line: " + str(exc_tb.tb_lineno)
    error_msg += bg.rs
    print(error_msg)

#encrypt text putting in session
def encrypt(text):
    return text

#decrypt text reading from session
def decrypt(text):
    return text

#get business mail account
def get_mail_account(request):
    mail_account = {}
    mail_account["email"] = ""
    mail_account["password"] = ""
    return mail_account

#handle mail thread to send message customers
def send_email(request, msg):
    th = threading.Thread(target=send_email_thread, args=(request, msg))
    th.start()

#send mail programmatically from business account to customers
def send_email_thread(request, msg):
    mail_account = get_mail_account(request)

    try:
        # for gmail
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.ehlo()
        s.starttls()

        # for godaddy mail
        # s = smtplib.SMTP_SSL(host='smtpout.secureserver.net', port=465)
        # s.ehlo()

        #s = smtplib.SMTP(host='smtp.office365.com', port=587)
        #s.ehlo()
        #s.starttls()

        s.login(mail_account["email"], mail_account["password"])
        s.send_message(msg)

    except Exception as e:
        print(e)
        return -1

    return 0

#check whether keys are exist or not in dictionary object
def check_keys(key_ary, dict_obj):
    for key in key_ary:
        if key not in dict_obj:
            return False
    return True

#handle login action by posted username and password
def authenticate_user(username, password):
    try:
        user_obj_list = list(tbl_user.objects.filter(username=username))
        if len(user_obj_list) == 0:
            return AUTH_ACCOUNT_NOT_FOUND, None
        user_obj = user_obj_list[0]
        if user_obj.is_active == 0:
            return AUTH_ACCOUNT_DISABLED, None

        user = authenticate(username=username, password=password)
        if user == None:
            return AUTH_WRONG_PWD, None

        return AUTH_SUCCESS, user

    except Exception as e:
        return AUTH_UNKOWN_ERROR, None

#get menu data for left side bar
def get_user_menu_data():
    user_menu_data = [
        {
            'id': 1,
            'url': 'dashboard1',
            'name': 'Dashboard1',
            'icon': 'fa fa-dashboard',
            'parent': 0,
            'has_child': 0
        },
        {
            'id': 2,
            'url': 'dashboard2',
            'name': 'Dashboard2',
            'icon': 'fa fa-dashboard',
            'parent': 0,
            'has_child': 0
        }
    ]
    return user_menu_data

#parse group file and get all of people's screen name and labels as array
def get_tweet_screen_names():
    file = open("static/library/txt/group", "r", encoding='utf-8')
    text = file.readlines()
    tscreens = []
    for tscreen in text:
        tscreens.append(tscreen)
    file.close()
    return tscreens


#reference authenticated user's infomation
def get_user_data(request):
    return request.user
    username = decrypt(request.session[encrypt("username")])
    try:
        user_obj = list(tbl_user.objects.filter(username=username).values())[0]
    except:
        user_obj = {}
    return user_obj
