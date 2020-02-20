from pyswip import Prolog
import json
prolog = Prolog()

patient = {"duration":40,               #头痛发作持续时间
           "times":10,                  #头疼次数
           "one_side":1,                #单侧，1表示有相关病情，0表示没有，下同
           "moderate_to_severe":1,      #中重度
           "pulsatility": 1,            #搏动性
           "activity": 1,               #日常体力活动加重
           "avoid_activities": 1,       #因头痛避免日常体力活动
           "nausea": 1,                 #恶心
           "vomiting": 1,               #呕吐
           "afraid_light": 1,           #畏光
           "afraid_sound": 1,           #畏声
           "e":1                        #不能用 ICHD-3 中其他诊断更好地解释
           }

with open("patient.json","w") as f:
    json.dump(patient,f)

#KB
prolog.assertz("headache(X):-a(X),e(X)")
prolog.assertz("a(X):-b(X),c(X),d(X),times(X,Y),Y > 5")
#标准B:持续时长4~72小时
prolog.assertz("b(X):-duration(X,Y),Y>4,Y<72")
#标准C:以下标准符合两个
# 单侧、搏动性、中重度、日常体力、活动加重头痛或因头痛而避免日常活动
prolog.assertz("c(X):-one_side(X),pulsatility(X)")
prolog.assertz("c(X):-one_side(X),moderate_to_severe(X)")
prolog.assertz("c(X):-one_side(X),activity_avoid_activities(X)")
prolog.assertz("c(X):-pulsatility(X),moderate_to_severe(X)")
prolog.assertz("c(X):-pulsatility(X),activity_avoid_activities(X)")
prolog.assertz("c(X):-moderate_to_severe(X),activity_avoid_activities(X)")
#活动加重头痛或因头痛而避免日常活动 分为 活动加重头痛   或   因头痛避免日常活动
prolog.assertz("activity_avoid_activities(X):-activity(X);avoid_activities(X)")
#标准D:以下标准符合一个
# 恶心和呕吐
# 畏光和畏声
prolog.assertz("d(X):-nausea_and_vomiting(X);afraid_light_and_sound(X)")
prolog.assertz("nausea_and_vomiting(X):-nausea(X),vomiting(X)")
prolog.assertz("afraid_light_and_sound(X):-afraid_light(X),afraid_sound(X)")


with open("patient.json") as f1:
    a = json.load(f1)
    print(a)
for key in a:
    if key == "duration" or key =="times":
        tmp_str = key + "(laowang," + str(a[key]) + ")"
    else:
        if a[key] == 1:
            tmp_str = key + "(laowang)"
        else:
            tmp_str = key + "(null)"
    print(tmp_str)
    prolog.assertz(tmp_str)
print('*'*80)
print(bool(list(prolog.query("headache(laowang)"))))

