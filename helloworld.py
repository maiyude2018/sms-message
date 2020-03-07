import streamlit as st
import numpy as np
import pandas as pd
from Requests import Requests
import time
from api import Api
import json
import pickle
import datetime as dt
from datetime import timezone
import random
import math
import copy
import datetime

st.title("steemmonsters信息显示器")



api = Api()
battle_log=""
quest_details = dict()
for x in api.settings()["quests"]:
    quest_details[x["name"]] = x


name = st.text_input('请输入账号',"player")

print("___________________________________________")
print("账户:",name)

@st.cache
def ms1(name):
    battle_log = ""
    battle_log += "账户：" +name + "\n"

    try:
        rc = api.get_player_vp(name)
        battle_log +=  "\n"+"RC："+ str(rc)+ "\n"
        #print("RC：",rc)
    except:
        pass
    return battle_log

def ms2(name):
    battle_log=""
    jiangli = 0
    gold = 0
    gold2 = 0
    gold1 = 0
    dina = 0

    battle_log += "\n"+"赛季信息:" + "\n"

    season=api.get_player_details(name)
    max_rating=season["season_details"]["max_rating"]
    rating = season["season_details"]["rating"]
    ras=api.rating(max_rating)
    battle_log +=  "\n"+"赛季最高成绩：" +str(max_rating)+ "\n"
    battle_log += "\n"+"赛季奖励卡片数量:" + str(ras) + "\n"
    jiangli += ras[1]
    if "黄金" in ras[0]:
        gold+=1
    if "黄金2" in ras[0]:
        gold2+=1
    if "黄金1" in ras[0]:
        gold1+=1
    if "钻石" in ras[0]:
        dina += 1

    print()

    #login=api.get_player_login(name[number])
    max_rating = season["max_rating"]
    rating = season["rating"]
    battles=season["battles"]
    wins=season["wins"]
    longest_streak=season["longest_streak"]
    battle_log += "\n" + "等级:" + str(rating) + "/"+str(max_rating)+"\n"
    battle_log += "\n" + "比赛次数:" + str(wins) + "/" + str(battles) + "\n"

    rate='%.2f%%' % ((wins/battles) * 100)

    battle_log += "\n" + "胜率:" + str(rate)  + "\n"+ "\n"
    return battle_log

def ms3(name):
    decc = 0
    LEGENDARY = GOLD = QUEST = ORB = 0
    battle_log=""
    battle_log += "\n"
    battle_log += "\n" + "账户信息:" +"\n"


    balances=api.get_player_balances(name)

    for i in balances:
        token=i["token"]
        balance=i["balance"]
        if token == "ECR":
            balance=balance/100

        battle_log += "\n" + str(token) + ":"+str(balance)+"\n"
        if token == "DEC":
            decc += balance
        if token == "GOLD":
            GOLD += balance
        if token == "LEGENDARY":
            LEGENDARY += balance
        if token == "QUEST":
            QUEST += balance
        if token == "ORB":
            ORB += balance
    return battle_log

def ms4(name):
    battle_log = ""
    quest=api.get_quests(name)
    quest=quest[0]
    completed_items = quest['completed_items']
    total_items = quest['total_items']

    created_date = quest['created_date'].replace('Z', '')
    created_date = dt.datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S.%f")
    reset_time = created_date + dt.timedelta(hours=31)
    quest_name = quest["name"]
    try:
        quest_color = quest_details[quest["name"]]["data"]["color"]
    except Exception as e:
        quest_color=None
        print(e)


    battle_log += "\n"+  "" + "\n"
    battle_log += "\n"+"\n" + "任务信息:" + "\n"

    nowtime = dt.datetime.now()
    if completed_items == total_items:
        battle_log += "\n" + "下次任务开始还有:" +str(reset_time - nowtime)+ "\n"

    else:
        battle_log += "\n"+  "" + "\n"
        battle_log += "\n" + "任务进行中:" + "\n"
        battle_log += "\n" + "任务完成情况:" + str(completed_items)+ "/"+str(total_items)+"\n"


    battle_log += "\n" + str(quest_name)+"  " + str(quest_color)+"\n"
    battle_log += "\n" + "下次任务时间:" +str(reset_time)+ "\n"
    battle_log += "\n" + "___________________________________________ " +"\n"

    battle_log += "\n"+  "" + "\n"

    return battle_log

if name != "player":
    a = ms1(name)
    a
    st.header('__________________________')
    b = ms2(name)
    b
    st.header('__________________________')
    c = ms3(name)
    c
    st.header('__________________________')
    d = ms4(name)
    d