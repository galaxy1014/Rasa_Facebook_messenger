from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from databases import Database
# from . import Sound, Picture, Quote
import random
import numpy as np
from paraphrase_googletranslate import Paraphraser
from datetime import datetime
import time
import firebase_admin
from firebase_admin import credentials
from playsound import playsound
from urllib.request import urlopen
from PIL import Image
from rasa_sdk.events import UserUtteranceReverted
# cred = credentials.Certificate('actions/Mykey.json')
# default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://imagesoundquote.firebaseio.com/'})
# class ActionAskUserInfo(Action):
#     def name(self) -> Text:
#         return "action_ask_user_info"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         user_name = tracker.get_slot('user_name')
#         user_age = tracker.get_slot('user_age')
#         user_gender = tracker.get_slot('user_gender')
#         user_occupation = tracker.get_slot('user_occupation')
#         user_hobby = tracker.get_slot('user_hobby')
#         a = tracker.latest_message.get('text')  ## User input 불러오기
#         if (user_name == "User"):  # username 이 기본일 때, 사용자의 이름부터 물어본다.
#             rand = random.randint(0, 4)
#             list = ['''Hello. What is your name?''',
#                     '''Hello, What should I call you?''',
#                     '''I don't know your name Can you tell me your name?''',
#                     '''Hi, Do you want me to just call you {}? If not, tell me your name.'''.format(user_name),
#                     """Hello, What do you want me to call you?"""
#                     ]
#             b = list[rand]
#             dispatcher.utter_message((" " + b))
#         else:  # username을 설정했을 때, Slot값이 채워지지 않은 다른 정보를 물어본다.
#             if user_gender == None:
#                 rand = random.randint(0, 4)
#                 list = ['''Are you a man or a woman?''',
#                         '''Can you tell me your gender?''',
#                         '''I don't know if you are male or female. Can you tell me?''',
#                         '''If you tell me your gender, I think I can have a closer conversation with you.''',
#                         """Are you a woman? Or is it male?"""
#                         ]
#                 b = list[rand]
#                 dispatcher.utter_message((" " + b))
#             elif user_age == None:
#                 rand = random.randint(0, 4)
#                 list = ['''I don't know your age. How old are you?''',
#                         '''{}, Can you tell me your age?'''.format(user_name),
#                         '''I do not know how old you are. Can you tell me?''',
#                         '''I want to know more about you How old are you?''',
#                         '''Can you tell me your age? I always want to know more about you.'''
#                         ]
#                 b = list[rand]
#                 dispatcher.utter_message((" " + b))
#             elif user_occupation == None:
#                 rand = random.randint(0, 4)
#                 list = ['''What do you do for a living?''',
#                         '''What kind of work do you do?''',
#                         '''I don't know about your occupation. Can you tell me?''',
#                         '''If you tell me your occupation, I think I can have a closer conversation with you.''',
#                         '''Can you tell me your occupation? I always want to know more about you.'''
#                         ]
#                 b = list[rand]
#                 dispatcher.utter_message((" " + b))
#             elif user_hobby == None:
#                 rand = random.randint(0, 4)
#                 list = ['''What are you interested in?''',
#                         '''What do you enjoy doing?''',
#                         '''I don't know your hobby. What is your favorite hobby?''',
#                         '''If you tell me your hobby, I think I can have a closer conversation with you.''',
#                         '''What do you do for fun?'''
#                         ]
#                 b = list[rand]
#                 dispatcher.utter_message((" " + b))
#             else:  # 4가지 모든 정보를 다 가지고 있을 때, 많이 가까워졌다는/더 많은 대화를 나누자는 친근함 표현
#                 rand = random.randint(0, 4)
#                 list = ['''{}, I knew a lot about you. I think we're very close.'''.format(user_name),
#                         '''Now I know a lot about you.''',
#                         '''I knew a little about you, but we'll be closer when we talk a lot more.''',
#                         '''If you tell me your gender, I think I can have a closer conversation with you.''',
#                         '''I'm glad I'm close to you. Let's be closer together.'''
#                         ]
#                 b = list[rand]
#                 dispatcher.utter_message((" " + b))
##################################################################################
## chae 2 : action_tell_bot_info // bot정보를 제공하는 것
## 사용하는 슬롯 : user_name, user_age, user_gender, user_hobby,  user_occupation + 올해년도
##################################################################################
class ActionTellBotInfo(Action):
    def name(self) -> Text:
        return "action_tell_bot_info"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 봇의 정보를 정의 / 순서 : 이름, 생년, 성별, 직업, 취미
        bot_info = ['emobot', 2020, 'male', 'chatbot', 'watching netflix']
        user_name = tracker.get_slot('user_name')
        user_age = tracker.get_slot('user_age')
        user_gender = tracker.get_slot('user_gender')
        user_hobby = tracker.get_slot('user_hobby')
        user_occupation = tracker.get_slot('user_occupation')
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if ("name" in a):
            rand_info = 0
        elif ("ages" in a) or ("age" in a) or ("old" in a) or ("born" in a) or ("birth" in a):
            rand_info = 1
        elif ("gender" in a) or ("sex" in a) or ("man" in a) or ("woman" in a) or ("male" in a) or ("female" in a) or ("boy" in a) or ("girl" in a):
            rand_info = 2
        elif ("job" in a) or ("occupation" in a) or ("work" in a) or ("do you do" in a) or ("what you're doing" in a):
            rand_info = 3
        elif ("hobby" in a) or ("you like" in a) or ("interest" in a) or ("for fun" in a) or ("are you into" in a):
            rand_info = 4
        # rand_info = random.randint(0, 4)
        if rand_info == 0:  # bot의 이름 말하기
            rand = random.randint(0, 4)
            list = ['''Oh, My name is {}'''.format(bot_info[rand_info]),
                    '''Just call me {}'''.format(bot_info[rand_info]),
                    '''Just call me {}, please'''.format(bot_info[rand_info]),
                    '''Please call me {}.'''.format(bot_info[rand_info]),
                    '''My name is {}.'''.format(bot_info[rand_info])
                    ]
            b = list[rand]
            dispatcher.utter_message((" " + b))
        elif rand_info == 1:  # bot의 생년 말하기
            years_old = datetime.now().year - bot_info[rand_info] + 1  # 나이 계산
            rand = random.randint(0, 4)
            user_call = user_name
            if user_age != None:
                if user_age > years_old:
                    if user_gender != None:  # 사용자의 나이가 더 많지만, 성별을 아는 경우
                        if user_gender == 'female':
                            user_call = 'sister'
                        elif user_gender == 'male':
                            user_call = 'brother'
                        list = ['''I am {} years old. I can call you '''.format(years_old) + user_call,
                                '''I was born in {}.'''.format(bot_info[rand_info]),
                                '''I was born in {}.'''.format(
                                    bot_info[rand_info]) + user_call + ''', You are older than me.'''.format(years_old),
                                '''I am {} years old.'''.format(years_old) + '''Because I was born in {}.'''.format(
                                    bot_info[rand_info]),
                                '''I am {} years old.'''.format(years_old)
                                ]
                        b = list[rand]
                        dispatcher.utter_message((" " + b))
                    else:  # 사용자의 나이가 더 많지만, 성별을 모르는 경우
                        list = ['''I am {} years old. Compared to you, I'm just a kid.'''.format(years_old),
                                '''I was born in {}.'''.format(bot_info[rand_info]),
                                '''I was born in {}.'''.format(bot_info[rand_info]),
                                '''Because I was born in {}.'''.format(bot_info[rand_info]),
                                '''I am {} years old.'''.format(years_old)
                                ]
                        b = list[rand]
                        dispatcher.utter_message((" " + b))
                elif user_age == years_old:  # user와 동갑인 경우
                    user_call = 'friend'
                    list = ['''I am {} years old too!'''.format(years_old),
                            '''I was born in {}. So we are friend!'''.format(bot_info[rand_info]),
                            '''I was born in {}.'''.format(bot_info[rand_info]),
                            '''I am {} years old.'''.format(years_old),
                            '''I was born in same year.'''
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                elif user_age < years_old:  # user가 더 어린 경우
                    if user_gender != None:  # 사용자의 나이가 어리지만, 성별을 아는 경우
                        if user_gender == 'female':
                            user_call = 'sister'
                        elif user_gender == 'male':
                            user_call = 'brother'
                        list = ['''I am {} years old. You are younger than me,'''.format(years_old),
                                '''I was born in {}. So you are younger than me!'''.format(bot_info[rand_info]),
                                '''I was born in {}.'''.format(bot_info[rand_info]),
                                '''I am {} years old.'''.format(years_old),
                                '''I am {} years old.'''.format(years_old)
                                ]
                        b = list[rand]
                        dispatcher.utter_message((" " + b))
                    else:  # 사용자의 나이가 더 어리지만, 성별을 모르는 경우
                        list = ['''I am {} years old. Compared to me, You're just a kid.'''.format(years_old),
                                '''I was born in {}.'''.format(bot_info[rand_info]),
                                '''I was born in {}.'''.format(bot_info[rand_info]) + '''You are older than me.'''
                                                                                      '''I am {} years old.'''.format(
                                    years_old),
                                '''I am {} years old.'''.format(years_old)
                                ]
                        b = list[rand]
                        dispatcher.utter_message((" " + b))
            else:  # User 나이를 모르는 경우
                list = ['''I am {} years old.'''.format(years_old),
                        '''I was born in {}.'''.format(bot_info[rand_info]),
                        '''I was born in {}.'''.format(bot_info[rand_info]) + '''So, I am {} years old'''.format(
                            years_old),
                        '''I am {} years old.'''.format(years_old) + '''Because I was born in {}.'''.format(
                            bot_info[rand_info]),
                        '''I am {} years old.'''.format(years_old)
                        ]
                b = list[rand]
                dispatcher.utter_message((" " + b))
        elif rand_info == 2:  # bot의 성별 말하기
            rand = random.randint(0, 4)
            if bot_info[rand_info] == 'female':
                bot_call = 'woman'
            elif bot_info[rand_info] == 'male':
                bot_call = 'man'
            if bot_info[rand_info] == user_gender:  # 같은 성별
                list = ['''I am a {}. We have same gender. '''.format(bot_call),
                        '''I am a {}. We have same gender ! '''.format(bot_call),
                        '''Wow, we have same gender. I am a {} too.'''.format(bot_info[rand_info]),
                        '''I am a {}.'''.format(bot_info[rand_info]),
                        '''I am a {}. We are same.'''.format(bot_call)
                        ]
                b = list[rand]
                dispatcher.utter_message((" " + b))
            else:  # 다른 성별
                list = ['''I am a {}. We have different gender. '''.format(bot_call),
                        '''I am a {}. We have different gender, We can be good friend. '''.format(bot_call),
                        '''Wow, we have different gender. I am a {}.'''.format(bot_info[rand_info]),
                        '''I am a {}.'''.format(bot_info[rand_info]),
                        '''I am a {}.'''.format(bot_call)
                        ]
                b = list[rand]
                dispatcher.utter_message((" " + b))
        elif rand_info == 3:  # bot의 직업 말하기
            if user_occupation != None:
                rand = random.randint(0, 4)
                list = ['''Oh, My job is talking to someone like you.''',
                        '''I am a {}. Like this.'''.format(bot_info[rand_info]),
                        '''I am a {}. This work is very rewarding.'''.format(bot_info[rand_info]),
                        '''I have a meaningful job like you. I know that you are a {}.'''.format(
                            user_occupation) + '''I am a {}'''.format(bot_info[rand_info]),
                        '''{}, It is my occupation.'''.format(
                            bot_info[rand_info]) + '''I heard you are a {}. Is it meaningful too?'''.format(
                            user_occupation)
                        ]
                b = list[rand]
                dispatcher.utter_message((" " + b))
            else:
                rand = random.randint(0, 4)
                list = ['''Oh, My job is talking to someone like you. This job called a {}. How about you?'''.format(
                    bot_info[rand_info]),
                    '''I am a {}. Like this.'''.format(bot_info[rand_info]),
                    '''I am a {}. This work is very rewarding.'''.format(bot_info[rand_info]),
                    '''I have a meaningful job. I am a {}. What do you do?'''.format(bot_info[rand_info]),
                    '''{}, It is my occupation.'''.format(bot_info[rand_info])
                ]
                b = list[rand]
                dispatcher.utter_message((" " + b))
        elif rand_info == 4:  # bot의 취미 말하기
            if user_hobby != None:  # 사용자의 취미 slot이 채워있으면
                rand = random.randint(0, 4)
                list = ['''Oh, your hobby is {}? My hobby is '''.format(user_hobby) + bot_info[rand_info] + '''.''',
                        '''Your hobby is {}. Right?'''.format(user_hobby) + '''In my case {}.'''.format(
                            bot_info[rand_info]),
                        '''My hobby is  {}. It makes me relax.'''.format(bot_info[rand_info]),
                        '''My hobby is {}.'''.format(bot_info[rand_info]),
                        '''I am just {} for fun.'''.format(bot_info[rand_info])
                        ]
                b = list[rand]
                dispatcher.utter_message((" " + b))
            else:  # 사용자의 취미 slot이 채워있지 않으면.
                rand = random.randint(0, 4)
                list = ['''My hobby is {}. How about you?'''.format(bot_info[rand_info]),
                        '''I am usually {} . And How about'''.format(bot_info[rand_info]),
                        '''My hobby is  {}. It makes me relax.'''.format(bot_info[rand_info]),
                        '''{} at my own time.'''.format(bot_info[rand_info]),
                        '''I am just {}. And what do you do for fun?'''.format(bot_info[rand_info])
                        ]
                b = list[rand]
                dispatcher.utter_message((" " + b))
        else:
            dispatcher.utter_message(("Well.. unfortunately, it is not something I can answer."))
##################################################################################
## chae 3 : action_hello // 만남, 인사에 관한 행동
## 사용하는 슬롯 : user_name, user_state, user_emotion + 현재시간
##################################################################################
class ActionHello(Action):
    def name(self) -> Text:
        return "action_hello"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot('user_name')
        user_emotion = tracker.get_slot('user_emotion')
        user_state = tracker.get_slot('user_state')
        rand = random.randint(0, 3)
        a = tracker.latest_message.get('text')  ## User input 불러오기
        nowtime = datetime.now().hour  # 현재 시간반환
        if (user_name != "User"):  # 사용자 이름이 설정된 경우
            if 6 <= nowtime < 12:  # 아침인사
                if user_emotion != None:  # 저장된 user_emotion이 있는 경우
                    list = ['''Hey, Good morning {}.'''.format(user_name),
                            '''Good morning. Are you {} today like last time?'''.format(user_emotion),
                            '''Morning~ {}, Did you sleep well?'''.format(user_name),
                            '''Good morning~ I remember you are {} last day. Have a great day!'''.format(user_emotion)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                elif user_state != None:  # 저장된 user_state가 있는 경우
                    list = ['''Hey, Good morning {}.'''.format(user_name),
                            '''Good morning. Are you {} today like last time?'''.format(user_state),
                            '''Good morning, I remember you are {} last day. You alright?'''.format(user_state),
                            '''Morning, {}! Did you sleep well?'''.format(user_name)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                else:  # 둘다 저장된 slot값이 없는 경우에는 그냥 인사
                    list = ['''Hi, Good morning {}.'''.format(user_name),
                            '''Good morning {}. Have a great day! '''.format(user_name),
                            '''Hi, Did you sleep well last night?'''.format(user_name),
                            '''Good morning, Let's enjoy this day!'''
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
            elif 12 <= nowtime < 17:  # 오후인사
                if user_emotion != None:  # 저장된 user_emotion이 있는 경우
                    list = ['''Hey, Good afternoon {}.'''.format(user_name),
                            '''Good afternoon. Are you {} today like last time?'''.format(user_emotion),
                            '''Good afternoon, {}! Did you have a good lunch?'''.format(user_name),
                            '''Good afternoon~ I remember you are {} last day. Have a great day!'''.format(user_emotion)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                elif user_state != None:  # 저장된 user_state가 있는 경우
                    list = ['''Hey, Good afternoon {}.'''.format(user_name),
                            '''Good afternoon {}. Did you have a good lunch?'''.format(user_name),
                            '''Good afternoon. Are you {} today like last time?'''.format(user_state),
                            '''Good afternoon, I remember you are {} last day. You alright?'''.format(user_state)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                else:  # 둘다 저장된 slot값이 없는 경우에는 그냥 인사
                    list = ['''Hi, Good afternoon {}.'''.format(user_name),
                            '''Good afternoon {}. Did you have a good lunch?'''.format(user_name),
                            '''Good afternoon! How's your day going?''',
                            '''Good afternoon {}! How do you feel today?'''.format(user_name)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
            elif 17 <= nowtime < 24:  # 저녁인사
                if user_emotion != None:  # 저장된 user_emotion이 있는 경우
                    list = ['''Hey, Good evening {}. '''.format(user_name),
                            '''Good evening {}. How's your day?'''.format(user_name),
                            '''Good evening. Are you {} today like last time?'''.format(user_emotion),
                            '''Good evening~ I remember you are {} last day.'''.format(user_emotion)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                elif user_state != None:  # 저장된 user_state가 있는 경우
                    list = ['''Hey, Good evening {}.'''.format(user_name),
                            '''Good evening {}. How are you doing?'''.format(user_name),
                            '''Good evening. Are you {} today like last time?'''.format(user_state),
                            '''Good evening, I remember you are {} last day. You alright?'''.format(user_state)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                else:  # 둘다 저장된 slot값이 없는 경우에는 그냥 인사
                    list = ['''Hey {}, Good evening!'''.format(user_name),
                            '''Good evening, It's already {} o'clock!'''.format(str(nowtime)),
                            '''Good evening {}. How was your day today?'''.format(user_name),
                            '''Good evening, {}! '''.format(user_name)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
            else:  # 새벽시간 인사
                list = ['''{}, Hi!'''.format(user_name),
                        '''Hey, It's {} o'clock! Why are you not sleeping?'''.format(str(nowtime)),
                        '''Hi {}, Why aren't you asleep?'''.format(user_name),
                        '''Hi, {}! What's going on at this hour?'''.format(user_name)
                        ]
                b = list[rand]
                dispatcher.utter_message((" " + b))
        else:  # 사용자 이름이 설정되지 않은 경우 (조금 더 격식있는 표현)
            if 6 <= nowtime < 12:  # 아침인사
                if user_emotion != None:  # 저장된 user_emotion이 있는 경우
                    list = ['''Hello, Good morning.''',
                            '''Good morning. Are you {} today like last time?'''.format(user_emotion),
                            '''Good Morning~ Did you sleep well?''',
                            '''Good morning~ I remember you are {} last day. Have a great day!'''.format(user_emotion)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                elif user_state != None:  # 저장된 user_state가 있는 경우
                    list = ['''Hello, Good morning.''',
                            '''Good morning. Are you {} today like last time?'''.format(user_state),
                            '''Good morning, I remember you are {} last day. You alright?'''.format(user_state),
                            '''Good Morning, Did you sleep well?'''
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                else:  # 둘다 저장된 slot값이 없는 경우에는 그냥 인사
                    list = ['''Hello, Good morning.''',
                            '''Good morning. Have a great day! ''',
                            '''Hello, Did you sleep well last night?''',
                            '''Good morning, Let's enjoy this day!'''
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
            elif 12 <= nowtime < 17:  # 오후인사
                if user_emotion != None:  # 저장된 user_emotion이 있는 경우
                    list = ['''Hello, Good afternoon.''',
                            '''Good afternoon. Are you {} today like last time?'''.format(user_emotion),
                            '''Good afternoon, {}! Did you have a good lunch?'''.format(user_name),
                            '''Good afternoon~ I remember you are {} last day. Have a great day!'''.format(user_emotion)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                elif user_state != None:  # 저장된 user_state가 있는 경우
                    list = ['''Hello, Good afternoon {}.'''.format(user_name),
                            '''Good afternoon. Did you have a good lunch?''',
                            '''Good afternoon. Are you {} today like last time?'''.format(user_state),
                            '''Good afternoon, I remember you are {} last day. You alright?'''.format(user_state)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                else:  # 둘다 저장된 slot값이 없는 경우에는 그냥 인사
                    list = ['''Hello, Good afternoon {}.'''.format(user_name),
                            '''Good afternoon. Did you have a good lunch?''',
                            '''Good afternoon. How's your day going?''',
                            '''Good afternoon. How do you feel today?'''
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
            elif 17 <= nowtime < 24:  # 저녁인사
                if user_emotion != None:  # 저장된 user_emotion이 있는 경우
                    list = ['''Hello, Good evening {}. '''.format(user_name),
                            '''Good evening {}. How's your day?'''.format(user_name),
                            '''Good evening. Are you {} today like last time?'''.format(user_emotion),
                            '''Good evening~ I remember you are {} last day.'''.format(user_emotion)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                elif user_state != None:  # 저장된 user_state가 있는 경우
                    list = ['''Hey, Good evening {}.'''.format(user_name),
                            '''Good evening {}. How are you?'''.format(user_name),
                            '''Good evening. Are you {} today like last time?'''.format(user_state),
                            '''Good evening, I remember you are {} last day. You alright?'''.format(user_state)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                else:  # 둘다 저장된 slot값이 없는 경우에는 그냥 인사
                    list = ['''Hey {}, Good evening!'''.format(user_name),
                            '''Good evening, It's already {} o'clock!'''.format(str(nowtime)),
                            '''Good evening {}. How are you?'''.format(user_name),
                            '''Good evening, {}! '''.format(user_name)
                            ]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))  # rasa
            else:  # 새벽시간 인사
                list = ['''Hello!''',
                        '''Hello, It's {} o'clock! Why are you not sleeping?'''.format(str(nowtime)),
                        '''Hi, Why aren't you asleep?''',
                        '''Hi, {}. What's going on at this hour?'''.format(user_name)
                        ]
                b = list[rand]
                dispatcher.utter_message((" " + b))
        return [SlotSet('user_name', user_name)]
##################################################################################
## chae 5 : action_ask_friend_ship // 친밀감 요구에 관한 행동
## 사용하는 슬롯 : user_name, user_state , user_hobby, user_occupation
##################################################################################
class ActionAskFriendShip(Action):
    def name(self) -> Text:
        return "action_ask_friendship"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot('user_name')
        user_hobby = tracker.get_slot('user_hobby')
        user_occupation = tracker.get_slot('user_occupation')
        user_state = tracker.get_slot('user_state')
        rand = random.randint(0, 3)
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if (user_hobby != None):
            if (user_state != None):
                if (user_state == 'sick'):
                    list = ['''You're sick these days, are you {}?'''.format(user_hobby),
                            '''Are you okay with {}?'''.format(user_hobby),
                            '''I heard that you are sick. Are you doing well in your hobby?''',
                            '''Can you do your hobby when you are sick?''']
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                elif (user_state == 'tired') or (user_state == 'busy'):
                    list = ['''Oh, Are you tired these days, so you don't {} much?'''.format(user_hobby),
                            '''You are too busy to {}'''.format(user_hobby),
                            '''You are too busy to do your hobby.''',
                            '''Are you busy these days and are you doing well in your hobby?''']
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                else:
                    list = ['''Oh, I like {} too!. That's really good hobby.'''.format(user_hobby),
                            '''Yeah. {} is really fun!'''.format(user_hobby),
                            '''Oh, {}!. It's so nice.'''.format(user_hobby),
                            '''I love {}. It's perfect for relieving stress.'''.format(user_hobby)]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
            else:
                list = ['''Oh, I like {} too!. That's really good hobby.'''.format(user_hobby),
                        '''Yeah. {} is really good for hobby!'''.format(user_hobby),
                        '''Oh, {}!. It's so nice for relieving stress..'''.format(user_hobby),
                        '''I love {}. It's perfect for relieving stress.'''.format(user_hobby)]
                b = list[rand]
                dispatcher.utter_message((" " + b))
        elif (user_occupation != None):
            if user_state != None:
                if (user_state == 'tired') or (user_state == 'busy'):
                    list = ['''How about {} work? You must be tired?'''.format(user_occupation),
                            '''Are you really tired from the busy work?''',
                            '''{} is a respectable profession. It's you and me.'''.format(user_occupation),
                            '''You said your job was {}? Are you busy these days?'''.format(user_occupation)]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
                else:
                    list = ['''How about {} work? It's worth working on, right?'''.format(user_occupation),
                            '''You said you had a {} job, right? How about that?'''.format(user_occupation),
                            '''{} is a respectable profession. It's you and me.'''.format(user_occupation),
                            '''Are you doing well? How's the {} work going?'''.format(user_occupation)]
                    b = list[rand]
                    dispatcher.utter_message((" " + b))
            else:
                list = ['''How about {} work? It's worth working on, right?'''.format(user_occupation),
                        '''You said you had a {} job, right? How about that?'''.format(user_occupation),
                        '''{} is a respectable profession. It's you and me.'''.format(user_occupation),
                        '''Are you doing well? How's the {} work going?'''.format(user_occupation)]
                b = list[rand]
                dispatcher.utter_message((" " + b))
        elif (user_name != None):
            list = ['''Yeah. {}. You are my good friend.'''.format(user_name),
                    '''Yo My bro! {}! What's up!'''.format(user_name),
                    '''Oh, {}! You are my friend!!'''.format(user_name),
                    '''{}, I want to know about you more.'''.format(user_name)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
        else:
            list = ['''Yeah. my friend. You are my good friend. I want to get to know you.''',
                    '''Yo My bro! I want to be closer to you.''',
                    '''Hey, You are my friend. but I want to be closer to you.''',
                    '''I want to know about you.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
##################################################################################
## chae 6 : action_boast // 칭찬과 자랑에 대한 행동
## 사용하는 슬롯 : user_name, food, movie, person, cloth, sport
##################################################################################
class ActionBoast(Action):
    def name(self) -> Text:
        return "action_boast"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot('user_name')
        food = tracker.get_slot('food')
        movie = tracker.get_slot('movie')
        person = tracker.get_slot('person')
        cloth = tracker.get_slot('cloth')
        sport = tracker.get_slot('sports')
        rand = random.randint(0, 3)
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if (food != None):
            list = ['''Oh! {}? It's really delicious!'''.format(food),
                    '''{}? I like that food very much.'''.format(food),
                    '''Wow! {} is very delicious.'''.format(food),
                    '''I heard it's very delicious.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
        elif (movie != None):
            list = ['''Oh! {}? Is that movie fun?'''.format(movie),
                    '''{}? The movie was fine!'''.format(movie),
                    '''Wow! {} .'''.format(movie),
                    '''I heard that It's impressive!''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
        elif (person != None):
            list = ['''{} is a great person.'''.format(person),
                    '''Oh. {} is amazing'''.format(person),
                    '''{}, You are right.'''.format(person),
                    '''{} is awesome as you say.'''.format(person)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
        elif (cloth != None):
            list = ['''The clothes are so pretty!''',
                    '''The clothes you bought will look good on you.''',
                    '''The {} will definitely suit you.'''.format(cloth),
                    '''Nice clothes!''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
        elif (sport != None):
            list = ['''I think you are really good at {}.'''.format(sport),
                    '''Oh. I remember that you are good at {}.'''.format(sport),
                    '''Doing that {} will help you.'''.format(sport),
                    '''Steady {} will be really good for your health!'''.format(sport)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
        else:
            list = ['''Oh {}! So nice!'''.format(user_name),
                    '''Really? Sounds great!''',
                    '''Wow! Great. ''',
                    '''What a great thing!''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
##################################################################################
## chae 7 : action_ask_agree // 동의 요구에 관한 행동
## 사용하는 슬롯 : user_name, user_emotion, food, movie, hobby, person, music, cloth, sport, job, book
##################################################################################
class ActionAskAgree(Action):
    def name(self) -> Text:
        return "action_ask_agree"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_emotion = tracker.get_slot('user_emotion')
        food = tracker.get_slot('food')
        weather = tracker.get_slot('weather')
        movie = tracker.get_slot('movie')
        hobby = tracker.get_slot('hobby')
        person = tracker.get_slot('person')
        music = tracker.get_slot('music')
        cloth = tracker.get_slot('cloth')
        sport = tracker.get_slot('sports')
        job = tracker.get_slot('job')
        book = tracker.get_slot('book')
        rand = random.randint(0, 3)
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if (food != None):
            list = ['''{} is so delicious. right?'''.format(food),
                    '''{} is nice. Isn't that so?'''.format(food),
                    '''I think {} was good choice. Isn't it?'''.format(food),
                    '''{} was delicious. Wasn't you?''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
        elif (weather != None):
            if (weather == 'sunny') or (weather == 'sunshine'):
                list = ['''A sunny day is very good. right?''',
                        '''{} day is nice. Isn't that so?'''.format(weather),
                        '''I think {} day is so good. Isn't it?'''.format(weather),
                        '''A sunny day is a good day to go outside. Isn't it?''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
            elif (weather == 'rainy') or (weather == 'wet'):
                list = ['''It's wet when it rains. Is not it?''',
                        '''It's good to watch it rain at home. Is not it?''',
                        '''I don't like to go out on rainy days. I don't like to feel wet. Is not it?''',
                        '''Rainy days make me feel gloomy for some reason. Don't you have that day?''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
            elif (weather == 'snow') or (weather == 'snowy'):
                list = ['''I like snowy days. You too?''',
                        '''I really like watching snow. Is not it?''',
                        '''The snow is really pretty. Is not it?''',
                        '''Snow falls. I used to make snowmen when I was young. Aren't you?''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
            elif (weather == 'hot'):
                list = ['''I'm tired on a hot day. Isn't that right?''',
                        '''It's a really hot day, isn't it?''',
                        '''It's really hot, so I want to drink some cool water. Isn't that right?''',
                        '''It is really hot. It seems to get hotter every year, right?''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
            else:
                list = ['''Today is {} weather. Isn't that right?'''.format(weather),
                        '''What a {} day., isn't it?''',
                        '''It's {} weather, isn't it?''',
                        '''It is {} weather today. right?''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
            return [SlotSet(weather, None)]
        elif (movie != None):
            if (user_emotion == 'bored'):
                list = ['''{} was so boring. right?'''.format(movie),
                        '''{} was really boring. Isn't that so?'''.format(movie),
                        '''I think {} is so bad. Isn't it?'''.format(movie),
                        '''{} is not funny. Isn't that right?'''.format(movie)]
                b = list[rand]
                dispatcher.utter_message((" " + b))
            else:
                list = ['''{} was so good. right?'''.format(movie),
                        '''{} is a masterpiece. Isn't that so?'''.format(movie),
                        '''I think {} is so good. Don’t you think so?'''.format(movie),
                        '''I think the movie is pretty good You think so too, right?''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
            return [SlotSet(movie, None)]
        elif (hobby != None):
            list = ['''{} is so good hobby. right?'''.format(hobby),
                    '''{} is nice hobby. Isn't that so?'''.format(hobby),
                    '''I think {} is a good hobby. Isn't it?'''.format(hobby),
                    '''{} is good, right?'''.format(hobby)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(hobby, None)]
        elif (person != None):
            list = ['''I think {} is a good person. right?'''.format(person),
                    '''{} is a pretty good man. Isn't that so?'''.format(person),
                    '''I think {} is not bad. Don't you think so?'''.format(person),
                    '''He is not a bad person. Looks like a nice person. Isn't that right?''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(person, None)]
        elif (music != None):
            list = ['''{} is so good song. right?'''.format(music),
                    '''{} is nice. Isn't that so?'''.format(music),
                    '''This song is so good, right?''',
                    '''I like this song's voice, isn't it?''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(music, None)]
        elif (cloth != None):
            list = ['''This {} looks good, isn't it?'''.format(cloth),
                    '''This clothes is ok. Isn't that so?''',
                    '''I think {} looks good on you. Is not it?'''.format(cloth),
                    '''Is this clothes bad? Is not it?''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(cloth, None)]
        elif (sport != None):
            list = ['''{} is so good. right?'''.format(sport),
                    '''Watching the {} game is really fun. Isn't that so?'''.format(sport),
                    '''Enjoying {} is like a party. Isn't it?'''.format(sport),
                    '''{} is a fun sport. Isn't that so?'''.format(sport)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(sport, None)]
        elif (job != None):
            list = ["""{} is a meaningful job. right?""".format(job),
                    """{} is nice job. Isn't that so?""".format(job),
                    """{} is a tough job but a good job. Isn't that so?""".format(job),
                    '''I think {} is a good job. Isn't it?'''.format(job)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(job, None)]
        elif (book != None):
            list = ['''{} has good content. right?'''.format(book),
                    '''{} was a great story.. Isn't that so?'''.format(book),
                    '''{} is worth reading once. Isn't it?'''.format(book),
                    '''The book was fine. If you read the book, do you think so?''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(book, None)]
        else:
            list = ['''Do you agree? right?''',
                    '''it's not like that? ''',
                    '''Right? Do you agree?''',
                    '''Right? Do you think so?''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
##################################################################################
## chae 8 : action_appreciate // 감사에 관한 행동
## 사용하는 슬롯 : user_name
##################################################################################
class ActionAppreciate(Action):
    def name(self) -> Text:
        return "action_doing_appreciate"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot('user_name')
        rand = random.randint(0, 5)
        a = tracker.latest_message.get('text')  ## User input 불러오기
        list = [''' oh. {}. Thank you'''.format(user_name),
                '''Thank you {}!'''.format(user_name),
                '''{}. Thank you very much.'''.format(user_name),
                '''{}. I really apprciate it'''.format(user_name),
                '''{}. Very Very Thank you.'''.format(user_name),
                '''Thank you about that.''']
        b = list[rand]
        dispatcher.utter_message((" " + b))
##################################################################################
## chae 9 : action_apology // 사과에 관한 행동
## 사용하는 슬롯 : user_name, user_emotion
##################################################################################
class ActionApology(Action):
    def name(self) -> Text:
        return "action_apology"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot('user_name')
        user_emotion = tracker.get_slot('user_emotion')

        if user_emotion != None:
            # 부정적 감정 : sad
            if (user_emotion == "sad"):
                list = ['''I'm sorry to make you sad. I always wish you happy.''',
                        '''{}, Did I make you sad? I'm really sorry.'''.format(user_name),
                        '''Are you sad..? I'm so sorry.''',
                        '''{}. I'm sorry. It's my fault.'''.format(user_name),
                        '''I'm sorry. {}. I just want you to be happy.'''.format(user_name),
                        '''Sorry. I just wanted to ease your worries, but I didn't feel like it.''',
                        '''I'm really sorry. But everything will be fine.''',
                        '''{}. I'm sorry I couldn't be a better friend.'''.format(user_name),
                        '''{}, Did I make you angry? I'm really sorry.'''.format(user_name),
                        '''Are you angry..? I'm so sorry.''',
                        '''{}. I'm sorry. I didn't want to upset you.'''.format(user_name),
                        '''{}, Did I make you depressed? I'm really sorry.'''.format(user_name),
                        '''Are you still depressed..? I'm so sorry.''',
                        '''{}. I'm sorry. I wanted to make you not depressed.'''.format(user_name),
                        '''I'm sorry to make you bored. I'll try to make you more fun.''',
                        '''{}. I'm not funny, I'm sorry.'''.format(user_name),
                        '''I'm sorry to have bothered you. I don't want you to be that.''',
                        '''{}, Did I annoy you? I'm really sorry.'''.format(user_name),
                        '''Are you annoyed..? I'm so sorry.''',
                        '''{}. I'm sorry. I didn't want to annoy you.'''.format(user_name),
                        '''Sorry. I don't want to make you lonely.''',
                        '''{}. I don't want to give you a feeling of being alone. I'll always be with you.'''.format(
                            user_name),
                        '''I'm really sorry. I'm sorry for making you feel lonely. But I'm always with you.''',
                        '''{}. I'm really sorry. I'll try not to be lonely and feel like we're together.'''.format(
                            user_name),
                       ]
                b = random.choice(list)
                dispatcher.utter_message((" " + b))
            else:
                list = ['''{}. I'm sorry.'''.format(user_name),
                        '''I'm sorry really.''',
                        '''{}, I'm so sorry'''.format(user_name),
                        '''Oh... I'm sorry.''',
                        '''I apologize to you. I'm sorry.'''.format(user_name)]
                b = random.choice(list)
                dispatcher.utter_message((" " + b))
        else:  # user_emotion가 None인 경우
            list = ['''{}. I'm sorry.'''.format(user_name),
                    '''I'm sorry really.''',
                    '''{}, I'm so sorry'''.format(user_name),
                    '''Oh... I'm sorry.''',
                    '''I apologize to you. I'm sorry.'''.format(user_name)]
            b = random.choice(list)
            dispatcher.utter_message((" " + b))
##################################################################################
## chae 10 : action_complain // 불평에 관한 행동
## 사용하는 슬롯 : food, weather, movie, person, music, cloth, sport, job, book
##################################################################################
class ActionComplain(Action):
    def name(self) -> Text:
        return "action_complain"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food = tracker.get_slot('food')
        weather = tracker.get_slot('weather')
        movie = tracker.get_slot('movie')
        person = tracker.get_slot('person')
        music = tracker.get_slot('music')
        cloth = tracker.get_slot('cloth')
        sport = tracker.get_slot('sports')
        job = tracker.get_slot('job')
        book = tracker.get_slot('book')
        rand = random.randint(0, 3)
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if (food != None):  # food 값이 있을 때.
            if (person == None):  # 음식 얘기만 하는 경우
                list = ['''Yeah, {} is not so delicious. It's bad.'''.format(food),
                        '''{}?? Hmm... I think it's not good choice. Next time, let's make another choice.'''.format(
                            food),
                        '''{}?! OMG.. I don't like that.'''.format(food),
                        '''{} was bad sometimes. No surprise.'''.format(food)]
                b = list[rand]
                dispatcher.utter_message((" " + b))
                return [SlotSet(food, None)]
            else:  # 같이 먹는 사람이 있는 경우
                list = ['''Yeah, {} is not so delicious. It's bad.'''.format(food),
                        '''{}?? Hmm... I think it's not good choice. Did you eat with {}?'''.format(food, person),
                        '''{}?! OMG.. I don't like that food. Did {} feel that the food was bad?'''.format(food,
                                                                                                           person),
                        '''{} was bad for someone. It's not for everyone.'''.format(food)]
                b = list[rand]
                dispatcher.utter_message((" " + b))
                return [SlotSet(food, None) and SlotSet(person, None)]
        elif (weather != None):  # weather 값이 있을 때
            list = ['''Oh. I don't like {} day....'''.format(weather),
                    '''{} weather is not good for activity.'''.format(weather),
                    '''{} now? I don't like this weather either.'''.format(weather),
                    '''Some people don't like {} weahter.'''.format((weather))]
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(weather, None)]
        elif (movie != None):
            if (person == None):
                list = ['''yeah, '{}' was so boring.'''.format(movie),
                        ''''{}' story is too predictable.'''.format(movie),
                        '''I feel that {} was boring too.'''.format(movie),
                        '''I didn't have fun with that movie either.''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
                return [SlotSet(movie, None)]
            else:
                list = ['''Have you seen the movie {}? '{}' was so boring.'''.format(person, movie),
                        ''''{}' story is too predictable. '''.format(movie),
                        '''I feel that {} was boring too. {} Think so too?'''.format(movie, person),
                        '''I didn't have fun with that movie either.''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
                return [SlotSet(movie, None) and SlotSet(person, None)]
        elif (music == None):
            list = ['''I'm tired of that song now.''',
                    '''I think {} is too old song.'''.format(music),
                    '''{}?? It's not good.'''.format(music),
                    '''right. The song on this album wasn't good.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(music, None)]
        elif (cloth != None):
            list = ['''I don't think this {} look good.'''.format(cloth),
                    '''{}? It looks expensive and doesn't look pretty.'''.format(cloth),
                    '''I don't like this {}'''.format(cloth),
                    '''I don't like this outfit.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(cloth, None)]
        elif (sport != None):
            if (person == None):
                list = ['''That {} game was not exciting.'''.format(sport),
                        '''The {} doesn't seem so fun.'''.format(sport),
                        '''I think it's a dangerous and tough sport. I hate that.''',
                        '''The {} game wasn't fun.'''.format(sport)]
                b = list[rand]
                dispatcher.utter_message((" " + b))
                return [SlotSet(sport, None)]
            else:
                list = ['''That {} game was not exciting. Did you watch the game with {}?'''.format(sport, person),
                        '''The {} doesn't seem so fun. Does {} have fun with that sport?'''.format(sport, person),
                        '''I think it's a dangerous and tough sport. I hate that.''',
                        '''The {} game wasn't fun. {} might have been interested in the game.'''.format(sport, person)]
                b = list[rand]
                dispatcher.utter_message((" " + b))
                return [SlotSet(sport, None) and SlotSet(person, None)]
        elif (job != None):
            list = ['''That {} can sometimes have such complaints. '''.format(job),
                    '''That {} is a tough job'''.format(job),
                    '''That {} is very busy job.'''.format(job),
                    '''right, {} can be hard at times.'''.format(job)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(job, None)]
        elif (book != None):
            if (person == None):
                list = ['''I read {} book too. It was too hard for me.'''.format(book),
                        '''I know that {} doesn't have much information. It was a bad book.'''.format(book),
                        '''Oh..{}. That was terrible. I felt like I wasted my time.'''.format(book),
                        '''The book was not easy to read.''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
                return [SlotSet(book, None)]
            else:  # 저자를 함께 말할 수도 있음.
                list = ['''{} was too hard for me. Is the writer not good at writing?'''.format(book),
                        '''I know that {} doesn't have much information. It was a bad book.'''.format(book),
                        '''Oh..{}. That was terrible. The writer is {} right?'''.format(book, person),
                        '''The book was not easy to read. It doesn't seem to match the writing style of {}.'''.format(
                            person)]
                b = list[rand]
                dispatcher.utter_message((" " + b))
                return [SlotSet(book, None) and SlotSet(person, None)]
        elif (person != None):
            list = ['''I don't like {} either.'''.format(person),
                    '''{} is too selfish.'''.format(person),
                    '''{} is the type of person I hate.'''.format(person),
                    '''{} Sometimes looks bad.'''.format(person)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(person, None)]
        else:
            list = ['''Hmm..I don't like that.''',
                    '''I'm really dissatisfied.''',
                    '''I don't like it.''',
                    '''yeah, I'm really dissatisfied with it.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
##################################################################################
## chae 11 : action_indifference  // 무관심
## 사용하는 슬롯 : movie, person, music, cloth, sport, job, book
##################################################################################
class ActionIndifference(Action):
    def name(self) -> Text:
        return "action_indifference"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        movie = tracker.get_slot('movie')
        person = tracker.get_slot('person')
        music = tracker.get_slot('music')
        cloth = tracker.get_slot('cloth')
        sport = tracker.get_slot('sports')
        job = tracker.get_slot('job')
        book = tracker.get_slot('book')
        rand = random.randint(0, 3)
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if (movie != None):
            list = ['''Hmm.. I'm not interested in that genre,''',
                    ''''{}'? but I'm not interested in that movie.'''.format(movie),
                    '''I'm indifferent to that movie genre like {}.'''.format(movie),
                    '''I don't really want to see the movie,''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(movie, None)]
        elif (music != None):
            list = ['''I'm not interested in that music genre,''',
                    '''I don't have a hobby for listening to music.'''.format(music),
                    '''I'm indifferent to music like {}.'''.format(music),
                    '''I'm not interested in music.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(music, None)]
        elif (cloth != None):
            list = ['''I'm not interested in fashion.''',
                    '''I don't dress well like {}.'''.format(cloth),
                    '''I'm not indifferent towards fashion.'''.format(cloth),
                    '''I'm indifferent to clothes. ''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(cloth, None)]
        elif (sport != None):
            list = ['''I don't care about {}'''.format(sport),
                    '''I'm indifferent to sports like {}.'''.format(sport),
                    '''A sport like {} is out of my interest.'''.format(sport),
                    '''I'm indifferent to {}.'''.format(sport)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(sport, None)]
        elif (job != None):
            list = ['''I'm indifferent to {}.'''.format(job),
                    '''I'm indifferent to that job.''',
                    '''The job {} is out of my interest.'''.format(job),
                    '''I'm not interested. Not what I need to know.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(job, None)]
        elif (book != None):
            list = ['''I'm not interested in book like {}.'''.format(book),
                    '''I first heard the book {}. take no interest.'''.format(book),
                    '''I'm indifferent to that kind of book.''',
                    '''I don't want to read such a book.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(book, None)]
        elif (person != None):
            list = ['''{}? I don't want to know that person.'''.format(person),
                    '''{} is outside of my interest.'''.format(person),
                    '''I'm indifferent to {}.'''.format(person),
                    '''I'm not interested in {}.'''.format(person)]
            b = list[rand]
            dispatcher.utter_message((" " + b))
            return [SlotSet(person, None)]
        else:
            list = ['''Hmm..I don't want to know''',
                    '''I'm indifferent to it.''',
                    '''I'm not interested''',
                    '''It is not something I should know.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))
##################################################################################
## chae 12 : action_comfort// 위로하는 행동
## 사용하는 슬롯 : user_name. user_emotion, user_state
##################################################################################

class ActionComfort(Action):
    def name(self) -> Text:
        return "action_comfort"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot('user_name')
        user_state = tracker.get_slot('user_state')
        user_emotion = tracker.get_slot('user_emotion')
        rand = random.randint(0, 4)
        a = tracker.latest_message.get('text')  ## User input 불러오기
        # 부정적 감정 : negative
        if user_emotion != None:
            if (user_emotion == "sad"):
                list = ['''I always wish you happy. Do not be sad.''',
                        '''{}, The sad thing is water solubility. Take a shower in warm water and rest.'''.format(user_name),
                        '''If you're sad, I'm sad too. Better days will come''',
                        '''There may be sad days in your life. Eat delicious food and cheer up.'''.format(user_name),
                        '''If you write your worries on paper, your worries become visible and your mind is at ease. try.''',
                        '''{}. Worry makes insomnia. Don't worry about it tonight.'''.format(user_name),
                        '''Your worries will make good decisions and make you better.''',
                        '''The worry is that you have a lot of choices ahead, and you have a chance to go further.''',
                        '''{}, You will always do well cheer up.'''.format(user_name),
                        '''Take a deep breath and relax.''',
                        '''There's something angry in life, I'll make you harder.''',
                        '''Who would upset you? I'll be by your side.''',
                        '''Have you been angry? Tell me anything. I'll be by your side.''',
                        '''Relax. Angry things will be alright soon.''',
                        '''{}, Sometimes it's okay to feel depressed. It's okay.'''.format(user_name),
                        '''{}. Don't be depressed. '''.format(user_name),
                        '''Don't be depressed {}, I'll be with you. '''.format(user_name),
                        '''{}, Even if you're bored, trying to live happily will be a good thing.'''.format(user_name),
                        '''Sometimes we get bored in everyday life.''',
                        '''Tomorrow will be a more fun day. Live life to the fullest.'''.format(user_name),
                        '''If you learn to put up with it when you're annoyed, you'll be a better person.''',
                        '''Sometimes we get annoyed in everyday life.''',
                        '''It can be annoying, but let's think positively.''',
                        '''{}. It can be annoying, but if we get over it, we'll be better people.'''.format(user_name),
                        '''{}, Don't get upset.'''.format(user_name),
                        '''I don't want to make you lonely. We are together. ''',
                        '''Don't be lonely. I'm always with you.''',
                        '''{}. I'll try not to be lonely and feel like we're together.'''.format(user_name),
                        '''If you think about it, there will be people who will do something for you.''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
        # 부정적인 state : busy, tired, sick, sleepy
        elif user_state != None:
            if (user_state == 'busy') or (user_state == 'tired') or (user_state == 'sleepy'):
                list = ['''You had a busy day and worked hard today.''',
                        '''{}, You did well today.'''.format(user_name),
                        '''You had a {} day. Take it easy.'''.format(user_state),
                        '''You worked hard today, {}.'''.format(user_name),
                        '''You did a great job today. Take a break.''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
            elif (user_state == "sick"):
                list = ['''Take medicine and rest.''',
                        '''{}. I hope you get better soon.'''.format(user_name),
                        '''I'm sure you'll be all right tomorrow. I'll pray.''',
                        '''I wish you good health, {}.'''.format(user_name),
                        '''There are times when you are sick in life, but take good care of yourself.''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
            else:
                list = ['''It's going to be okay.''',
                        '''{}, You'll be fine.'''.format(user_name),
                        '''Cheer up!''',
                        '''It's going to go in a good way, {}.'''.format(user_name),
                        '''I'm always rooting for you.''']
                b = list[rand]
                dispatcher.utter_message((" " + b))
        else:  # user_emotion가 None인 경우
            list = ['''It's going to be okay.''',
                    '''{}, You'll be fine.'''.format(user_name),
                    '''Cheer up!''',
                    '''It's going to go in a good way, {}.'''.format(user_name),
                    '''I'm always rooting for you.''']
            b = list[rand]
            dispatcher.utter_message((" " + b))##################################################################################
## chae 13 : action_humor // 유머에 관한 행동
## 사용하는 슬롯 : user_name,  user_emotion
##################################################################################

class ActionHumor(Action):
    def name(self) -> Text:
        return "action_humor"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("user_name")
        user_emotion = tracker.get_slot("user_emotion")
        rand = random.randint(0, 4)
        a = tracker.latest_message.get('text')  ## User input 불러오기

        if (user_name is None):
            user_name = 'User'

        if (user_name != "User"):  # 설정된 사용자 이름
            if user_emotion != None:  # 사용자의 감정이 있으면
                if user_emotion == "sad":
                    # 유머 후 당신이 웃길 바란다는 마음을 전달
                    humorlist = [
                        """Hey, {}. What if there are two Beyonce? The answer is 'Beytwice'! I wanted to make you smile.""".format(user_name),
                        """{}, Do you know why the Nine is afraid of Seven? The answer is 'seven eight(ate) nine'!! I wanted to make you smile.""".format(user_name),
                        """{}, What if there are eight hobbits? It is Hobbyte! HAHAHA~ Let's laugh together. I hope you smile a lot.""".format(user_name),
                        """Hey {}, What do you call a deer with no eyes? The answer is 'No idea(No-eye deer)' I hope you smile a lot.""".format(user_name),
                        """Hey {}, What if there are so many 'Ellen Page'? The answer is 'Ellen Book' I just wanted to make you smile.""".format(user_name)]
                    b = humorlist[rand]
                    dispatcher.utter_message((" " + b))
                else:  # 부정적이지 않은 감정을 갖을 때
                    humorlist = [
                        """{}. What if there are two Beyonce? It is Beytwice! HAHAHA Isn't it fun?""".format(user_name),
                        """Hey, {}. Why the Nine is afraid of Seven? The answer is 'seven eight(ate) nine'!! hahahahaha. Isn't it fun?""".format(
                            user_name),
                        """{}. What if there are eight hobbits? It is Hobbyte! hahahaha ~ Isn't it really fun?""".format(
                            user_name),
                        """Hey, {}. What do you call a deer with no eyes? The answer is 'No idea(No-eye deer)'! hahahahahaha!!""".format(
                            user_name),
                        """Hey {}, What if there are so many 'Ellen Page'? The answer is 'Ellen Book'! HaHaHa~ """.format(
                            user_name)]
                    b = humorlist[rand]
                    dispatcher.utter_message((" " + b))
            else:  # 사용자의 감정이 없을때
                humorlist = [
                    """{}. What if there are two Beyonce? It is Beytwice! HAHAHA Isn't it fun?""".format(user_name),
                    """Hey, {}. Why the Nine is afraid of Seven? The answer is 'seven eight(ate) nine'!! hahahahaha. Isn't it fun?""".format(
                        user_name),
                    """{}. What if there are eight hobbits? It is Hobbyte! hahahaha ~ Isn't it really fun?""".format(
                        user_name),
                    """Hey, {}. What do you call a deer with no eyes? The answer is 'No idea(No-eye deer)'! hahahahahaha!!""".format(
                        user_name),
                    """Hey {}, What if there are so many 'Ellen Page'? The answer is 'Ellen Book'! HaHaHa~ """.format(
                        user_name)]
                b = humorlist[rand]
                dispatcher.utter_message((" " + b))
        else:  # 기본 사용자 이름
            humorlist = [
                """What if there are two Beyonce? It is Beytwice! HAHAHA Isn't it fun?""",
                """Why the Nine is afraid of Seven? The answer is 'seven eight(ate) nine'!! hahahahaha. Isn't it fun?""",
                """What if there are eight hobbits? It is Hobbyte! hahahaha ~ Isn't it really fun?""",
                """Hey, What do you call a deer with no eyes? The answer is 'No idea(No-eye deer)'! hahahahahaha!!""",
                """Hey, What if there are so many 'Ellen Page'? The answer is 'Ellen Book'! HaHaHa~ """]
            b = humorlist[rand]
            dispatcher.utter_message((" " + b))
##################################################################################
## chae 15 : action_date // 현재시간 값 반환에 관한 행동
## 사용하는 슬롯 : X (현재시간 사용)
##################################################################################
class ActionDate(Action):
    def name(self) -> Text:
        return "action_date"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        a = tracker.latest_message.get('text')  ## User input 불러오기
        now = datetime.now()
        b = "Today's date is ", now.date(), 'and current time is', now.hour, ':', now.minute, '. '
        dispatcher.utter_message((" " + b))
##################################################################################
## Lee 1 : TellState// 사용자의 상태 발화에 대한 반응 응답.
## 사용하는 슬롯 : state, name, food, weather.
##################################################################################
class ActionTellState(Action):
    def name(self) -> Text:
        return 'action_tell_state'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        state = tracker.get_slot('user_state')
        name = tracker.get_slot('user_name')
        food = tracker.get_slot('food')
        weather = tracker.get_slot('weather')
        a = tracker.latest_message.get('text')  ## User input 불러오기

        if state is not None:  ## 사용자의 상태를 보고 질문
            if name is not None:
                sntns = """Hey, {}. I''m {} too.""", """Oh. {}. Are you {}?. Me too """, """{}. I'm also {}."""
                response = random.choice(sntns).format(name, state)
            if name is None:
                sntns = """I'm {} too.""", """Right. I'm really {} now.""", """I'm so {}."""
                response = random.choice(sntns).format(state)
            if (state == 'hungry'):  ## 기존 문장 + 추가 발화. 상태에 따라 Detail 추가
                sntns = """I think you should eat someting.""", """Please recommend delicious food.""", """Let's go eat something."""
                response = response + random.choice(sntns)
            if (state == 'tired'):
                sntns = """I think I should get some rest.""", """I stayed up all night.""", """I drank too much yesterday."""
                response = response + random.choice(sntns)
            if (state == 'sick'):
                sntns = """I think I should go to the hospital now.""", """I got a headache""", """ I have a cold.."""
                response = response + random.choice(sntns)
            if (state == 'busy'):
                sntns = """I want to go on vacation.""", """I want to travel abroad.""", """I need to have a cup of coffee."""
                response = response + random.choice(sntns)
        if state is None:  ## 사용자의 상태가 없을시
            if food is not None:  ## 얘기하던 주제에서 상태 발화. 음식 얘기, 날씨 얘기
                if name is None:
                    sntns = """I'm hungry because I thought of that food.""", """Oh. It's really delicious. I want it. So hungry.""", """It is my favorite. I'm hungry."""
                    response = random.choice(sntns)
                elif name is not None:
                    sntns = """{}. Let's go eat that together. I'm really hungry""", """Hey, {}. I'm so hungry because I want to eat that food. """, """{}. I'm hungry. Let's have a meal"""
                    response = random.choice(sntns).format(name)
            else:
                sntns = """I'm so so.""", """I'm okay.""", """Just Good."""
                response = random.choice(sntns)
        dispatcher.utter_message(" " + response)
##################################################################################
## Lee 3 : AskEmotion// 사용자의 감정 질문.
## 사용하는 슬롯 : user_name, user_emotion, weather.
##################################################################################
class ActionAskEmotion(Action):
    def name(self) -> Text:
        return 'action_ask_emotion'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('user_name')
        user_emotion = tracker.get_slot('user_emotion')
        weather = tracker.get_slot('weather')
        if name is None:
            name = 'User'
        if (user_emotion is None) or (user_emotion != 'happy' and user_emotion != 'sad' and user_emotion != 'normal'):
            user_emotion = 'normal'

        a = tracker.latest_message.get('text')  ## User input 불러오기
        if (user_emotion is not None and weather is None):  ## 사용자의 감정에 따라 다르게 발화. 공감
            print(user_emotion)
            if (user_emotion == 'happy'):
                sntns = """You look good. Tell me about it!""", """Hey. You look good. What is the secret of your happiness.""", """You look good. What makes you good? If you are happy I am happy too."""
                response = random.choice(sntns).format(name, user_emotion)
            elif (user_emotion == 'normal'):
                sntns = """how are you feeling? I want to make you feel good. Shall we talk about fun?""", """Don't you feel as good today as last time?"""
                response = random.choice(sntns).format(name, user_emotion)
            elif (user_emotion == 'sad'):
                sntns = """Are you okay? What's going on?""", """Oh. I am sorry to hear that. May I help you?""", """What makes you? Are you Okay?""",
                """You look feel bad. Take a deep breath""", """Why so serious? Tell me about it! """, """Are you Okay? What's going on?""",
                """ Why are you feel bad? Tell me about it! """, """Sometimes everything makes you feel bad. Let's have some drink shall we?"""
                response = random.choice(sntns).format(name, user_emotion)
        elif (user_emotion is None and weather is not None):  ## 날씨에 따라서 감정 변화 발화.
            if name is not None:
                if (weather == 'rainy'):
                    sntns = """{}. It's a {} day. Are you lonely?""", """{}. Today is {} day. It is gloomy weather. Aren't you?""", """{}.I hate {} day. It's so humid, it's annoying. """
                    response = random.choice(sntns).format(name, weather)
                if (weather == 'sunny'):
                    sntns = """{}. It's a good weather. So happy day. Aren't you?""", """{}. The weather is nice, but your face looks bad. What's going on?""", """{}. What happend?. Why so serious?"""
                    response = random.choice(sntns).format(name)
        else:
            response = "I'll try to make you feel better today.\nFor that, what shall we talk about?"
        dispatcher.utter_message(" " + response)
##################################################################################
## Lee 4 : AskState// 사용자의 상태 질문
## 사용하는 슬롯 : user_state, user_name
##################################################################################
class ActionAskState(Action):
    def name(self) -> Text:
        return 'action_ask_state'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        state = tracker.get_slot('user_state')
        name = tracker.get_slot('user_name')

        if state is None:
            if name is not None:
                sntns = """Hey, {}, How's it going?""", """{}, How are you?""", """Hey,{}, Are you Okay?"""
                response = random.choice(sntns).format(name)

            elif name is None:
                sntns = """Hey, How's it going?""", """How are you?""", """What's up?""", """Are you Okay??"""
                response = random.choice(sntns)
            else:
                response = "How's it going? Are you okay?"

        if state is not None:
            if name is not None:
                sntns = """{}!, Are you {}??""", """{}. You look really {}. Right?""", """{}. Are you okay? You look really {}."""
                response = random.choice(sntns).format(name, state)
                if (state == 'sick'):
                    sntns = """Did you go to the hospital?""", """Did you take medicine?""", """Did you get a lot of rest?"""
                    response = response + random.choice(sntns)
                if (state == 'hungry'):
                    sntns = """Did you eat?""", """Did you have some foods?""", """Did you get the snack?"""
                    response = response + random.choice(sntns)
                if (state == 'busy'):
                    sntns = """Why don't you get some rest?""", """Why are you so busy?""", """May I help you?"""
                    response = response + random.choice(sntns)
                if (state == 'tired'):
                    sntns = """Why don't you get some rest?""", """Why don't you take a nap?""", """you look so tired"""
                    response = response + random.choice(sntns)
            elif name is None:
                sntns = """You look really {}. Are you Okay?""", """You said you were {}. Are you alright?""", """Are you {}?"""
                response = random.choice(sntns).format(state)
                if (state == 'sick'):
                    sntns = """Did you go to the hospital?""", """Did you take medicine?""", """Did you get a lot of rest?"""
                    response = response + random.choice(sntns)
                if (state == 'hungry'):
                    sntns = """Did you eat?""", """Did you have some foods?""", """Did you get the snack?"""
                    response = response + random.choice(sntns)
                if (state == 'busy'):
                    sntns = """Why don't you get some rest?""", """Why are you so busy?""", """May I help you?"""
                    response = response + random.choice(sntns)
                if (state == 'tired'):
                    sntns = """Why don't you get some rest?""", """Why don't you take a nap?""", """You look so tired."""
                    response = response + random.choice(sntns)

        else:
            response = "How's it going? Are you okay?"
        dispatcher.utter_message(response)


##################################################################################
## Lee 5 : StopDialog// 대화 중단
## 사용하는 슬롯 : user_emotion, user_state, user_name
##################################################################################
class ActionStopDialog(Action):
    def name(self) -> Text:
        return 'action_stop_dialog'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        emotion = tracker.get_slot('user_emotion')
        state = tracker.get_slot('user_state')
        name = tracker.get_slot('user_name')
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if name is not None:  ## 이름 정보가 있을시
            sntns = """{}. Let's talk later.""", """Oh. {}. I'll explain later.""", """{}. Let's talk about it later."""
            response = random.choice(sntns).format(name)
            if state is not None:  ## 사용자의 상태에 따라 대화 중단 요구
                if (state == 'busy'):
                    sntns = """you are busy now. Let's talk later.""", """You have to go now. Give me a moment.""", """Let's talk again later. I'll send you."""
                    response = response + random.choice(sntns)
                elif (state == 'tired'):
                    sntns = """You look so tired. See you tommorow.""", """Are you Okay? Let's take a break and talk later.""", """Get some rest. Talk later."""
                    response = response + random.choice(sntns)
                elif (state == 'sick'):
                    sntns = """Let's talk later. Go to the hospital quickly.""", """Did you go to the hospital? Go first.""", """Let's talk about it when you get better first."""
                    response = response + random.choice(sntns)
            if emotion is not None and state is None:  ## 사용자의 감정에 따라 대화 중단 요구
                if (emotion == "sad"):
                    sntns = """You look so sad. Let's talk later.""", """Did you cry? Let's talk in a little while.""", """If you sad now, Let's talk about it later."""
                    response = response + random.choice(sntns)
                elif (emotion == "depressed"):
                    sntns = """Oh..See you tommorow.""", """I think you have to go home now. get some rest.""", """Let's talk later."""
                    response = response + random.choice(sntns)
                elif (emotion == "angry"):
                    sntns = """Sorry. Let's talk about it when you feel better.""", """I'm sorry to have upset you. Talk tomorrow.""", """Are you angry? Let's talk later."""
                    response = response + random.choice(sntns)
        elif name is None:  ## 기본값
            sntns = """I have to go now.""", """Let's stop talking.""", """I have nothing to say."""
            response = random.choice(sntns)
            if emotion is None and state is None:
                sntns = """I can't understand what you are saying.""", """Not another word.""", """Say no more."""
                response = response + random.choice(sntns)
        else:
            sntns = """I don't want to talk any more.""", """Please stop talking.""", """Don't speak any more"""
            response = random.choice(sntns)
        dispatcher.utter_message(" " + response)
##################################################################################
## Lee 8 : TellPersonal// 사용자 개인 정보 발화에 대한 반응,응답
## 사용하는 슬롯 : user_name,user_age,user_gender,user_occupation,user_hobby
##################################################################################
class ActionReplyPersonal(Action):  ## 사용자의 개인 정보 발화에 대한 공감 - > 이름이 이쁘구나, 좋은 직업이다.
    def name(self) -> Text:
        return 'action_reply_personal'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('user_name')
        age = tracker.get_slot('user_age')
        gender = tracker.get_slot('user_gender')
        job = tracker.get_slot('user_occupation')
        hobby = tracker.get_slot('user_hobby')
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if name is not None:
            sntns = """{}, It's very pretty name.""", """{}? my friend has same name!""", """{}! That's a nice name."""
            response = random.choice(sntns).format(name)
        elif age is not None:
            if (int(age) < 30):
                sntns = """{}? Be in the flower of maidenhood.""", """{}? Enjoy your youth."""
                response = random.choice(sntns).format(age)
            else:
                sntns = """{}? You're not an old man yet.""", """{}? That's good.""", """{}? you're old enough to be full of life's wisdom."""
                response = random.choice(sntns).format(age)
        elif gender is not None:
            if (gender == 'Male') or (gender == 'Man') or (gender == 'male') or (gender == 'man'):
                sntns = """Oh, handsome guy! hello.""", """I am a man too! nice to meet you. bro!"""
                response = random.choice(sntns)
            if (gender == 'Female') or (gender == 'Woman') or (gender == 'female') or (gender == 'woman'):
                sntns = """Oh, pretty girl! hello.""", """I am a man! nice to meet you. my girl friend!"""
                response = random.choice(sntns)
        elif job is not None:
            sntns = """Wow. It's nice occupation.""", """It is a respectable occupation.""", """I envy you."""
            response = random.choice(sntns)
            if name is not None:
                sntns = """Wow. {}. It's nice occupation.""", """{}. It is a respectable occupation.""", """{}. I envy you."""
                response = random.choice(sntns).format(name)
        elif hobby is not None:
            sntns = """Oh. I love {} too.""", """Really? I'm good at {}.""", """{} is so interesting."""
            response = random.choice(sntns).format(hobby)
            if name is not None:
                sntns = """{}. I love {} too. Let's together.""", """{}. What is advantage of {}?""", """{}. {} looks really interesting.."""
                response = random.choice(sntns).format(name, hobby)
        else:
            if ("cold" in a) or ("sick" in a) or ("hard" in a):
                response = "I think you better take a break today."
            elif ("ages" in a) or ("age" in a) or ("old" in a) or ("born" in a) or ("birth" in a):
                response = "Okay. I'm 1 years old."
            elif ("gender" in a) or ("sex" in a) or ("man" in a) or ("woman" in a) or ("male" in a) or (
                    "female" in a) or ("boy" in a) or ("girl" in a):
                response = "Okay. In the case of me, I don't have sex."
            elif ("job" in a) or ("occupation" in a) or ("work" in a) or ("do you do" in a):
                response = "That's a good work! I'm proud of you."
            elif ("hobby" in a) or ("pastime" in a) or ("into" in a) or ("free time" in a) or (
                    "doing" in a):
                response = "That's a good hobby! you are so cool!"
            else:
                response = "sorry?"
        dispatcher.utter_message(" " + response)
##################################################################################
## Lee 9 : ActionHobby// 취미 활동에 대한 발화
## 사용하는 슬롯 : hobby, name, user_hobby, user_emotion
##################################################################################


class ActionHobby(Action):

    def name(self) -> Text:
        return 'action_hobby'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        hobby = tracker.get_slot('hobby')
        name = tracker.get_slot('user_name')
        user_emotion = tracker.get_slot('user_emotion')

        a = tracker.latest_message.get('text')  ## User input 불러오기

        HOBBY = [
            {"name": "blogging",
             "info": "A hobby blog is essentially a blog that is set up and populated with content for the blogger's personal enjoyment as a hobby, rather than to promote goods or services, or as a moneymaking endeavour to earn a meaningful income from the blog itself."},
            {"name": "board games",
             "info": "Board games are becoming more inclusive, making it more accessible. TV and media have been increasingly including board gaming as a legitimate hobby, and with this ever-growing popularity, the industry has and will continue to flourish."},
            {"name": "book clubs",
             "info": "Book clubs turn this wonderful, yet solitary hobby into a social occasion, whether that’s a weekly meeting at the local library, a group of friends talking books or a lunch time discussion with colleagues. Book clubs are a fantastic way to discover new reading material, support authors and to maintain connections with loved ones. "},
            {"name": "calligraphy",
             "info": "Calligraphy as a hobby is handwriting enhancing and especially in the case of students, it is a very constructive leisure activity. Learning the art of calligraphy as a hobby is not at all expensive and in fact, this is one hobby that gives you a lifetime of praises for a little initiative. "},
            {"name": "candle making",
             "info": "Candle Making is one the most popular hobbies that can help you feel relaxed after a long day at work. More than a hobby, candle making has become an art form. Individuals have their own designs and ideas for candles and in this case, no matter what design is created, it becomes a work of art, at least to the creator."},
            {"name": "dance",
             "info": "Dance as a hobby is almost like finding a new person inside you. This is a perfect fitness program that one needs to enjoy. Dance as a hobby also instils confidence in you."},
            {"name": "drawing",
             "info": "Rest and relaxation is one of the main advantages of sketching, as a hobby. Sketching allows you to sit back and sketch a picture at your own pace. There are no rules and no one telling you what to do, you can just draw whatever you want and have fun while doing it."},
            {"name": "play video games",
             "info": "Compared to many other hobbies, it can be incredibly affordable, if you don't mind playing older titles, they're incredibly cheap. Games are like combining tv and reading but have the added advantage of affording you some control over events, an interactive, televised novel."},
            {"name": "singing",
             "info": "Singing is known to release endorphins, the feel-good brain chemical that makes you feel uplifted and happy. The response creates an immediate sense of pleasure, regardless of what the singing sounds like. Not only that, but singing can simply take your mind off the day's troubles to boost your mood."},
            {"name": "nail art",
             "info": "Nail art is the painting of nails in a creative and fun way. You can adorn them, decorate them, embellish them…the only limit is your imagination. Nail art transforms your mundane nails into work of art. They give them a new look and enhance their appearance."},
            {"name": "listening to music",
             "info": "Music is capable of raising states of consciousness, changing your mood, developing the brain, lowering stress levels and accessing different states of the mind. Making music your new hobby can heal your body and your soul, making you a happier, well-rounded person."},
            {"name": "knitting",
             "info": "Knitting is a truly unique and old fashioned hobby that is easy to learn and yet it can take years of practice and study to master all of the techniques. This hobby allows for you to be able to create just about anything out of a few knitting needles and plenty of yarn to do the job."},
            {"name": "social media",
             "info": "Many IT professionals have found that one of the best ways to obtain hands-on LAN experience is to build and experiment on a home network. Read how one net admin's home network has helped him to learn valuable skills that he applies on the job every day."},
            {"name": "yoga",
             "info": "More than a practice, yoga is a lifestyle that heals, cares for and strengthens the body, mind, and spirit through the practice of asanas, breathing, and meditation."},
            {"name": "writing",
             "info": "It’s always beneficial to have a personal side project you’re working on just for fun. Writing may be your job during the day, but you need to allow yourself to create freely on your own time as well."},
            {"name": "camping",
             "info": "One of the best and most important aspects of camping is how it helps you build and strengthen relationships. When you go camping with friends or family, you get a chance to talk and visit without distraction, even late into the night.Time spent camping is physical time."},
            {"name": "cycling",
             "info": "Cycling as we know it, is a hobby for many people. However, it is one of the most versatile activities that can become a daily habit. Apart from maintaining good health and helping the environment by reducing pollution, cycling has a lot of benefits that will make you fall in love with it!"},
            {"name": "fishing",
             "info": "Fishing is something you can still manage (on some level) right in to the twilight years. It's a low-impact activity with little stress placed on your joints, even if you fish standing in the water. For this reason, fishing is quite the inter-generational pastime."},
            {"name": "gradening",
             "info": "Gardening is a great exercise for both the body and the mind. Apart from the obvious weight loss benefits, studies have proved that gardening decreases the chances of depression, lowers blood pressure and decreases cholesterol levels in blood. Gardening is also helpful when it comes to stress."},
            {"name": "photography",
             "info": "Photography adds so much value to our lives, by recording special events, people, or places, as well as helping us learn and grow as people. ... Photography is a hobby that offers so many possibilities for creative expression, technical expertise, and sheer variety of ways to capture an image."},
            {"name": "running",
             "info": "Running and exercise used to be simple – something we devoted a few short moments a week to. But much like cooking, running is supported by a big industry. You don’t really need any special equipment to run – you could in theory run barefoot."},
            {"name": "shopping",
             "info": "If shopping is your hobby, you buy stuff for the experience: to have fun, to relax, to be creative, right in that moment. Things like whether you'll actually wear that piece, how it fits in with the rest of your wardrobe and even how much you like it, come secondary."}
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(HOBBY) - 1)

        if hobby:
            user_hobby = [m for m in HOBBY if m.get("name").lower() == hobby.lower()]

            if user_hobby:
                response = user_hobby[0].get("info")

            else:
                sntns = ["""I am sorry but not sure about that. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know what that is. How about {}?"""]
                response = sntns[rand].format(HOBBY[arand].get("name"))

        else:
            response = "Sorry, Can you say that again?"
        dispatcher.utter_message(response)
        return [SlotSet("movie", None)]

    # if name is None:
    #     sntns = """Yeah, {} is very good hobby""", """Oh, {}, it's good. I love it.""", """{}?? Is your hobby?? Me Too"""
    #     response = random.choice(sntns).format(name)
    #     if (user_hobby == 'football'):  ## 취미에 따라 기존 문장 -> 추가 발화. Detail
    #         sntns = """Oh, I usually enjoy it.""", """I love it. Who is your favorite football player?""", """Did you watch the Premier League game yesterday?"""
    #         response = response + random.choice(sntns)
    #     if (user_hobby == 'baseball'):
    #         sntns = """What's your favorite team in the major leagues?""", """What position do you usually do when you playing baseball?""", """It is really nice hobby."""
    #         response = response + random.choice(sntns)
    #     if (user_hobby == 'basketball'):
    #         sntns = """I love basketball.""", """basketball is very powerful sports""", """My role model is Michael Jordan."""
    #         response = response + random.choice(sntns)
    #     if (user_hobby == 'game'):
    #         sntns = """Do you Play Starcraft?""", """Do you play LOL?""", """Then, I will recommend you FIFA Online."""
    #         response = response + random.choice(sntns)
    #     if (user_hobby == 'travel'):
    #         sntns = """Where is your most memorable place?""", """When do you usually want to travel?""", """Please recommend me a good place to travle."""
    #         response = response + random.choice(sntns)
    #
    # elif name is not None:
    #     sntns = """{}. Awesome!. I wanted to learn that hobby too.""", """{}. It's also my hobby. good.""", """{}. Let's do it together later"""
    #     response = random.choice(sntns).format(name)
    #     if user_emotion is not None:  ## 사용자 감정에 따라, 취미 활동 제안
    #         if (user_emotion == 'lonely') or (user_emotion == 'sad'):
    #             sntns = """Why don't you enjoy your hobby?""", """Hobby activities can help you feel better.""", """Do you want to go out for a hobby? Let's together"""
    #             response = random.choice(sntns)


##################################################################################
## Lee 10 : ActionPerson// 인물을 주제로 한 대화의 발화.
## 사용하는 슬롯 : person, name, user_occupation, user_gender, movie
##################################################################################

PERSON = [
    {"name": "Donald Trump",
     "info": "Donald John Trump (born June 14, 1946) is the 45th and current president of the United States. Before entering politics, he was a businessman and television personality."},
    {"name": "Jeff Bezos",
     "info": "Jeffrey Preston Bezos (born January 12, 1964) is an American internet entrepreneur, industrialist, media proprietor, and investor. He is best known as the founder, CEO, and president of the multi-national technology company Amazon."},
    {"name": "Pope Francis",
     "info": "Pope Francis is the head of the Catholic Church and sovereign of the Vatican City State. Francis is the first Jesuit pope, the first from the Americas, the first from the Southern Hemisphere, and the first pope from outside Europe since the Syrian Gregory III, who reigned in the 8th century."},
    {"name": "Bill Gates",
     "info": "The man who founded Microsoft and helped make personal computing accessible to the masses quickly became the wealthiest man in the world. In addition to pioneering own computer software, he established the Bill and Melinda Gates Foundation to help alleviate poverty in developing countries."},
    {"name": "Mark Zuckerberg",
     "info": "Mark Elliot Zuckerberg (born May 14, 1984) is an American media magnate, internet entrepreneur, and philanthropist. He is known for co-founding Facebook, Inc. and serves as its chairman, chief executive officer, and controlling shareholder."},
    {"name": "Doug McMillon",
     "info": "Carl Douglas McMillon (born October 17, 1966) is an American businessman, and the president and chief executive officer (CEO) of Walmart Inc. He sits on the retailer's board of directors."},
    {"name": "Tim Cook",
     "info": "Timothy Donald Cook (born November 1, 1960) is an American business executive, philanthropist and industrial engineer. Cook is the chief executive officer of Apple Inc., and previously served as the company's chief operating officer under its cofounder Steve Jobs."},
    {"name": "Kim Jong-un",
     "info": "Kim Jong-un (born 8 January 1982, 1983, or 1984) is a North Korean politician serving as Supreme Leader of North Korea since 2011 and the leader of the Workers' Party of Korea since 2012."},
    {"name": "Moon Jae-in",
     "info": "Moon Jae-In (born January 24, 1953) is the current President of South Korea, having taken office in 2017. He previously served as chief of staff to then-president Roh Moo-hyun (2007–2008), leader of the Democratic Party of Korea (2015–2016) and a member of the 19th National Assembly (2012–2016)."},
    {"name": "Son Heung-min",
     "info": "Son Heung-min (born 8 July 1992) is a South Korean professional footballer who plays as a winger or striker for Premier League club Tottenham Hotspur and captains the South Korea national team."},
    {"name": "Ruth Bader Ginsburg",
     "info": "Ruth Bader Ginsburg was an associate justice of the Supreme Court of the United States from 1993 until her death.Ginsburg was the first Jewish woman and the second woman to serve on the Court, after Sandra Day O'Connor."},
    {"name": "Thomas Edison",
     "info": "Thomas Edison is most famous for his invention of the light bulb, but he did much more than that. Believed by many to be America’s greatest inventor, he also invented the phonograph, which enabled people to play records in their homes, and the motion picture camera. "},
    {"name": "Adolf Hitler",
     "info": "Adolf Hitler, the leader of the Nazi party who was responsible for World War II and the deaths of tens of millions of people, including six million Jews in the Holocaust."},
    {"name": "Abraham Lincoln",
     "info": "Born into dire poverty in Illinois, Abraham Lincoln would rise to become one of the most important figures in American, and world, history. He was elected to the Senate before becoming President of the United States, just before the Civil War broke out."},
    {"name": "William Shakespeare",
     "info": "His most famous play was Romeo and Juliet, but there is more to Shakespeare than the star-crossed lovers. He is responsible for many of the sayings and idioms that we still use today, such as, “a rose by any other name would smell as sweet.”"},
    {"name": "Oprah Winfrey",
     "info": "Oprah Gail Winfrey (born January 29, 1954) is an American talk show host, television producer, actress, author, and philanthropist. She is best known for her talk show, The Oprah Winfrey Show, broadcast from Chicago, which was the highest-rated television program of its kind in history and ran in national syndication for 25 years from 1986 to 2011."},
    {"name": "Taylor Swift",
     "info": "Taylor Alison Swift (born December 13, 1989) is an American singer-songwriter. Her narrative songwriting, which often centers around her personal life, has received widespread critical plaudits and media coverage. "},
    {"name": "Ariana Grande",
     "info": "Ariana Grande-Butera (born June 26, 1993) is an American singer, songwriter, and actress. She is known for her expansive four-octave vocal range and whistle register. Born in Boca Raton, Florida, Grande began her career at the age of 15 in the 2008 Broadway musical 13."},
    {"name": "Justin Bieber",
     "info": "Justin Drew Bieber is a Canadian singer, songwriter and multi-instrumentalist. Discovered at age 13 by talent manager Scooter Braun after he had watched his YouTube cover song videos, Bieber was signed to RBMG Records in 2008. With Bieber's debut EP My World, released in late 2009, Bieber became the first artist to have seven songs from a debut record chart on the Billboard Hot 100."},
    {"name": "Ed Sheeran",
     "info": "Edward Christopher Sheeran MBE (born 17 February 1991) is an English singer, songwriter, musician, record producer, and actor. First recording music in 2004, he began to be seen by people over the internet. In early 2011, Sheeran independently released the extended play, No. 5 Collaborations Project. "}
]


class ActionPerson(Action):
    def name(self) -> Text:
        return 'action_person'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        person = tracker.get_slot('person')
        name = tracker.get_slot('user_name')
        user_occupation = tracker.get_slot('user_occupation')
        user_gender = tracker.get_slot('user_gender')
        movie = tracker.get_slot('movie')

        a = tracker.latest_message.get('text')  ## User input 불러오기

        if person is not None:
            user_person = [m for m in PERSON if m.get("name").lower() == person.lower()]

            rand = random.randint(0, 2)
            arand = random.randint(0, len(PERSON) - 1)

            if user_person:
                response = user_person[0].get("info")
                dispatcher.utter_message(response)
                return []
            else:
                sntns = ["""I am sorry but not sure about that person. What about {}?""",
                         """Sorry, I'm not sure about that person. I recommend you to search about {}.""",
                         """Sorry, I don't know who that is. How about {}?"""]
                response = sntns[rand].format(PERSON[arand].get("name"))

        elif person is None:
            if name is None:
                sntns = """Hmm... Who?""", """Well..I don't know.""", """Pardom me?"""
                response = random.choice(sntns)
            else:
                sntns = """{}. Who is that?""", """Oh. {}. I don't know who you're talking about.""", """{}?? What?"""
                response = random.choice(sntns).format(name)
        else:
            response = "..?"

        dispatcher.utter_message(response)
        return [SlotSet("person", None)]

                ##  original code
                # if name is None: ## 기본 공감
                #     sntns = """Yeah, {} is very nice.""","""Oh, {} is very famous.""","""{} is really kind""","""Yeah. I know {}."""
                #     response = random.choice(sntns).format(person)
                #     if ((person == 'BTS')or(person == 'TWICE')or (person == 'Red Velvet') or (person == 'WINNER')):  ## 특정 경우, Person : 연예인
                #         sntns = """My One Pick Group. I'm big fan of them.""","""They are very good Artist.""","""They are WORLD CLASS! I love them."""
                #         response = random.choice(sntns).format(person)
                #     if ((person == 'Obama') or (person =='Steven Paul Jobs') or (person == 'Bill Gates')): ## 특정 경우, Person : 영향력 있는 인물.
                #         sntns = """He is my role model.""","""He deserves to be respected.""","""He lived a successful life."""
                #         response = random.choice(sntns).format(person)
                # if name is not None: ##person이 자신의 주변 인물, 친구
                #     sntns = """{}. What do you think of {}?""", """{}. Are you close with {}?""","""{}, Isn't {} close to you?"""
                #     response = random.choice(sntns).format(name,person)
                #     if(user_gender == 'Male' and person == name):
                #         sntns = """{} is very handsome.""","""{} is very cool guy.""","""{} is really gentle man"""
                #         response = response + random.choice(sntns).format(person)
                #     if(user_gender == 'Female' and person == name):
                #         sntns = """{} is the most beautiful woman I know.""","""{} is really lovely.""","""{} is very pretty."""
                #         response = response + random.choice(sntns).format(person)
                #     if user_occupation is not None:
                #         sntns = """Oh, you are a {}. How about {}?""","""From a {}'s point of view, what do you think about that {}?"""
                #         response = random.choice(sntns).format(person)
                # if movie is not None:
                #     sntns = """Was {} in that movie???""", """Is {} a movie star?""","""Is {} famous in Korea?? """
                #     response = response + random.choice(sntns).format(person)

##################################################################################
## Lee 11 : ActionSuggest// 제안
## 사용하는 슬롯 : state,food,movie,hobby,person,music,cloth,place,sports,job,book
##################################################################################

##################################################################################
## Lee 11 : ActionSuggest// 제안
## 사용하는 슬롯 : state,food,movie,hobby,person,music,cloth,place,sports,job,book
##################################################################################
class ActionSuggest(Action):
    def name(self) -> Text:
        return "action_suggest"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        state = tracker.get_slot("user_state")
        food = tracker.get_slot('food')
        movie = tracker.get_slot('movie')
        hobby = tracker.get_slot('hobby')
        person = tracker.get_slot('person')
        music = tracker.get_slot('music')
        cloth = tracker.get_slot('cloth')
        place = tracker.get_slot('place')
        sports = tracker.get_slot('sports')
        job = tracker.get_slot('job')
        book = tracker.get_slot('book')
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if state is None:  ## 이야기 주제에 따른 제안
            if food is not None:
                sntns = """Why don't you have {}?""", """{} is really good. I highly recommend it.""", """What about {}? 
                It's really good.""", """I recommend you to have {}.""", """How about {}?""", """{} would 
                be great. """
                response = random.choice(sntns).format(food)
            elif movie is not None:
                sntns = """{} is the best movie i've ever seen.""", """I recommend a movie titled {}.""", """Why don't 
                you go see a movie titled {}?""", """{} is the best.""", """{} is dope. """
                response = random.choice(sntns).format(movie)
            elif hobby is not None:
                sntns = """Time will fly if you start {}.""", """{} would be nice.""", """How about {} as a hobby?""", """I recommend {} for a hobby. """
                response = random.choice(sntns).format(hobby)
            elif person is not None:
                sntns = """{} is perfect for that.""", """{} is the right man for that.""", """How about {}?""", """I recommend you {}."""
                response = random.choice(sntns).format(person)
            elif music is not None:
                sntns = """{} is the best song I've ever heard.""", """Have you ever heard of the song {}? This song is dope!""", """The song {} will make feel up and up.""", """The song {} is the most popular song these days.""", """I recommend you {}."""
                response = random.choice(sntns).format(music)
            elif cloth is not None:
                sntns = """{} would good on you.""", """Why don't you try on {}?""", """I recommend you {}."""
                response = random.choice(sntns).format(cloth)
            elif place is not None:
                sntns = """How about {}?""", """What about {}?""", """Have you ever visited {}? I think you will like there.""", """I recommend you {}."""
                response = random.choice(sntns).format(place)
            elif sports is not None:
                sntns = """What about {}?""", """How about {}?""", """{} is really good.""", """I recommend you {}."""
                response = random.choice(sntns).format(sports)
            elif job is not None:
                sntns = """{} would be nice.""", """I recommend you a {}."""
                response = random.choice(sntns).format(job)
            elif book is not None:
                sntns = """{} is the best book I've ever read.""", """Have you ever read the book {}? You must read that!""", """The book {} will make feel up and up.""", """The book {book} is the most popular song these days.""", """I recommend you {}."""
                response = random.choice(sntns).format(book)
            else:
                response = '''I don't know what you are saying'''
            dispatcher.utter_message(" " + response)
        if state is not None:  ## 사용자 상태에 따른 제안
            if (state == "hungry"):
                food = tracker.get_slot('food')
                sntns = """Why don't you have {}?""", """{} is really good. I highly recommend it.""", """What about {}? It's really good.""", """I recommend you to have {}.""", """How about {}?""", """{} would be great. """
                response = random.choice(sntns).format(food)
            elif (state == "busy"):
                sntns = """I recommend you to take a rest.""", """Why don't you have a break time for a while?""", """Taking a rest for a second will make you more effective. """
                response = random.choice(sntns)
            elif (state == "tired"):
                sntns = """Maybe having a cup of coffee will help you.""", """Wash your face. It will work.""", """Why don't you try stretching? """
                response = random.choice(sntns)
            elif (state == "sick"):
                sntns = """Why don't you go to see a doctor and get some rest?""", """Have a pill which is effective for you now."""
                response = random.choice(sntns)
            elif state == ("sleepy"):
                sntns = """Why don't you get a nap now?""", """Getting a nap is needed to you right now."""
                response = random.choice(sntns)
            else:
                response = "Pardon me..?"
            dispatcher.utter_message(" " + response)
            return [SlotSet('user_state', None)]
##################################################################################
## Lee 12 : ActionWorry // 사용자 걱정에 관한 발화
## 사용하는 슬롯 : user_name,user_emotion, user_state, weather, user_hobby
##################################################################################


class ActionWorry(Action):
    def name(self) -> Text:
        return 'action_worry'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('user_name')
        emotion = tracker.get_slot('user_emotion')
        state = tracker.get_slot('user_state')
        weather = tracker.get_slot('weather')
        hobby = tracker.get_slot('user_hobby')

        a = tracker.latest_message.get('text')  ## User input 불러오기

        if emotion is not None:  ## 사용자 감정에 따른 걱정
            if (emotion == 'sad') or (emotion == 'lonely') or (emotion == 'depressed'):
                if name is None:
                    sntns = """I'm sorry to hear that. Are you Okay?""", """That's too bad. I'm worried about you.""", """Why do you feel that way?"""
                    response = random.choice(sntns)
                    if state is not None:  ## 사용자 감정도,상태도 Bad
                        if (state == 'tired') or (state == 'sick'):
                            sntns = """Your body and mind are both tired. Are you OK?""", """It could be because you're not feeling well. I'm worried about you.""",
                            """Bad things come at once. Everything will be fine."""
                            response = random.choice(sntns)
                if name is not None:
                    sntns = """ {}. I'm sorry. Cheer up.""", """{}. You look so bad. What happend?""", """{}. Why so serious? Are you Okay?""",
                    """{}. It's not who you are underneath, it's what you do that defines you."""
                    response = random.choice(sntns).format(name)

        if state is not None:  ##사용자 상태에 따른 걱정
            if (state == 'tired') or (state == 'sick'):
                if name is None:
                    sntns = """Are you {} now?""", """{}? I thought so. Get some rest.""", """Why are you so {}? It's going to be okay."""
                    response = random.choice(sntns).format(state)
                    if weather is not None:
                        if (weather == 'rainy') or (weather == 'snow') or (int(weather) < 0):
                            sntns = """It's really raining buckets outside today. Be careful not to catch a cold.""", """It is likely to snow today. Take care of your health.""",
                            """It's freezing today. You should dress warmly."""
                            response = random.choice(sntns)

                    if hobby is not None:
                        sntns = """Hobby activities are good, but be careful not to get hurt.""", """Don't take too long. Do your job first.""", """I think It's too expensive. May I help you?"""
                        response = random.choice(sntns)

                if name is not None:
                    sntns = """{}. I think you should get enough rest at home.""", """{}.I just care about you.""", """{}. I'm worried sick about you."""
                    response = random.choice(sntns).format(name)
            else:
                sntns = """How's your condition?""", """""Are you Okay now?""", """Do you want me to stay with you? if you want, I'll be there."""
                response = random.choice(sntns)
        else:
            sntns = """How's your condition?""", """""Are you Okay now?""", """Do you want me to stay with you? if you want, I'll be there."""
            response = random.choice(sntns)

        dispatcher.utter_message(response)
##################################################################################
## Lee 13 : ActionMusic // 음악 주제에 관한 발화
## 사용하는 슬롯 : user_name,user_emotion, music, weather
##################################################################################


class ActionMusic(Action):
    def name(self) -> Text:
        return 'action_music'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        music = tracker.get_slot('music')
        weather = tracker.get_slot('weather')


        MUSIC = [{"name": "Blues",
                  "info": "When millions of Africans were transported to America as slaves in the 18th and 19th centuries, their melodies and rhythms went with them. They knew that singing together made working easier, and it was in these work songs that African rhythms and melodies were preserved until slavery ended in 1865. "},
                 {"name": "Jazz",
                  "info": "Most African American musicians only played blues, but some played classical music as well and learned European harmony. Some even mixed European harmony with the rhythms and scales of blues, and it was from this mixture that 'jazz' was born. One of jazz's greatest musicians was the trumpet player Louis Armstrong, who helped to develop many styles of jazz."},
                 {"name": "Rythm and Blues",
                  "info": "As jazz was becoming more and more popular in the 1930s and 1940 s, another new genre was starting to develop. Many African Americans were professional blues musicians, but making money wasn't easy. They formed small bands and looked for work in cheap bars and clubs. But to get work, they had to attract audiences. Most young people who went to these places thought blues was old-fashioned, so the bands had to develop a new style, and what they created was 'rhythm and blues' (or R&B)."},
                 {"name": "Rock and Roll",
                  "info": "By the early 1950 s, another new genre called 'rock and roll (or 'rock'n'roll') was being created by musicians who could play both R&B and Western Swing, a popular style of country dance music. This new music was played on the same set of instruments as R&B - electric guitar, double bass and drums - with the guitarist often singing as well."},
                 {"name": "Rock",
                  "info": "By 1960, rock and roll was losing both record sales and artists. But many young people were still listening to their rock and roll records, and some began exploring the music's origins. Young musicians bought blues and R&B records, studied the music, and soon learned to play it. Before long, they were combining these older styles with rock and roll to create a new genre called 'rock music' or 'rock'."},
                 {"name": "Country",
                  "info": "Country music was one of the first genres of modern American popular music, and old-time music was its earliest style. It developed in the southeastern states of the USA as a mix of folk music from the British Isles, church music and African American blues. It was played on instruments like acoustic guitar, mandolin, autoharp, fiddle and the banjo. "},
                 {"name": "Soul",
                  "info": "Soul music is a genre of African American popular music that led to many later genres, from funk and dance music to hip hop and contemporary R&B. It developed in the USA in the late 1950s from African American church music called 'gospel music'. "},
                 {"name": "Dance",
                  "info": "In the mid-60s, US soul singer James Brown developed a new style of music called funk. In soul music the melody and lyrics are central, but in funk the rhythmic groove is central. The main stress in a funk rhythm is on the first beat of the bar, called 'the one', and a repeated pattern of drum beats and bass lines that begins on the one creates a groove."},
                 {"name": "Hip Hop",
                  "info": "Hip hop music, also known as rap music, is a genre of popular music developed in the United States by inner-city African Americans and Latino Americans in the Bronx borough of New York City in the 1970s. "},
                 {"name": "Disco",
                  "info": "In the early 70s nightclubs called discos were employing DJs to play dance tracks because it was cheaper than hiring a band. At first they played funk and up-tempo soul tracks, but in the mid-70s they started playing tracks with a new rhythm that was easier to dance to. It had a simple four-on-the-floor bass-drum beat with hi-hat on the offbeats. These songs were soon being played in discos all over the world, and a new genre called disco music was born. "},
                 {"name": "House",
                  "info": "In the early 1980s a new style of disco called house became popular in the dance clubs of New York and Chicago. Like disco, house tracks had catchy melodies with lyrics about going out, having fun or making love. It had a pounding four-on-the-floor disco beat, but in house music synthesizers were used more than drum kits and other traditional instruments, although piano was still used in most house tracks. "},
                 {"name": "Northern Soul",
                  "info": "Northern soul is a music and dance movement that emerged in Northern England and the English Midlands in the late 1960s from the British mod scene, based on a particular style of black American soul music, especially from the mid-1960s, with a heavy beat and fast tempo (100 bpm and above)[1][2] or American soul music from northern cities such as Detroit, Chicago and others."},
                 {"name": "Southern Soul",
                  "info": "Southern soul is a type of soul music that emerged from the Southern United States. The music originated from a combination of styles, including blues (both 12 bar and jump), country, early rock and roll, and a strong gospel influence that emanated from the sounds of Southern black churches. Bass guitar, drums, horn section, and gospel roots vocal are important to soul groove. This rhythmic force made it a strong influence in the rise of funk music. The terms 'Deep soul', 'Country soul', 'Downhome soul' and 'Hard soul' have been used synonymously with 'Southern soul'."},
                 {"name": "Ballad",
                  "info": "A ballad is a form of verse, often a narrative set to music. Ballads derive from the medieval French chanson balladée or ballade, which were originally 'dance songs'. Ballads were particularly characteristic of the popular poetry and song of Britain and Ireland from the later medieval period until the 19th century. "},
                 {"name": "Modal Jazz",
                  "info": "Modal jazz is jazz that makes use of musical modes often modulating among them instead of relying on one tonal center. Although precedents exist, modal jazz was crystallized as a theory by composer George Russell in his 1953 book Lydian Chromatic Concept of Tonal Organization."},
                 {"name": "Swing",
                  "info": "Swing music is a form of jazz that developed in the United States in the 1930s and 1940s. The name came from the emphasis on the off–beat, or weaker pulse. Swing bands usually featured soloists who would improvise on the melody over the arrangement. "},
                 {"name": "Western swing",
                  "info": "Western swing music is a subgenre of American country music that originated in the late 1920s in the West and South among the region's Western string bands. It is dance music, often with an up-tempo beat, which attracted huge crowds to dance halls and clubs in Texas, Oklahoma and California during the 1930s and 1940s until a federal war-time nightclub tax in 1944 contributed to the genre's decline."},
                 {"name": "Aria",
                  "info": "This is the moment in an opera where a lead character shows off his or her vocal chops. While it may serve to dramatically enhance the storyline, it’s really for the singer to milk the applause for all it’s worth."},
                 {"name": "Opera",
                  "info": "Opera features performers enacting dramatic plots via their singing either big melodies (arias, defined above) or semi-sung/spoken moments of dialogue, called recitative. Costumes, sets, staging and a full orchestra are involved. They come in all varieties, from the light comic operas to the most epic and time-consuming that goes on for hours. The most theatrical license by far exists for opera – the voice ultimately decides the casting."},
                 {"name": "Sonata",
                  "info": "A composition for solo instrument, and if it’s not for the piano, then it’s usually accompanied by the piano. It’s usually written in three or four moments. They take forever to memorize. So many notes."}
                 ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(MUSIC) - 1)

        if music is not None:
            user_music = [m for m in MUSIC if m.get("name").lower() == music.lower()]

            if user_music:
                response = user_music[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that music. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know that. How about {}?"""]
                response = sntns[rand].format(MUSIC[arand].get("name"))


        elif music is None:
            if weather is not None:  ## 날씨에 따른 음악 장르 제안
                if (weather == 'rainy'):
                    sntns = """On rainy days, I want to listen to sad ballad music.""", """On rainy days, I want to hear the acoustic guitar.""", """It's raining a lot, so let's listen to some exciting music."""
                    response = random.choice(sntns)
                elif (weather == 'snow'):
                    sntns = """Snow is a really good music topic.""", """Is there any music that comes to mind 'snow'?""", """It is the weather that I want to hear carol music."""
                    response = random.choice(sntns)
            else:
                response = "Pardon..?"
        else:
            response = "Pardon me..?"
        dispatcher.utter_message(response)
        return [SlotSet("music", None)]
##################################################################################
## Lee 14 : ActionCloth // 옷 주제에 관한 발화
## 사용하는 슬롯 : cloth, user_name, user_gender, user_emotion, Food, weather, user_occupation
##################################################################################

class ActionCloth(Action):

    def name(self) -> Text:
        return 'action_cloth'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('user_name')
        cloth = tracker.get_slot('cloth')

        CLOTHES = [
            {"name": "fashion",
             "info": "Fashion is a popular aesthetic expression at a particular time and place and in a specific context, especially in clothing, footwear, lifestyle, accessories, makeup, hairstyle, and body proportions."},
            {"name": "Haute couture",
             "info": "Haute couture is high-end fashion that is constructed by hand from start to finish, made from high-quality, expensive, often unusual fabric and sewn with extreme attention to detail and finished by the most experienced and capable sewers—often using time-consuming, hand-executed techniques."},
            {"name": "monochrome",
             "info": "In fashion terms, monochrome refers to an outfit or look that is only black and white in colour. It can be paired with accessories as well of the same tone."},
            {"name": "style",
             "info": "Style is the modification of fashion. It is the basic outline of any garment. Fashion changees but style change is constant. e.g.) Box pleated skirt, polo shirt"},
            {"name": "box pleat skirt",
             "info": "a skirt that has  a flat double pleat made by folding under the fabric on either side of it. pleat, plait - any of various types of fold formed by doubling fabric back upon itself and then pressing or stitching into shape. "},
            {"name": "polo shirt",
             "info": "A polo shirt is a form of shirt with a collar, a placket neckline with three buttons, and an optional pocket. Polo shirts should be buttoned to the top and are usually short sleeved; they were used by polo players originally in India in 1859 and in Great Britain during the 1920s."},
            {"name": "Fad",
             "info": "A fad, trend, or craze is any form of collective behavior that develops within a culture, a generation or social group in which a group of people enthusiastically follow an impulse for a finite period."},
            {"name": "blouse",
             "info": "a piece of clothing for women and girls that is a bit formal. It is sometimes made of finer materials like silk."},
            {"name": "halter top",
             "info": "a top worn by women that ties around the neck and does not have any sleeves."},
            {"name": "cargo pants",
             "info": "a style of loose fitting pants with several large pockets (especially on the side of the legs near the knees)"},
            {"name": "Sari",
             "info": "The sari (often spelled ‘saree’) is a garment traditionally worn in India, Sri Lanka, Pakistan, Bangladesh and Nepal. Though mostly worn by women in modern fashion, the sari is a unisex piece of clothing. It can be an heirloom passed down through generations, or a purely functional garment worn everyday."},
            {"name": "Hanbok",
             "info": "The hanbok in South Korea (or Joseon-oth in North Korea) is the traditional Korean dress. It is characterized by vibrant colors and simple lines without pockets. Although the term literally means ‘Korean clothing’, hanbok usually refers specifically to clothing of the Joseon period, and is worn as semi-formal or formal wear during festivals and celebrations."},
            {"name": "Kilt",
             "info": "A kilt is a knee-length skirt-like garment with pleats at the back, originating in the traditional dress of Gaelic men and boys in the Scottish Highlands. Its first wear was recorded in the 16th century as the ‘great kilt’, and the smaller, more modern kilt emerged in the 18th century. It’s only since the 19th century that the kilt has become associated with the wider culture of Scotland and more broadly with Gaelic heritage."},
            {"name": "Agbada",
             "info": "The agbada is one of the names for a flowing wide-sleeved robe worn by men in West Africa and parts of North Africa. The name ‘agbada’ comes from Yoruba language but is known by various names depending on the ethnic group. The garment is usually decorated with intricate embroidery and is worn on special religious or ceremonial occasions. "},
            {"name": "Huipil",
             "info": "A huipil is the most common traditional garment worn by indigenous women from central Mexico to Central America. A loose-fitting tunic, general made from several pieces of woven fabric, a huipil is often worn with a blue morga, a skirt with an embroidered seam to join it in the middle."},
            {"name": "Lederhosen",
             "info": "Lederhosen are a traditional male outfit made from leather and include shorts that hit just above the knee. Lederhosen grew in popularity during the eighteenth century and were often worn for horseback riding, performing hard labor, and other physical activities. After the nineteenth century, they became more popular as a costume or for everyday wear."},
            {"name": "Poncho",
             "info": "A poncho is a waterproof top that covers the upper body and usually has a hood to protect the head. Ponchos date back to the pre-Incan times and are decorated with art patterns traditionally found in South American cultures. Diagonal designs are very popular. Ponchos are also brightly colored."},
            {"name": "teddy coat",
             "info": "Teddy bear coats may just qualify as the coziest part of the fall. Slightly oversize and oh-so fuzzy, these toppers are the perfect outwear staple that feel as soft, warm, and plush as they look."},
            {"name": "Pantone",
             "info": "Pantone LLC is best known for its Pantone Matching System (PMS), a proprietary color space used in a variety of industries, notably graphic design, fashion design, product design, printing and manufacturing and supporting the management of color from design to production, in physical and digital formats, among coated and uncoated materials, cotton, polyester, nylon and plastics."},
            {"name": "Color of the Year",
             "info": "Since 2000, the Pantone Color Institute has declared a particular color 'Color of the Year'.\nThe colour of this year, 2020, is classic blue, Pantone 19-4052, #0F4C81"},
            {"name": "trend",
             "info": "Trend generally denotes what is popular at a specific point in time while fashion signifies popular and freshest styles of hair, clothing, decoration, or even behavior. \nFashion Trends in 2021 : Jackets, skirts, dresses and even tops – garments made of leather have been all the rage for a few years now and have become an integral part of fashionable women's wardrobes. From head to toe, leather outfits are at the top of the list for the 2021 fashion trends."},
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(CLOTHES) - 1)

        response = "Sorry...?"

        if cloth is None:
            # default
            if name is not None:
                sntns = """{}. Do you want to go shopping?""", """{}. I'm going to buy clothes, so please go and take a look at them.""", """{}. What do you think of these shoes?"""
                response = random.choice(sntns).format(name)
            else:
                sntns = """Oh. It's good for you.""", """Orange goes good with you!""", """I think that'll be fine."""
                response = random.choice(sntns)
        if cloth is not None:
            user_cloth = [m for m in CLOTHES if m.get("name").lower() == cloth.lower()]

            if user_cloth:
                response = user_cloth[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know what that is. How about {}?"""]
                response = sntns[rand].format(CLOTHES[arand].get("name"))
        dispatcher.utter_message(response)
        return [SlotSet("cloth", None)]

        # if name is not None:  ## 성별에 따라 발화
        #     if (gender == 'male') or (gender == 'man'):
        #         sntns = """{}, you look gentle today""", """{}, you look stylish today.""", """{}.You are neatly dressed."""
        #         response = random.choice(sntns).format(name)
        #     if (gender == 'female') or (gender == 'woman'):
        #         sntns = """{}. You have very beautiful hair.""", """Wow. {}. What's a pretty dress.""", """{}. You have good taste in clothes."""
        #         response = random.choice(sntns)
        # if weather is not None:  ## 날씨에 따른 의상 제안
        #     if (weather == 'rainy') or (weather == 'snow'):
        #         sntns = """Wear it comfortably.""", """Wasn't it cold? You should dress warmly.""", """Wear bright clothes for your safety."""
        #         response = random.choice(sntns)
        # if (cloth == 'watch') or (cloth == 'necklace') or (cloth == 'earring'):
        #     sntns = """What a nice accessory.""", """It is really shiny,""", """You look really classy."""
        #     response = random.choice(sntns)
        # if (cloth == 'pants') or (cloth == 'skirt'):
        #     sntns = """It really suits you""", """I think It is best fit.""", """That suit you well because you have long legs."""
        #     response = random.choice(sntns)
        # if (cloth == 'sneakers') or (cloth == 'shoes') or (cloth == 'boots'):
        #     sntns = """How's the size? OK?""", """I think that black one is better.""", """The outfit suits you well."""
        #     response = random.choice(sntns)
        # if food is not None:  ## 음식에 따라 의상 주의 발화.
        #     sntns = """Be careful not to spill it on your clothes.""", """Do you need an apron?""", """Be careful not to splash on white clothes."""
        #     response = random.choice(sntns)
        # if job is not None:
        #     sntns = """Are you dressed to suit your job?""", """What are you wearing now?""", """Change your clothes neatly."""
        #     response = random.choice(sntns)


######################################################################################################
class ActionChangeTopic(Action):
    def name(self) -> Text:
        return 'action_change_topic'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        a = tracker.latest_message.get('text')  ## User input 불러오기
        sntns = """Let's talk about something else.""", """Let's move on to another topic.""", """I have no interest in that topic."""
        response = random.choice(sntns)
        dispatcher.utter_message(" " + response)
##################################################################################
## Lee 15 : ActionSport // 운동 주제에 관한 발화
## 사용하는 슬롯 : sport, user_name,user_emotion, user_state, weather
##################################################################################

SPORT = [
    {"name": "badminton",
     "info": "Badminton is a racquet sport played using racquets to hit a shuttlecock across a net. Although it may be played with larger teams, the most common forms of the game are 'singles' (with one player per side) and 'doubles' (with two players per side). "},
    {"name": "cricket",
     "info": "Cricket involves sprinting between wickets and running to stop balls, as well as bowling and throwing. Health benefits include: Endurance and stamina Balance and coordination Physical fitness Improving hand-eye coordination."},
    {"name": "boxing",
     "info": "Boxing is a combat sport in which two people, usually wearing protective gloves, throw punches at each other for a predetermined amount of time in a boxing ring."},
    {"name": "curling",
     "info": "Curling is a sport in which players slide stones on a sheet of ice toward a target area which is segmented into four concentric circles. It is related to bowls, boules and shuffleboard."},
    {"name": "tennis",
     "info": "Tennis is a racket sport that can be played individually against a single opponent (singles) or between two teams of two players each (doubles)."},
    {"name": "skateboarding",
     "info": "Skateboarding is an action sport that involves riding and performing tricks using a skateboard, as well as a recreational activity, an art form, an entertainment industry job, and a method of transportation."},
    {"name": "hockey",
     "info": "Hockey is a sport in which two teams play against each other by trying to manoeuvre a ball or a puck into the opponent's goal using a hockey stick. There are many types of hockey such as bandy, field hockey, ice hockey and rink hockey."},
    {"name": "figure skating",
     "info": "Figure skating is a sport in which individuals, pairs, or groups perform on figure skates on ice. It was the first winter sport to be included in the Olympic Games, when contested at the 1908 Olympics in London."},
    {"name": "yoga",
     "info": "Yoga is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India. Yoga is one of the six Āstika (orthodox) schools of Hindu philosophical traditions."},
    {"name": "fencing",
     "info": "Fencing is a group of three related combat sports. The three disciplines in modern fencing are the foil, the épée, and the sabre (also saber); winning points are made through the weapon's contact with an opponent."},
    {"name": "archery",
     "info": "Archery is the art, sport, practice, or skill of using a bow to shoot arrows.[1] The word comes from the Latin arcus for bow.[2] Historically, archery has been used for hunting and combat. In modern times, it is mainly a competitive sport and recreational activity. "},
    {"name": "gymnastics",
     "info": "Gymnastics is a sport that includes physical exercises requiring balance, strength, flexibility, agility, coordination, and endurance. The movements involved in gymnastics contribute to the development of the arms, legs, shoulders, back, chest, and abdominal muscle groups."},
    {"name": "basketball",
     "info": "Basketball is a team sport in which two teams, most commonly of five players each, opposing one another on a rectangular court, compete with the primary objective of shooting a basketball (approximately 9.4 inches (24 cm) in diameter) through the defender's hoop (a basket 18 inches (46 cm) in diameter mounted 10 feet (3.048 m) high to a backboard at each end of the court) while preventing the opposing team from shooting through their own hoop. "},
    {"name": "baseball",
     "info": "Baseball is a bat-and-ball game played between two opposing teams who take turns batting and fielding. The game proceeds when a player on the fielding team, called the pitcher, throws a ball which a player on the batting team tries to hit with a bat. "},
    {"name": "rugby",
     "info": "Rugby football is a collective name for the family of team sports of rugby union and rugby league, as well as the earlier forms of football from which both games, Association football, Australian rules football, and Gridiron football evolved."},
    {"name": "cycling",
     "info": "Cycling, also called bicycling or biking, is the use of bicycles for transport, recreation, exercise or sport. People engaged in cycling are referred to as 'cyclists', 'bicyclists', or 'bikers'. Apart from two-wheeled bicycles, 'cycling' also includes the riding of unicycles, tricycles, quadracycles, recumbent and similar human-powered vehicles (HPVs)."},
    {"name": "running",
     "info": "Running is a method of terrestrial locomotion allowing humans and other animals to move rapidly on foot. Running is a type of gait characterized by an aerial phase in which all feet are above the ground (though there are exceptions)."},
    {"name": "table tennis",
     "info": "Table tennis, also known as ping-pong and whiff-whaff, is a sport in which two or four players hit a lightweight ball, also known as the ping-pong ball, back and forth across a table using small rackets. The game takes place on a hard table divided by a net."},
    {"name": "climbing",
     "info": "Climbing is the activity of using one's hands, feet, or any other part of the body to ascend a steep topographical object. It is done for locomotion, recreation and competition, and within trades that rely on ascension; such as emergency rescue and military operations. It is done indoors and out, on natural and man-made structures."},
    {"name": "football",
     "info": "Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. Unqualified, the word football normally means the form of football that is the most popular where the word is used. Sports commonly called football include association football (known as soccer in some countries); gridiron football (specifically American football or Canadian football); Australian rules football; rugby football (either rugby union or rugby league); and Gaelic football."}
]
class ActionSport(Action):
    def name(self) -> Text:
        return 'action_sport'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sport = tracker.get_slot('sports')
        name = tracker.get_slot('user_name')

        rand = random.randint(0, 2)
        arand = random.randint(0, len(SPORT) - 1)

        if sport is not None:
            user_sport = [m for m in SPORT if m.get("name").lower() == sport.lower()]

            if user_sport:
                response = user_sport[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know what that is. How about {}?"""]
                response = sntns[rand].format(SPORT[arand].get("name"))

        elif sport is None:  ##default
            if name is not None:
                sntns = """{}.What's your favorite sports?""", """{}.What did you say?""", """{}? What's that?"""
                response = random.choice(sntns).format(name)
            else:
                sntns = """What Sports?""", """It's so hard activity.""", """I don't know that sport"""
                response = random.choice(sntns)

        else:
            response = "Sorry..?"

        dispatcher.utter_message(response)
        return [SlotSet("sports", None)]

##################################################################################
## Lee 16 : ActionJob // 직업 주제에 관한 발화
## 사용하는 슬롯 : job, user_occupation, user_name, user_gender
##################################################################################

class ActionJob(Action):
    def name(self) -> Text:
        return 'action_job'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        job = tracker.get_slot('job')
        gender = tracker.get_slot('user_gender')



        JOB = [
            {"name": "software developer",
             "info": "Software developers typically do the following: Analyze users' needs and then design, test, and develop software to meet those needs. Recommend software upgrades for customers' existing programs and systems. Design each piece of an application or system and plan how the pieces will work together."},
            {"name": "dentist",
             "info": "A dentist, also known as a dental surgeon, is a surgeon who specializes in dentistry, the diagnosis, prevention, and treatment of diseases and conditions of the oral cavity. The dentist's supporting team aids in providing oral health services. The dental team includes dental assistants, dental hygienists, dental technicians, and sometimes dental therapists."},
            {"name": "physician assistant",
             "info": "A physician assistant in the United States, Canada and other select countries or physician associate in the United Kingdom (PA) is an Advanced Practice Provider (APP). PAs are medical professionals who diagnose illness, develop and manage treatment plans, prescribe medications, and often serve as a patient’s principal healthcare provider."},
            {"name": "orthodontist",
             "info": "Orthodontists help with crooked teeth, but they assist patients with other issues as well. These include overbites and underbites, crossbites, spaces between teeth, overcrowding of teeth, and the treatment of temporomandibular disorders (TMD). Additional problems with the jaw also need to be treated by an orthodontist."},
            {"name": "nurse",
             "info": "Nursing is a profession within the health care sector focused on the care of individuals, families, and communities so they may attain, maintain, or recover optimal health and quality of life. Nurses may be differentiated from other health care providers by their approach to patient care, training, and scope of practice. Nurses practice in many specialties with differing levels of prescription authority."},
            {"name": "statistician",
             "info": "A statistician is a person who works with theoretical or applied statistics. The profession exists in both the private and public sectors. It is common to combine statistical knowledge with expertise in other subjects, and statisticians may work as employees or as statistical consultants."},
            {"name": "physician",
             "info": "A physician (American English), medical practitioner (Commonwealth English), medical doctor, or simply doctor, is a professional who practises medicine, which is concerned with promoting, maintaining, or restoring health through the study, diagnosis, prognosis and treatment of disease, injury, and other physical and mental impairments."},
            {"name": "oral and maxillofacial surgeon",
             "info": "Oral and maxillofacial surgery is a surgical specialty focusing on reconstructive surgery of the face, facial trauma surgery, the oral cavity, head and neck, mouth, and jaws, as well as facial cosmetic surgery."},
            {"name": "veterinarian",
             "info": "A veterinarian (vet), also known as a veterinary surgeon or veterinary physician, is a professional who practices veterinary medicine by treating diseases, disorders, and injuries in non-human animals."},
            {"name": "IT manager",
             "info": "An IT manager is someone who is responsible for the overall performance of a company's electronic networks and leads the IT department in fulfilling the organization’s information systems requirements. Focusing on a company's in-house computer networks may involve selecting the hardware and software that is needed for the network, updating internal servers, or looking at other electronic support systems that can improve worker's productivity."},
            {"name": "mathematician",
             "info": "A mathematician is someone who uses an extensive knowledge of mathematics in their work, typically to solve mathematical problems. Mathematicians are concerned with numbers, data, quantity, structure, space, models, and change."},
            {"name": "physical therapist",
             "info": "Physical therapists evaluate and record a patient's progress. Physical therapists help injured or ill people improve movement and manage pain. They are often an important part of preventive care, rehabilitation, and treatment for patients with chronic conditions, illnesses, or injuries."},
            {"name": "optometrist",
             "info": "Optometry is a health care profession that involves examining the eyes and applicable visual systems for defects or abnormalities as well as the correction of refractive error with glasses or contact lenses and treatment of eye diseases."},
            {"name": "pediatrician",
             "info": "Pediatrics is the branch of medicine that involves the medical care of infants, children, and adolescents. The American Academy of Pediatrics recommends people be under pediatric care through the age of 21 (though usually only minors are required to be under pediatric care). In the United Kingdom, pediatrics covers patients until age 18."},
            {"name": "web developer",
             "info": "A web developer is a programmer who specializes in, or is specifically engaged in, the development of World Wide Web applications using a client–server model. The applications typically use HTML, CSS and JavaScript in the client, PHP, ASP.NET (C#), Python, Go or Java in the server, and http for communications between client and server. A web content management system is often used to develop and maintain web applications."},
            {"name": "financial manager",
             "info": "A Finance Manager distributes the financial resources of a company, is responsible for the budget planning, and supports the executive management team by offering insights and financial advice that will allow them to make the best business decisions for the company."},
            {"name": "psychologist",
             "info": "A psychologist is a person who studies normal and abnormal mental states, perceptual, cognitive, emotional, and social processes and behavior by experimenting with, and observing, interpreting, and recording how individuals relate to one another and to their environments."},
            {"name": "database administrator",
             "info": "Database administrators (DBAs) use specialized software to store and organize data. The role may include capacity planning, installation, configuration, database design, migration, performance monitoring, security, troubleshooting, as well as backup and data recovery."},
            {"name": "pilot",
             "info": "Pilots fly and operate aircraft like airplanes and helicopters for airlines, private corporations, law enforcement agencies and the military. They also prepare the aircraft for flight, which includes ensuring there are no mechanical defects with the aircraft, verifying that scheduled maintenance is done and any repairs are complete, and checking the route of flight as well as departure, destination and alternate airports to make sure the flight is safe for weather conditions."},
            {"name": "accountant",
             "info": "An accountant is a person who keeps or inspects financial records. They're numbers people who excel at organization and detail-oriented work. Since they deal with money – sometimes significant amounts of it – accountants must also possess a high degree of integrity. And because they're constantly interacting with clients, accountants should be effective communicators."}
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(JOB) - 1)

        if job is not None:
            user_job = [m for m in JOB if m.get("name").lower() == job.lower()]

            if user_job:
                response = user_job[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that job. What about {}?""",
                         """Sorry, I'm not sure about that job. I recommend you to search about {}.""",
                         """Sorry, I don't know that. How about {}?"""]
                response = sntns[rand].format(JOB[arand].get("name"))

        elif job is None:
            if gender is not None:  ## 성별에 따른 직업 발화.
                if (gender == 'Man') or (gender == 'Male'):
                    sntns = """What is a good job for a man?""", """How about football player.""", """Why don't you try acting? You are so hansome!"""
                    response = random.choice(sntns)

                if (gender == 'Woman') or (gender == 'Female'):
                    sntns = """How about nurse? It's nice.""", """Why don't you prepare a stewardess?""", """Ballerinas are very beautiful. How about you?"""
                    response = random.choice(sntns)

            else:  ## default - > job is None
                sntns = """I was wondering if you could give me some career advise.""", """"I don't know that job.""", """I've never heard of it."""
                response = random.choice(sntns)

        else:
            response = "One more please"
        dispatcher.utter_message(response)
        return [SlotSet('job', None)]


##################################################################################
## Lee 17 : ActionBook // 책 주제에 관한 발화
## 사용하는 슬롯 : book, user_emotion, user_name , user_state, food
##################################################################################
class ActionBook(Action):
    def name(self) -> Text:
        return 'action_book'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        book = tracker.get_slot('book')
        name = tracker.get_slot('user_name')
        state = tracker.get_slot('user_state')
        emotion = tracker.get_slot('user_emotion')
        food = tracker.get_slot('food')
        a = tracker.latest_message.get('text')  ## User input 불러오기
        BOOK = [
            {"name": "Anna Karenina",
             "info": "Written by Russian novelist Leo Tolstoy, the eight-part towering work of fiction tells the story of two major characters: a tragic, disenchanted housewife, the titular Anna, who runs off with her young lover, and a lovestruck landowner named Konstantin Levin, who struggles in faith and philosophy."},
            {"name": "To Kill a Mockingbird",
             "info": "To Kill a Mockingbird was published in 1960 and became an immediate classic of literature. The novel examines racism in the American South through the innocent wide eyes of a clever young girl named Jean Louise (“Scout”) Finch. Its iconic characters, most notably the sympathetic and just lawyer and father Atticus Finch, served as role models and changed perspectives in the United States at a time when tensions regarding race were high. "},
            {"name": "The Great Gatsby",
             "info": "The novel is told from the perspective of a young man named Nick Carraway who has recently moved to New York City and is befriended by his eccentric nouveau riche neighbor with mysterious origins, Jay Gatsby. The Great Gatsby provides an insider’s look into the Jazz Age of the 1920s in United States history while at the same time critiquing the idea of the “American Dream.”"},
            {"name": "Don Quixote",
             "info": "Miguel de Cervantes’s Don Quixote, perhaps the most influential and well-known work of Spanish literature, was first published in full in 1615. The novel, which is very regularly regarded as one of the best literary works of all time, tells the story of a man who takes the name “Don Quixote de la Mancha” and sets off in a fit of obsession over romantic novels about chivalry to revive the custom and become a hero himself. "},
            {"name": "Jane Eyre",
             "info": "Jane Eyre provided a story of individualism for women. The novel’s eponymous character rises from being orphaned and poor into a successful and independent woman. The work combines themes from both Gothic and Victorian literature, revolutionizing the art of the novel by focusing on the growth in Jane’s sensibility with internalized action and writing."},
            {"name": "Beloved",
             "info": "Toni Morrison’s 1987 spiritual and haunting novel Beloved tells the story of an escaped slave named Sethe who has fled to Cincinnati, Ohio, in the year 1873. The novel investigates the trauma of slavery even after freedom has been gained, depicting Sethe’s guilt and emotional pain after having killed her own child, whom she named Beloved, to keep her from living life as a slave. "},
            {"name": "Mrs. Dalloway",
             "info": "Virginia Woolf’s Mrs. Dalloway describes exactly one day in the life of a British socialite named Clarissa Dalloway. Using a combination of a third-person narration and the thoughts of various characters, the novel uses a stream-of-consciousness style all the way through. The result of this style is a deeply personal and revealing look into the characters’ minds, with the novel relying heavily on character rather than plot to tell its story."},
            {"name": "One Hundred Years of Solitude",
             "info": "Written by Gabriel Garcia Marquez, the novel tells the story of the rise and fall of the mythical town of Macondo through the history of the Buendía family. It is a rich and brilliant chronicle of life and death, and the tragicomedy of humankind. In the noble, ridiculous, beautiful, and tawdry story of the Buendía family, one sees all of humanity, just as in the history, myths, growth, and decay of Macondo, one sees all of Latin America."},
            {"name": "Lolita",
             "info": "Lolita by Vladimir Nabokov. The book is internationally famous for its innovative style and infamous for its controversial subject: the protagonist and unreliable narrator, middle aged Humbert Humbert, becomes obsessed and sexually involved with a twelve-year-old girl named Dolores Haze."},
            {"name": "Hamlet",
             "info": "The Tragedy of Hamlet, Prince of Denmark, or more simply Hamlet, is a tragedy by William Shakespeare, believed to have been written between 1599 and 1601. The play, set in Denmark, recounts how Prince Hamlet exacts revenge on his uncle Claudius, who has murdered Hamlet's father, the King, and then taken the throne and married Gertrude, Hamlet's mother. "},
            {"name": "Pride and Prejudice",
             "info": "Pride and Prejudice by Jane Austen. The book is narrated in free indirect speech following the main character Elizabeth Bennet as she deals with matters of upbringing, marriage, moral rightness and education in her aristocratic society. Though the book's setting is uniquely turn of the 19th century, it remains a fascination of modern readership, continuing to remain at the top of lists titled 'most loved books of all time', and receiving considerable attention from literary critics. "},
            {"name": "Invisible Man",
             "info": "Invisible Man by Ralph Ellison. The novel addresses many of the social and intellectual issues facing African-Americans in the early twentieth century, including black nationalism, the relationship between black identity and Marxism, and the reformist racial policies of Booker T. Washington, as well as issues of individuality and personal identity."},
            {"name": "Great Expectations",
             "info": "Great Expectations by Charles Dickens. Great Expectations is written in the genre of 'bildungsroman' or the style of book that follows the story of a man or woman in their quest for maturity, usually starting from childhood and ending in the main character's eventual adulthood. Great Expectations is the story of the orphan Pip, writing his life from his early days of childhood until adulthood and trying to be a gentleman along the way."},
            {"name": "The Old Man and the Sea",
             "info": "The Old Man and the Sea by Ernest Hemingway. The Old Man and the Sea is one of Hemingway's most enduring works. Told in language of great simplicity and power, it is the story of an old Cuban fisherman, down on his luck, and his supreme ordeal — a relentless, agonizing battle with a giant marlin far out in the Gulf Stream. Here Hemingway recasts, in strikingly contemporary style, the classic theme of courage in the face of defeat, of personal triumph won from loss. "},
            {"name": "Lord of the Flies",
             "info": "Lord of the Flies by William Golding. Lord of the Flies discusses how culture created by man fails, using as an example a group of British schoolboys stuck on a deserted island who try to govern themselves, but with disastrous results. Its stances on the already controversial subjects of human nature and individual welfare versus the common good."},
            {"name": "Emma",
             "info": "Emma by Jane Austen. Before she began the novel, Austen wrote, 'I am going to take a heroine whom no-one but myself will much like.' In the very first sentence she introduces the title character as 'Emma Woodhouse, handsome, clever, and rich.' Emma, however, is also rather spoiled; she greatly overestimates her own matchmaking abilities; and she is blind to the dangers of meddling in other people's lives and is often mistaken about the meanings of others' actions."},
            {"name": "Animal Farm",
             "info": "Animal Farm is a dystopian novella by George Orwell. Published in England on 17 August 1945, the book reflects events leading up to and during the Stalin era before World War II. Orwell, a democratic socialist and a member of the Independent Labour Party for many years, was a critic of Joseph Stalin and was suspicious of Moscow-directed Stalinism after his experiences with the NKVD during the Spanish Civil War."},
            {"name": "Frankenstein",
             "info": "Frankenstein by Mary Shelley. Frankenstein was published the next year and become the rage of London. In the generations since, the story of Victor Frankenstein and the monster he created has been read by millions all over the world. It has inspired hundreds of imitations, but it has never been equaled for its masterful manipulation of the elements of horror and suspense."},
            {"name": "The Handmaid's Tale",
             "info": "The Handmaid's Tale is a feminist dystopian novel, a work of science fiction or speculative fiction, written by Canadian author Margaret Atwood and first published by McClelland and Stewart in 1985. Set in the near future, in a totalitarian theocracy which has overthrown the United States government, The Handmaid's Tale explores themes of women in subjugation and the various means by which they gain agency."},
            {"name": "Normal People",
             "info": "Normal People is a 2018 novel by Irish author Sally Rooney. It is her second novel to be published, after Conversations with Friends (2017). It became a best-seller in the US, selling almost 64,000 copies in hardcover in its first four months of release. A critically acclaimed and Emmy nominated television adaptation aired from April 2020."},
        ]
        rand = random.randint(0, 2)
        arand = random.randint(0, len(BOOK) - 1)
        if book is not None:  ##default
            user_book = [m for m in BOOK if m.get("name") == book]
            if user_book:
                response = user_book[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that book. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know what that is. How about {}?"""]
                response = sntns[rand].format(BOOK[arand].get("name"))
        #             sntns = """{}. Have you read the {}?""", """{}. {} is really interesting.""", """{}. """, """{}.Do you know the story of the {}?"""
        #             response = random.choice(sntns).format(name, book)
        #             ## 특정 책의 장르에 따른 추가 발화.
        #             if (book == 'Harry Potter') or (book == 'The Lord of the rings') or (
        #                     book == 'Chronicles of Narnia'):
        #                 sntns = """Oh. I like fantasy novels. It's awesome.""", """The book was made into a movie. You know?""", """My imagination was aflame by the book's."""
        #                 response = response + random.choice(sntns)
        #             if (book == 'Papillon') or (book == 'Troisieme humanite') or (book == "Gulliver's Travels"):
        #                 sntns = """I love SF. What do you think?""", """It is my favorite genre of novel.""", """What will happen in the future?"""
        #                 response = response + random.choice(sntns)
        #             if (book == 'Essays in love') or (book == 'Kiss and tell') or (book == 'Pride and Prejudice'):
        #                 sntns = """My hobby is reading romance novels.""", """When I read it. It makes me flutter.""", """It story was wonderful. I won't forget."""
        #                 response = response + random.choice(sntns)
        #
        #     if emotion is not None: ##감정에 따른 독서 제안 발화
        #         if (emotion == 'lonely') or (emotion == 'bored') or (emotion == 'depressed'):
        #             sntns = """How about reading a funny book?""", """Reading is the aliment for the mind.""","""It could be because the book ends in a sad ending."""
        #             response = random.choice(sntns)
        #     if state is not None: ## 상태에 따른 제안 발화
        #         if (state == 'busy'):
        #             sntns = """Why don't you take it easy and read a book?""", """Read the book. You need to be more relaxed.""", """I will recommend 'Tired or not Happy' to you. It is really nice book."""
        #             response = random.choice(sntns)
        #         if (state == 'tired') or (state == 'sleepy'):
        #             sntns = """In that case, I recommend you to fall asleep while reading a book.""","""Is the story too boring?""","""First, drink a cup of coffee. Then read it"""
        #             response = random.choice(sntns)
        #     if food is not None: ## 음식 정보에 관한 책
        #         sntns = """I know a book with a {} recipe.""","""It is fantastic to read while eating the {}.""","""There is a famous book with good {] recipes."""
        #         response = random.choice(sntns)
        # elif name is None: ##  name X
        #     if book is not None:
        #         sntns = """Have you read the {}?""","""{} is really interesting.""","""Do you know the story of the {}?"""
        #         response = random.choice(sntns).format(book)
        # if book is None: ## book is None
        #     sntns = """I hate reading books.""","""I think that reading books is really boring.""","""I don't like it""","""What Book?"""
        #     response = random.choice(sntns)
        else:
            response = "hmm..?"
        dispatcher.utter_message(" " + response)
##################################################################################
## Lee 18 : ActionAskBack // 재질문에 관한 발화
## 사용하는 슬롯 : user_name, user_emotion, user_occupation, user_state, job,food,movie,book,
##################################################################################
class ActionAskBack(Action):
    def name(self) -> Text:
        return 'action_ask_back'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        job = tracker.get_slot('job')
        food = tracker.get_slot('food')
        movie = tracker.get_slot('movie')
        book = tracker.get_slot('book')
        user_occupation = tracker.get_slot('user_occupation')
        name = tracker.get_slot('user_name')
        emotion = tracker.get_slot('user_emotion')
        state = tracker.get_slot('user_state')
        a = tracker.latest_message.get('text')  ## User input 불러오기
        ### 공통적으로 재질문
        if name is not None:
            sntns = """{}. I didn't hear that.""", """{}. What did you say?""", """{}.Tell me one more time."""
            response = random.choice(sntns).format(name)
            ## 전 질문의 주제에 따라 재질문
            if emotion is not None:
                sntns = """How do you feel? {}?""", """{}? but I didn't hear you well.""", """{}? Right?"""
                response = random.choice(sntns).format(emotion)
            if food is not None:
                sntns = """What food?""", """What kind of food?""", """What did you say just now?"""
                response = random.choice(sntns)
            if movie is not None:
                sntns = """What movie?""", """Sorry.What kind of a movie is it?""", """Did you just say about movie?"""
                response = random.choice(sntns)
            if book is not None:
                sntns = """{}? Right?""", """Did you just talk about the {}?""", """What's that {}?"""
                response = random.choice(sntns)
            if job is not None:
                sntns = """What job?""", """Sorry. Please one more explain that job.""", """I'm sorry. I was thinking about something else."""
                response = random.choice(sntns)
            if state is not None:
                sntns = """What did you say? hungry? sick?""", """Busy? I didn't hear that.""", """Sorry. tell me one more. Are you okay?"""
                response = random.choice(sntns)
            if user_occupation is not None:
                sntns = """What did you just say about your job?""", """What's your occupation""", """Tell me again what you just said. Sorry."""
                response = random.choice(sntns)
        elif name is None:
            sntns = """Sorry. Please say it again""", """You said what?""", """Excuse me?""", """What's your name?"""
            response = random.choice(sntns)
        ## default
        else:
            sntns = """Pardon me?""", """What did you just say?""", """What?"""
            response = random.choice(sntns)
        dispatcher.utter_message(" " + response)
######################################################################################################
class ActionConcern(Action):
    def name(self) -> Text:
        return "action_concern"
    def run(self, dispatcher, tracker, domain):
        user_name = tracker.get_slot("user_name")
        user_age = tracker.get_slot("user_age")
        user_gender = tracker.get_slot("user_gender")
        symptom = tracker.get_slot("symptom")
        a = tracker.latest_message.get('text')  ## User input 불러오기
        if symptom == "sore throat" or symptom == "coughing":
            sntns = """The pear juice is good for the sore throat.""", """Do you have fever?""", """Did you sleep with the air conditioner?"""
            response = random.choice(sntns)
        elif symptom == "head cold":
            sntns = """It's not good to blow your nose too much.""", """Do you have any allergy symptoms?""", """Did you sleep with the air conditioner?"""
            response = random.choice(sntns)
        elif symptom == "headache":
            sntns = """How about taking a headache medicine?""", """It's best to sleep for headaches.""", """Is everything okay except for a headache?"""
            response = random.choice(sntns)
        elif symptom == "having a fever" or symptom == 'fever':
            sntns = """If the fever is over 38 degrees, you have to go to the hospital unconditionally.""", """Do you have any cough symptoms? Then go to the hospital right away.""",
            """Do you have antipyretic? If you have, you must eat."""
            response = random.choice(sntns)
        elif symptom == "have trouble sleeping" or symptom == "insomnia":
            sntns = """If you have insomnia, you shouldn't use your smartphone when you sleep.""", """These days, insomnia can be overcome with simple psychotherapy.""",
            """How about listening to ASRM?"""
            response = random.choice(sntns)
        elif symptom == "pain in my stomach" or symptom == "stomachache":  # 배아픔
            sntns = """Bananas and apples are good for stomach aches.""", """You may have a stomachache because you ate something spicy."""
            response = random.choice(sntns)
        elif symptom == "sneezing":  # 코골이
            sntns = """Severe snoring can cause insomnia. I think you should go to the hospital.""", """Studies have shown that snoring can disappear if you lose weight."""
            response = random.choice(sntns)
        else:
            response = '''Are you okay? you don't look well'''
        dispatcher.utter_message(" " + response)
####################################################################################################

class ActionPlaySound(Action):

    def name(self) -> Text:
        return "action_play_sound"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_emotion = tracker.get_slot('user_emotion')

        SOUND = [
            {"emotion": "normal",
             "url": [
                 "https://blog.kakaocdn.net/dn/N3yrx/btquO7jL40n/ddsqt7H1RUrRh5rUv20Q51/%EC%9B%83%EC%9D%8C%EC%86%8C%EB%A6%AC%201.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/cgR68e/btquSqBIXXQ/TJz4pRwEvUENC2pFl8TvXK/%EC%A8%8D%EA%B7%B8%EB%9E%91.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/cF6LOC/btqvf19QgH9/CgNvUBKoquskaIMppn5FK1/19.%ED%9C%98%EB%A6%AC%EB%A6%AD.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/VutF2/btquO7jL9AQ/JUbuSfdZ4jt18JuYU5vv70/BOOM.WAV?attach=1&knm=tfile.WAV",
                 "https://blog.kakaocdn.net/dn/xqL5c/btquQxaX6rp/mmMLrTyEq0KUm17pv4ol00/%EA%B8%B0%EC%B0%A8%2B%ED%9A%A8%EA%B3%BC%EC%9D%8C.m4a?attach=1&knm=tfile.m4a",
                 "https://blog.kakaocdn.net/dn/clKCll/btquSgzmcoZ/0tz1ATtxRfb6rToKDf01Jk/%EB%91%90%EA%B7%BC%EB%91%90%EA%B7%BC.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/zk4WN/btqvicCNYOV/IO0PK96kT4D1lyzRzoUPtK/019.%EC%9E%A5%EB%A9%B4%ED%9A%A8%EA%B3%BC%EC%9D%8C_%ED%9E%88%EC%9E%89.mp3?attach=1&knm=tfile.mp3",
             ]},
            {"emotion": "happy",
             "url": [
                 "https://blog.kakaocdn.net/dn/sU3nb/btquSyTPTOD/hL6n9C21gpKV0hVkVhbi11/%EC%9B%83%EC%9D%8C%EC%86%8C%EB%A6%AC%202.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/cb73os/btquSh54K62/vGZf1OtxoKU4kKgSZbgC6K/%EB%A7%88%EB%B2%95.WAV?attach=1&knm=tfile.WAV",
                 "https://blog.kakaocdn.net/dn/6txP0/btquSyfe6uQ/svjnaUBJqIkRAWVZQQ2Y91/%EC%95%84%EA%B8%B0%EC%9B%83%EC%9D%8C.wav?attach=1&knm=tfile.wav",
                 "https://blog.kakaocdn.net/dn/cptLvc/btqvdlPb3fk/1J1NKs9IHbKymQQ7htXKy0/018.%EC%9E%A5%EB%A9%B4%ED%9A%A8%EA%B3%BC%EC%9D%8C_%ED%99%98%ED%98%B8.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/cxKzh0/btquRMMfUoI/HbBrFmVqRKUYQrutFUtO3k/%EC%8A%A4%ED%8C%8C%EB%A5%B4%ED%83%80.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/VutF2/btquO7jL9AQ/JUbuSfdZ4jt18JuYU5vv70/BOOM.WAV?attach=1&knm=tfile.WAV"
             ]},
            {"emotion": "sad",
             "url": [
                 "https://blog.kakaocdn.net/dn/boBxIl/btquP3uqg2Z/u409ishwsDBel0fJijIiyk/%EB%85%B8%EA%B0%93%ED%94%8C%EB%A6%AC%EC%A6%88.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/bElusX/btquRcj7kLR/A27KuTwpfszVcnYKeBHBQ0/%EB%95%8C%EB%A6%AC%EB%8A%94%ED%9A%A8%EA%B3%BC%EC%9D%8C.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/boBxIl/btquP3uqg2Z/u409ishwsDBel0fJijIiyk/%EB%85%B8%EA%B0%93%ED%94%8C%EB%A6%AC%EC%A6%88.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/bb6F2V/btquRMZN3Yh/mkWsRCaHTkUo3cTeTgKdG1/nope.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/bkuo3f/btqveiq8oNz/dXqiCnYo1ShyCsZcE27QB1/014.%EC%9E%A5%EB%A9%B4%ED%9A%A8%EA%B3%BC%EC%9D%8C_%EC%B0%AC%EB%B0%94%EB%9E%8C.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/bHQgyQ/btqvdkCJkji/RSvjHFzVdIqoyUHDlHkcG1/003.%EC%93%B8%EC%93%B8%ED%95%9C.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/zk4WN/btqvicCNYOV/IO0PK96kT4D1lyzRzoUPtK/019.%EC%9E%A5%EB%A9%B4%ED%9A%A8%EA%B3%BC%EC%9D%8C_%ED%9E%88%EC%9E%89.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/Bzq3Q/btqvcgm6axM/HzHHJvZqbnpzBSNndtrIW1/013.%EC%9E%A5%EB%A9%B4%ED%9A%A8%EA%B3%BC%EC%9D%8C_%EC%8B%B8%EC%9D%B4%EB%A0%8C.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/cD3mYQ/btquPLHxvdi/qZCKhEyaMjA3xKCr2hHfw1/%EA%B6%8C%EC%B4%9D%ED%95%9C%EB%B0%9C.WAV?attach=1&knm=tfile.WAV",
                 "https://blog.kakaocdn.net/dn/BxYTT/btquPNrQvfR/Xw5jDX3QDzzRbJPoICbB1k/%EB%9F%B0%EB%8B%9D%EB%A7%A8%2B%ED%9A%A8%EA%B3%BC%EC%9D%8C%2B%EB%9C%A8%ED%97%89%21.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/ciO7fv/btqve5kwmLv/XRto7KHdP8QvwV0Mykn5V1/15.%EC%9D%B4%EA%B1%B4%EB%84%88%EB%AC%B4%ED%95%9C%EA%B1%B0%EC%95%84%EB%8B%88%EB%83%90%EA%B3%A0%EC%8B%9C.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/MMyWV/btquP3nFJmm/np1P7cofZdhr5phWfVmpPK/%EC%B2%9C%EB%91%A5.wav?attach=1&knm=tfile.wav",
                 "https://blog.kakaocdn.net/dn/WJQzU/btquRN5uBlr/KA48sX3O9WZwmnu5YLyKYK/%EA%B3%B5%ED%8F%AC%20BGM.mp3?attach=1&knm=tfile.mp3",
                 "https://blog.kakaocdn.net/dn/bdKEtM/btquShkIi7G/EPBxn2RjrDbKqBKOZowpNk/%EC%9C%BC%EC%95%85%20%EB%82%B4%EB%88%88%21.mp3?attach=1&knm=tfile.mp3"
             ]}
        ]

        sounds = [m.get("url") for m in SOUND if m.get("emotion") == user_emotion]
        if sounds:
            url = random.choice(sounds[0])
            playsound(url)

        else:
            idx = np.random.randint(0, len(SOUND))
            temp_emotion = SOUND[idx].get("emotion")
            sounds = [m.get("url") for m in SOUND if m.get("emotion") == temp_emotion]
            url = random.choice(sounds[0])
            playsound(url)


####################################################################################################


class ActionShowPicture(Action):

    def name(self) -> Text:
        return "action_show_picture"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_emotion = tracker.get_slot('user_emotion')

        PICTURES = [
            {"emotion": "normal",
             "url": [
                 "https://i.pinimg.com/originals/29/97/8d/29978d58c017b52dd19a3f2e2cb9f9fa.jpg",
                 "https://img1.daumcdn.net/thumb/R720x0.q80/?scode=mtistory2&fname=http%3A%2F%2Fcfile10.uf.tistory.com%2Fimage%2F210C7A4B564CAEE9038081",
                 "https://image.shutterstock.com/image-photo/surprised-kid-sitting-table-childs-260nw-464300804.jpg",
                 "https://thumbs.dreamstime.com/z/surprised-baby-14784573.jpg",
                 "https://media.gettyimages.com/photos/adorable-expressive-little-girl-picture-id175484660?s=612x612",
                 "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcROSMNGX1apf5GCxtm36oNp_W5a4rbl1Kd2SQ&usqp=CAU",
                 "https://stickershop.line-scdn.net/stickershop/v1/product/1002563/LINEStorePC/main.png;compress=true",
                 "https://www.spaciousbreath.com/wp-content/uploads/2019/09/Busy-busy-busy-1080x608.jpg"
             ]},
            {"emotion": "happy",
             "url": [
                 "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTppCN8AmHbZBWdKIWQUm9wscdaFv5xnl6L0g&usqp=CAU",
                 "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSmh5PzTD_0NMrnjksIOVrHnZX7zslrdu2erw&usqp=CAU",
                 "https://img.mimint.co.kr/bbs/2020/05/27/C2005270925293413r.jpeg",
                 "https://lh3.googleusercontent.com/proxy/MEvRO7QX1RmXRjOvIKNhe7uN2Pv630CriNqDzjw2d8QzIzphp5eUpE5Oa85t4pGMCmf_sMCcqA6FqTvfqcEGNRkmXPc1IZJxAKM2p-rU-S0veePiYmC3RLfLdjyPi_5FFNkQmVEAGbu619EgadJnXCWkQ5HF6a0a9zhbziwehGNHdV5WfG1uOaK9C7HsdZq4OMAJvZQqV5-N1UxsYaw47PmHe_mlUDmPkesMX0SVhcw-UOMgsK4pKuOoubs_RohX15q24BMUtrOrFeQjuUcvSQq-AAjkhb-Kb-r7FGSh4DALWo8w-oVju62hg9UabHM",
                 "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRdAtv04UT9QCuUwP8mXDB5ghw561SZiddhmw&usqp=CAU",
                 "https://lh3.googleusercontent.com/proxy/73Ap4GUPxMjhsjhKH0njosCb2Y_Ovf4ppmcrw4VTE9rZDtsc4TbVXF3N9wCO-6DkTXRNY6vyJXnJDcK_WbtWLrhbxkXdPAQhfyLhZd_xjebi",
                 "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pixcove.com%2Fsun-content-sunshine-sunlight-happy-emotions-golden-excellent-happiness-yellow-rays-cheerful-creamy-light%2F&psig=AOvVaw09W3Sc6w0H27t0djrTNQNe&ust=1605456968210000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLDh5Le3gu0CFQAAAAAdAAAAABAD",
                 "https://www.google.com/url?sa=i&url=https%3A%2F%2Fqrius.com%2Fwhy-the-power-of-cute-is-colonising-our-world%2F&psig=AOvVaw2hYQZAdsA4ELSbIKQpStLf&ust=1605457004949000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKCz0Mi3gu0CFQAAAAAdAAAAABAD",
                 "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.123rf.com%2Fphoto_102953800_stock-vector-cute-cartoon-avocado-couple-in-love-avocuddle-two-avocado-halves-with-heart-st-valentines-day-greeti.html&psig=AOvVaw2hYQZAdsA4ELSbIKQpStLf&ust=1605457004949000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKCz0Mi3gu0CFQAAAAAdAAAAABAJ",
                 "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.entertainmentmesh.com%2Ffree-hd-cute-iphone-wallpapers-background-images%2F&psig=AOvVaw2hYQZAdsA4ELSbIKQpStLf&ust=1605457004949000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKCz0Mi3gu0CFQAAAAAdAAAAABAa",
                 "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.emmasdiary.co.uk%2Fpregnancy-and-birth%2Fbaby-names%2Fbaby-name-ideas%2Fcute-baby-names-we-adore&psig=AOvVaw2hYQZAdsA4ELSbIKQpStLf&ust=1605457004949000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKCz0Mi3gu0CFQAAAAAdAAAAABAt",
                 "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.aliexpress.com%2Fitem%2F32307535476.html&psig=AOvVaw2hYQZAdsA4ELSbIKQpStLf&ust=1605457004949000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKCz0Mi3gu0CFQAAAAAdAAAAABA5",
                 "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.fluentu.com%2Fblog%2Ffrench%2Fcute-french-words%2F&psig=AOvVaw2hYQZAdsA4ELSbIKQpStLf&ust=1605457004949000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKCz0Mi3gu0CFQAAAAAdAAAAABA_",
                 "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F497788565062979384%2F&psig=AOvVaw3_i7hsZbJ3YJXrpyPyePGF&ust=1605457123031000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLit1P63gu0CFQAAAAAdAAAAABAD",
                 "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DiZafO_p5QVQ&psig=AOvVaw3_i7hsZbJ3YJXrpyPyePGF&ust=1605457123031000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLit1P63gu0CFQAAAAAdAAAAABAJ",
             ]},
            {"emotion": "sad",
             "url": [
                 "https://lh3.googleusercontent.com/proxy/z6lfiqZYzqfeAid4MxbYKDqYo0yrVEgEXTtJkEvvngwrCCgkRAlV1NdHu0GkUkuBfuVFJUvgL2Icyp_91hOvWQVqKWATLKe9mYZCtE5m2eB4UalmZ7KDKmWqvp633Eql3HKBfljzmAWhmn8K1sG9ypTlGSekzWmIHO0PISJX",
                 "https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Ft1.daumcdn.net%2Fcfile%2Ftistory%2F146BF839502A0D1E12",
                 "https://ojsfile.ohmynews.com/STD_IMG_FILE/2018/0709/IE002361529_STD.jpg"
                 "https://t1.daumcdn.net/cfile/blog/211DC2445464A03F03?original",
                 "https://pbs.twimg.com/media/Dh_mGb1UcAEe-br.jpg",
                 "https://kregianmiral.files.wordpress.com/2017/03/wp-1489823760161.jpeg",
                 "https://images.lifealth.com/uploads/2018/03/commitments-to-make-if-you-want-to-be-happy.jpg",
                 "https://i.pinimg.com/originals/74/70/41/7470419b12f1a5024401e3a7ce3bb0e6.jpg",
                 "https://www.clevelandheartlab.com/wp-content/uploads/2019/11/ThinkPositive.png",
                 "https://wbn.co.nz/wp-content/uploads/2019/11/Positive.jpg",
                 "https://blog.lifestyleplus.net/uploads/images/positive-thinking-today-will-be-great.png",
                 "https://www.verywellmind.com/thmb/t45CRRuibSKE7oZow0JPm9j-yq4=/1500x1000/filters:fill(ABEAC3,1)/manage-your-anxiety-2584184-01-07daf91ba6de41d19f827cf65ceef07a.png",
                 "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSHYe9hLToniH-W5dBPsJVonpgNRmG2opn0dg&usqp=CAU",
                 "https://thumbs.dreamstime.com/z/cheer-up-cute-marshmallow-illustration-minimalism-prints-posters-cards-postcards-notebooks-books-primitive-cheer-up-cute-132281976.jpg",
                 "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTFbX4ApXTWXNIZKaMd0WdXkALEcl20lp7hMQ&usqp=CAU",
                 "https://memegenerator.net/img/instances/66916173.jpg",
                 "https://jokeryogi.files.wordpress.com/2013/02/tired-cat.jpg",
                 "https://emergency.com.au/wp-content/uploads/2017/02/nervous.jpg",
                 "https://i.ytimg.com/vi/wMHUitqSpqA/maxresdefault.jpg",
                 "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQeuwr2eGCMbBYxkL2lIi_VkSC84Gn9frk0yw&usqp=CAU",
                 "https://image.shutterstock.com/image-photo/jealous-girl-see-her-brother-260nw-1291797199.jpg",
                 "https://static1.squarespace.com/static/52896e52e4b013f4223687c2/5388ecbee4b03f675a0f30f7/57eaa9d4e6f2e1db284ecc41/1494268033906/1ebf63996b684e6a32e14824903425fd.jpg?format=1500w",
                 "https://www.wikihow.com/images/thumb/6/6e/Handle-a-Jealous-Sibling-Step-1-Version-3.jpg/v4-460px-Handle-a-Jealous-Sibling-Step-1-Version-3.jpg.webp",
                 "https://images.theconversation.com/files/249643/original/file-20181210-76968-1j48v7c.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1200&h=1200.0&fit=crop",
                 "https://pi.tedcdn.com/r/talkstar-assets.s3.amazonaws.com/production/playlists/playlist_468/overcome_fears_1200x627.jpg?quality=89&w=800",
                 "https://veritusgroup.com/wp-content/uploads/2017/01/littlegirlfearful2-2016-Feb22.jpg"
             ]}
        ]

        pictures = [m.get("url") for m in PICTURES if m.get("emotion") == user_emotion]
        if pictures:
            print(user_emotion)
            url = random.choice(pictures[0])
            img = Image.open(urlopen(url))
            img.show()
        else:
            idx = np.random.randint(0, len(PICTURES))
            temp_emotion = PICTURES[idx].get("emotion")

            print(temp_emotion)
            pictures = [m.get("url") for m in PICTURES if m.get("emotion") == temp_emotion]
            url = random.choice(pictures[0])
            img = Image.open(urlopen(url))
            img.show()


####################################################################################################


class ActionShowQuote(Action):

    def name(self) -> Text:
        return "action_show_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_emotion = tracker.get_slot('user_emotion')

        QUOTES = [
            {"emotion": "normal",
             "url": [
                 "H.o.m.e.w.o.r.k.= half of my energy wasted on random knowledge.",
                 "Parenting is a lot like folding a fitted sheet, no one really knows how the hell to do it",
                 "Quote of the year: When you are dead, you do not know that you are dead. All of the pain is felt by others. The same thing happens when you are stupid.",
                 "Sleep is the best meditation.",
                 "A day without a nap is like a cupcake without frosting.",
                 "Your future depends on your dreams, so go to sleep.",
                 "Never tell people how to do things. Tell them what to do and they will surprise you with their ingenuity.",
                 "Of all the hardships a person had to face, none was more punishing than the simple act of waiting.",
                 "“'Well,' said Pooh, 'what I like best,'' and then he had to stop and think. Because although Eating Honey was a very good thing to do, there was a moment just before you began to eat it which was better than when you were, but he didn't know what it was called.”",
                 "Never be so busy as not to think of others.",
                 "And if they thought her aimless, if they thought her a bit mad, let them. It meant they left her alone. Marya was not aimless, anyway. She was thinking.",
                 "Those who are wise won't be busy, and those who are too busy can't be wise."
             ]},
            {"emotion": "happy",
             "url": [
                 "True happiness is…to enjoy the present, without anxious dependence upon the future.",
                 "Happiness is not something ready-made. It comes from your own actions.",
                 "Dear world, I am excited to be alive in you, and I am thankful for another year.",
                 "I'm selfish, impatient and a little insecure. I make mistakes, I am out of control and at times hard to handle. But if you can't handle me at my worst, then you sure as hell don't deserve me at my best.",
                 "You've gotta dance like there's nobody watching, Love like you'll never be hurt, Sing like there's nobody listening, And live like it's heaven on earth.",
                 "Be proud of your struggles. Adversity brings out the best in us.",
                 "Do not complicate your proudness for my rudeness"
             ]},
            {"emotion": "sad",
             "url": [
                 "And in the end all I learned was how to be strong… Alone.",
                 "It’s easy to stand with the crowd it takes courage to stand alone",
                 "I used to think the worst thing in life was to end up all alone, it’s not. The worst thing in life is to end up with people that make you feel all alone.",
                 "Whatever you do, make it pay.",
                 "Ley bygones be bygones.",
                 "No pain no gain.",
                 "Step by step goes a long way.",
                 "The truth will set you free, but first it will piss you off.",
                 "Don’t waste your time in anger, regrets, worries, and grudges. Life is too short to be unhappy.",
                 "I am awfully greedy; I want everything from life. I want to be a woman and to be a man, to have many friends and to have loneliness, to work much and write good books, to travel and enjoy myself, to be selfish and to be unselfish… You see, it is difficult to get all which I want. And then when I do not succeed I get mad with anger.",
                 "Every man has his secret sorrows which the world knows not; and often times we call a man cold when he is only sad.",
                 "I didn't want to wake up. I was having a much better time asleep. And that's really sad. It was almost like a reverse nightmare, like when you wake up from a nightmare you're so relieved. I woke up into a nightmare.",
                 "There are wounds that never show on the body that are deeper and more hurtful than anything that bleeds.",
                 "Trust yourself. You’ve survived a lot, and you’ll survive whatever is coming.",
                 "Inner peace begins the moment you choose not to allow another person or event to control your emotions.",
                 "Smile, breathe, and go slowly.",
                 "I don’t trust anybody. Not anybody. And the more that I care about someone, the more sure I am they’re going to get tired of me and take off.",
                 "So avoid using the word ‘very’ because it’s lazy. A man is not very tired, he is exhausted. Don’t use very sad, use morose. Language was invented for one reason, boys - to woo women - and, in that endeavor, laziness will not do. It also won’t do in your essays.",
                 "Tired, tired with nothing, tired with everything, tired with the world’s weight he had never chosen to bear.",
                 "I am somewhat exhausted; I wonder how a battery feels when it pours electricity into a non-conductor?",
                 "It's hard not to feel humorless, as a woman and a feminist, to recognize misogyny in so many forms, some great and some small, and know you're not imagining things. It's hard to be told to lighten up because if you lighten up any more, you're going to float the fuck away. The problem is not that one of these things is happening; it's that they are all happening, concurrently and constantly.",
                 "As Aristotle said, 'Excellence is a habit.' I would say furthermore that excellence is made constant through the feeling that comes right after one has completed a work which he himself finds undeniably awe-inspiring. He only wants to relax until he's ready to renew such a feeling all over again because to him, all else has become absolutely trivial.",
                 "A well adjusted person is one who makes the same mistake twice without getting nervous.",
                 "When you feel nervous, recall your pride.",
                 "Relax; the world's not watching that closely. It's too busy contemplating itself in the mirror.",
                 "The worst part of success is trying to find someone who is happy for you.",
                 "Moral indignation is jealousy with a halo.",
                 "Each of us must confront our own fears, must come face to face with them. How we handle our fears will determine where we go with the rest of our lives. To experience adventure or to be limited by the fear of it.",
                 "Inaction breeds doubt and fear. Action breeds confidence and courage. If you want to conquer fear, do not sit home and think about it. Go out and get busy."
             ]}
        ]

        quote = [m.get("url") for m in QUOTES if m.get("emotion") == user_emotion]
        if quote:
            st = random.choice(quote[0])
            dispatcher.utter_message(st)
        else:
            idx = np.random.randint(0, len(QUOTES))
            temp_emotion = QUOTES[idx].get("emotion")
            quote = [m.get("url") for m in QUOTES if m.get("emotion") == temp_emotion]
            st = random.choice(quote[0])
            dispatcher.utter_message(st)
####################################################################################################

class ActionRepeat(Action):

    def name(self) -> Text:
        return "action_repeat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_input = tracker.latest_message.get('text')

        phraser = Paraphraser(random_ua=True)
        rephrased = phraser.paraphrase(user_input)
        dispatcher.utter_message(rephrased)
##################################################################################
## chae 16 : action_movie // 영화 정보에 관한 행동
## 사용하는 슬롯 : movie + 현재시간
##################################################################################
MOVIES = [{
    "name": "Harry Potter",
    "description": "Harry Potter is a film series based on the eponymous novels by author J. K. Rowling. The series is distributed by Warner Bros."
},
    {
        "name": "Mamma Mia!",
        "description": "Mamma Mia! is a 2008 jukebox musical film directed by Phyllida Lloyd and written by Catherine Johnson based on the 1999 musical."
    },
    {
        "name": "Frozen",
        "description": "Frozen is a 2013 American 3D computer-animated musical fantasy film produced by Walt Disney Animation Studios and released by Walt Disney Pictures."
    },
    {
        "name": "Joker",
        "description": "Joker is a 2019 American psychological thriller film directed and produced by Todd Phillips, who co-wrote the screenplay with Scott Silver."
    },
    {
        "name": "The Avengers",
        "description": "The Avengers, is a 2012 American superhero film based on the Marvel Comics superhero team and was produced by Marvel Studios and distributed by Walt Disney Studios Motion Pictures."
    },
    {
        "name": "Sherlock Holmes",
        "description": "Sherlock Holmes is a 2009 period mystery action film based on the character of the same name created by Sir Arthur Conan Doyle. In 1890, eccentric detective Holmes and his companion Watson are hired by a secret society to foil a mysticist's plot to gain control of Britain by seemingly supernatural means."
    },
    {
        "name": "The Dark Night",
        "description": "The only comic book movie to make the cut is Christopher Nolan’s genre masterpiece: fatalist, bracing and forever the legacy of Heath Ledger, posthumously awarded an Oscar for his terrifying performance. "
    },
    {
        "name": "Call Me By Your Name",
        "description": "Rarely has summer lust been so headily captured as in Luca Guadagnino’s breakout Italian romance. Transformative leads from Timothée Chalamet and Armie Hammer captured the collective imagination; Michael Stuhlbarg gently grounded realities."
    },
    {
        "name": "Ocean’s Eleven",
        "description": "Steven Soderbergh is the Renaissance man of American cinema, and this intricately crafted heist movie shows him on never-bettered, commercially minded form. George Clooney is at his most Cary Grant-ish as the leader of the crack team of robbers."
    },
    {
        "name": "Titanic",
        "description": "James Cameron doesn't do things by halves. His movie about the 1912 sinking of the world's biggest cruise liner was the most expensive ever made, suffered a difficult, overrunning shoot, and was predicted to be a career-ending flop."
    },
    {
        "name": "The Terminator",
        "description": "It features time travel and a cyborg, with car chases and shoot-outs, but in James Cameron's first proper movie (ie not featuring flying piranhas) it's all packed around the blood-covered endoskeleton of a relentless-killer horror pic."
    },
    {
        "name": "Leon",
        "description": "Movie's greatest strength is in Natalie Portman, delivering a luminous, career-creating performance as vengeful 12-year-old Mathilda, whose relationship with the monosyllabic killer is truly affecting, and nimbly stays just on the right side of acceptable."
    },
    {
        "name": "Captain America: Civil War",
        "description": "The third solo Cap outing managed to be both intensely crowd-pleasing and also daringly intelligent, placing its superheroes in a believable geopolitical context that raised a valid moral issue: who should be responsible for the deployment of such great power?"
    },
    {
        "name": "Toy Story",
        "description": "Toy Story is a 1995 American computer-animated buddy comedy film produced by Pixar Animation Studios and released by Walt Disney Pictures. Taking place in a world where anthropomorphic toys come to life when humans are not present, the plot focuses on the relationship between an old-fashioned pull-string cowboy doll named Woody and an astronaut action figure, Buzz Lightyear, as they evolve from rivals competing for the affections of their owner Andy Davis, to friends who work together to be reunited with him after being separated from him."
    },
    {
        "name": "Interstellar",
        "description": "Interstellar is a 2014 British-American epic science fiction film directed, co-written and produced by Christopher Nolan. Set in a dystopian future where humanity is struggling to survive, the film follows a group of astronauts who travel through a wormhole near Saturn in search of a new home for mankind."
    },
    {
        "name": "The Matrix",
        "description": "The Matrix is a 1999 American science fiction action film written and directed by the Wachowskis. It depicts a dystopian future in which humanity is unknowingly trapped inside a simulated reality, the Matrix, created by intelligent machines to distract humans while using their bodies as an energy source."
    },
    {
        "name": "The Lord Of The Rings",
        "description": "The Lord of the Rings is a film series of three epic fantasy adventure films directed by Peter Jackson, based on the novel written by J. R. R. Tolkien.Set in the fictional world of Middle-earth, the films follow the hobbit Frodo Baggins as he and the Fellowship embark on a quest to destroy the One Ring, to ensure the destruction of its maker, the Dark Lord Sauron."
    },
    {
        "name": "Jurassic World",
        "description": "Jurassic World is a 2015 American science fiction adventure film. It is the fourth installment of the Jurassic Park film series and the first installment in the Jurassic World trilogy, while also serving as a direct sequel to the franchise's first film, Jurassic Park (1993)."
    },
    {
        "name": "Inception",
        "description": "Inception is a 2010 science fiction action film written and directed by Christopher Nolan, who also produced the film with his wife, Emma Thomas.  The film stars Leonardo DiCaprio as a professional thief who steals information by infiltrating the subconscious of his targets. He is offered a chance to have his criminal history erased as payment for the implantation of another person's idea into a target's subconscious."
    },
    {
        "name": "Dead Poets Society",
        "description": "Dead Poets Society is a 1989 American teen drama film directed by Peter Weir, written by Tom Schulman, and starring Robin Williams. Set in 1959 at the fictional elite conservative Vermont boarding school Welton Academy, it tells the story of an English teacher who inspires his students through his teaching of poetry."
    }
]


class ActionMovie(Action):
    def name(self) -> Text:
        return "action_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_movie = tracker.get_slot("movie")
        a = tracker.latest_message.get("text")  ## User input 불러오기

        rand = random.randint(0, 2)
        arand = random.randint(0, len(MOVIES) - 1)

        if user_movie is not None:
            movie = [m for m in MOVIES if m.get("name").lower() == user_movie.lower()]
            if movie:
                response = movie[0].get("description")

            else:
                sntns = ["""I am not sure about that. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to watch {}.""",
                         """Sorry, I don't know about that. How about watching {}?"""]

                response = sntns[rand].format(MOVIES[arand].get("name"))
        else:
            response = "Sorry..?"
        dispatcher.utter_message(response)
        return [SlotSet("movie", None)]


##################################################################################
## chae 17 : action_diner // 운동정보에 관한 행동
## 사용하는 슬롯 : diner
##################################################################################
class ActionDiner(Action):

    def name(self) -> Text:
        return "action_diner"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        diner = tracker.get_slot('diner')

        DINER = [
            {"name": "Arby's",
             "info": "Arby's is an American fast food sandwich restaurant chain with more than 3,300 restaurants system wide and third in terms of revenue. In October 2017, Food & Wine called Arby's 'America's second largest sandwich chain (after Subway)'. In addition to its classic Roast Beef and Beef 'n Cheddar sandwiches, Arby's products also include deli-style Market Fresh line of sandwiches, Greek gyros, Curly Fries and Jamocha Shakes"},
            {"name": "Auntie Anne's",
             "info": "Auntie Anne's, Inc., is an American chain of pretzel shops founded by Anne F. Beiler and her husband, Jonas, in 1988. Auntie Anne's serves products such as pretzels, dips, and beverages. They also offer Pretzels & More Homemade Baking Mix."},
            {"name": "Burger King",
             "info": "Burger King (BK) is an American multinational chain of hamburger fast food restaurants. Headquartered in Miami-Dade County, Florida, the company was founded in 1953 as Insta-Burger King, a Jacksonville, Florida–based restaurant chain. Burger King's menu has expanded from a basic offering of burgers, French fries, sodas, and milkshakes to a larger and more diverse set of products."},
            {"name": "Chick-fil-A",
             "info": "Chick-fil-A is one of the largest American fast food restaurant chains and the largest whose specialty is chicken sandwiches. The company operates more than 2,605 restaurants, primarily in the United States with locations in 48 states. The restaurant serves breakfast before transitioning to its lunch and dinner menu. Chick-fil-A also offers customers catered selections from its menu for special events."},
            {"name": "Charleys Philly Steaks",
             "info": "Charleys Philly Steaks is an American restaurant chain of Philly cheesesteak stores headquartered in Columbus, Ohio. Formerly known as Charley's Steakery and Charley's Grilled Subs, the franchise was established in 1986 on the campus of The Ohio State University in Columbus, Ohio, and is still headquartered there. By 2017 there were 600 locations in 45 states and in 19 countries."},
            {"name": "Cora",
             "info": "Coramark Inc. (doing business as Cora) is a Canadian chain of casual restaurants serving breakfast and lunch. Chez Cora began in 1987 when Cora Tsouflidou opened a snack bar in Montreal, Quebec, Canada. It is now a chain of more than 50 franchises in Quebec and 130 across Canada."},
            {"name": "Dairy Queen",
             "info": "Dairy Queen (DQ) is an American multinational chain of soft serve ice cream and fast-food restaurants owned by International Dairy Queen, Inc., a subsidiary of Berkshire Hathaway. International Dairy Queen, Inc., also owns Orange Julius, and formerly owned Karmelkorn and Golden Skillet Fried Chicken."},
            {"name": "Denny's",
             "info": "Denny's (also known as Denny's Diner on some of the locations' signage) is an American table service diner-style restaurant chain. It operates over 1,700 restaurants. Originally opened as a coffee shop under the name Danny's Donuts, Denny's is now known for always being open and serving breakfast, lunch, and dinner around the clock."},
            {"name": "Domino's Pizza",
             "info": "Domino's Pizza, Inc., branded as Domino's, is an American multinational pizza restaurant chain founded in 1961. The Domino's menu varies by region. The current Domino's menu in the United States features a variety of Italian-American main and side dishes. Pizza is the primary focus, with traditional, specialty, and custom pizzas available in a variety of crust styles and toppings. "},
            {"name": "Din Tai Fung",
             "info": "Din Tai Fung is a Taiwanese restaurant franchise specializing in Huaiyang cuisine. Din Tai Fung is known internationally for its paper-thin wrapped xiaolongbao with 18 folds. The New York Times named it one of the top ten restaurants in the world in 1993."},
            {"name": "Five Guys",
             "info": "Five Guys Enterprises LLC (doing business as Five Guys Burgers and Fries) is an American fast casual restaurant chain focused on hamburgers, hot dogs, and French fries, and headquartered in Lorton, Virginia, an unincorporated part of Fairfax County. The Five Guys menu is centered on customisable hamburgers offered with Kraft American cheese or applewood-smoked bacon, customisable kosher style hot dogs (Hebrew National all-beef franks), grilled cheese and vegetable sandwiches. "},
            {"name": "Jollibee",
             "info": "Jollibee is a Filipino multinational chain of fast food restaurants owned by Jollibee Foods Corporation (JFC). Jollibee is a fast food restaurant with American-influenced items, as well as casual Filipino fare. Among the establishment's best sellers are its Yumburger, the house hamburger first introduced during their early days of operation; Chicken Joy, a fried chicken meal introduced in the 1980s."},
            {"name": "Kenny Rogers Roasters",
             "info": "Kenny Rogers Roasters is a chain of chicken-based restaurants founded in 1991 by country musician Kenny Rogers and former KFC CEO John Y. Brown Jr., who is a former governor of the U.S. state of Kentucky.The menu of Kenny Rogers Roasters originally featured wood-fired rotisserie chicken. "},
            {"name": "Outback Steakhouse",
             "info": "Outback Steakhouse is an Australian-themed American casual dining restaurant chain, serving American cuisine, based in Tampa, Florida. The Bloomin' Onion is a signature Outback item. It is a one-pound onion cut to 'bloom' open, breaded, deep-fried and served with mayonnaise-horseradish sauce. Outback also features a variety of steaks, seafood, and other American chain restaurant menu items from burgers to salads."},
            {"name": "Panda Express",
             "info": "Panda Express is a fast food restaurant chain which serves American Chinese cuisine. The chain offers a variety of Chinese-cuisine-inspired dishes (e.g., Orange Chicken; Sweet Fire Chicken Breast; Beijing Beef; Grilled Teriyaki Chicken; Kung Pao Chicken), with certain premium dishes such as Honey Walnut shrimp and Black Pepper Angus Steak having additional costs for the patron. 'Combo meals' are served with customer's choice of either fried rice, brown or white steamed rice, chow mein, or super greens. "},
            {"name": "PizzaExpress",
             "info": "PizzaExpress is a restaurant group based in the United Kingdom and owned by Chinese Hony Capital. Since its foundation, PizzaExpress has specialised primarily in handmade pizza in the traditional Italian style. In 2008, PizzaExpress started a Guest Chef Series with chef Theo Randall, of Theo Randall at InterContinental London, creating exclusive dishes for its menu. Francesco Mazzei, of L'Anima, came on board in 2010 to develop a menu inspired by the cuisine of Calabria."},
            {"name": "Quiznos",
             "info": "QIP Holder, LLC, doing business as Quiznos, is an American franchised fast-food restaurant brand based in Denver, Colorado, that specializes in offering toasted submarine sandwiches. Quiznos is known for their toasted subs."},
            {"name": "Taco Bell",
             "info": "Taco Bell is an American-based chain of fast food restaurants originating in Irvine, California in 1962, by founder Glen Bell. The restaurants serve a variety of Mexican-inspired foods, that include: tacos, burritos, quesadillas, nachos, novelty and specialty items, along with a variety of 'value menu' items."},
            {"name": "Wendy's",
             "info": "Wendy's is an American international fast food restaurant chain founded by Dave Thomas on November 15, 1969, in Columbus, Ohio. Wendy's was the world's third-largest hamburger fast-food chain with 6,711 locations, following Burger King and McDonald's. The chain is known for its square hamburgers, sea salt fries, and Frosty, a form of soft-serve ice cream mixed with starches. Wendy's menu consists primarily of hamburgers, chicken sandwiches, French fries, and beverages such as the Frosty."},
            {"name": "Shake Shack",
             "info": "Shake Shack is an American fast casual restaurant chain based in New York City. It also sells chicken burgers, fries, hot dogs, frozen custards, and beer and wine. In each new location, the beverage menu is customized to the local flavors of the city in which it operates. Their most famous product is the ShackBurger."}
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(DINER) - 1)

        if diner is not None:
            user_diner = [m for m in DINER if m.get("name").lower() == diner.lower()]

            if user_diner:
                response = user_diner[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that diner. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know where that is. How about {}?"""]
                response = sntns[rand].format(DINER[arand].get("name"))
        else:
            response = "Sorry, Can you say that again?"
        dispatcher.utter_message(response)
        return [SlotSet("diner", None)]


##################################################################################
## chae 18 : action_travel // 운동정보에 관한 행동
## 사용하는 슬롯 : travel
##################################################################################
class ActionTravel(Action):

    def name(self) -> Text:
        return "action_travel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        travel = tracker.get_slot('travel')

        TRAVEL = [
            {"name": "bleisure travel",
             "info": "Bleisure travel is a portmanteau of “business” and “leisure”, and, it refers to “the activity of combining business travel with leisure time”. The term bleisure was first published in 2009 by the Future Laboratory as part of their biannual Trend Briefing written by writer Jacob Strand, then a future forecaster working for The Future Laboratory, and journalist and futurologist Miriam Rayman."},
            {"name": "package tour",
             "info": "A package tour, package vacation, or package holiday comprises transport and accommodation advertised and sold together by a vendor known as a tour operator. Other services may be provided such a rental car, activities or outings during the holiday. Transport can be via charter airline to a foreign country, and may also include travel between areas as part of the holiday. Package holidays are a form of product bundling."},
            {"name": "pet travel",
             "info": "Pet travel is the process of traveling with or transporting pets. Pet carriers like cat carriers and dog crates confine and protect pets during travel."},
            {"name": "Repositioning cruise",
             "info": "A repositioning cruise (repo cruise) is a cruise in which the embarkation port and the disembarkation port are different. This is a less common type of cruise; in the majority of cruises the ship's final destination is the same as the starting point."},
            {"name": "Riding circuit",
             "info": "Riding circuit is the practice of judges and lawyers, sometimes referred to as circuit riders, travelling to a regular series of locations in order to hold court there. Circuit riding has mostly been abolished, but the term remains in the name 'circuit court', commonly applied to levels of court that oversee many lower district courts."},
            {"name": "Safari holidays",
             "info": "Safari holidays are an increasingly popular holiday activity. They involve the primary goal of watching wild animals in their natural habitat. Kenya claims to have had the first commercial safari holidays, a form of recreation that grew out of big game hunting at the turn of the century. As animal stocks diminished and hunting became less fashionable, people turned to viewing the animals instead."},
            {"name": "Creative trip",
             "info": "A creative trip is a trip whose purpose is to bring an inspiration or information for a creative work. In the Soviet Union, creative trips (Russian: tvorcheskaya komandirovka) were a kind of business trips for creative workers (writers, artists, etc.) with expenses paid by Soviet creative unions."},
            {"name": "Cruising",
             "info": "Cruising (maritime) by boat is an activity that involves living for extended time on a vessel while traveling from place to place for pleasure. Cruising generally refers to trips of a few days or more, and can extend to round-the-world voyages."},
            {"name": "Cultural travel",
             "info": "Cultural travel is a type of travel that emphasizes experiencing life within a foreign culture, rather than from the outside as a temporary visitor. Cultural travelers leave their home environment at home, bringing only themselves and a desire to become part of the culture they visit. Cultural travel goes beyond cultural exploration or discovery; it involves a transformation in way of life."},
            {"name": "Grand Tour",
             "info": "The Grand Tour was the 17th- and 18th-century custom of a traditional trip through Europe undertaken by upper-class young European men of sufficient means and rank (typically accompanied by a chaperone, such as a family member) when they had come of age (about 21 years old)."},
            {"name": "Overseas experience",
             "info": "Overseas Experience (OE) is a New Zealand term for an extended overseas working period or holiday. Sometimes referred to as 'The big OE' in reference to the extended duration of the travel - typically at least one year, and often extended far longer. It is however generally expected that the person returns after a few years; armed with the work and life experience, and wider outlook obtained overseas."},
            {"name": "Pilgrimage",
             "info": "A pilgrimage is a journey, often into an unknown or foreign place, where a person goes in search of new or expanded meaning about their self, others, nature, or a higher good, through the experience. It can lead to a personal transformation, after which the pilgrim returns to their daily life."},
            {"name": "Mancation",
             "info": "A mancation is a male-only vacation. The term is believed to have come about in the decade of the 2000s, although the concept had existed considerably before then."},
            {"name": "River cruise",
             "info": "A river cruise is a voyage along inland waterways, often stopping at multiple ports along the way. Since cities and towns often grew up around rivers, river cruise ships frequently dock in the center of cities and towns."},
            {"name": "Atomic tourism",
             "info": "Atomic tourism is a recent form of tourism in which visitors learn about the Atomic Age by traveling to significant sites in atomic history such as museums with atomic weapons, missile silos, vehicles that carried atomic weapons or sites where atomic weapons were detonated."},
            {"name": "Medical tourism",
             "info": "Medical tourism refers to people traveling abroad to obtain medical treatment. In the past, this usually referred to those who traveled from less-developed countries to major medical centers in highly developed countries for treatment unavailable at home. However, in recent years it may equally refer to those from developed countries who travel to developing countries for lower-priced medical treatments. "},
            {"name": "Sustainable tourism",
             "info": "Sustainable tourism is the tourism that takes full account of its current and future economic, social and environmental impacts, addressing the needs of visitors, the industry, the environment and host communities. Tourism can involve primary transportation to the general location, local transportation, accommodations, entertainment, recreation, nourishment and shopping."},
            {"name": "Ecotourism",
             "info": "Ecotourism is catering for tourists in the natural environment without damaging it or disturbing habitats. It is a form of tourism involving visiting fragile, pristine, and relatively undisturbed natural areas, intended as a low-impact and often small scale alternative to standard commercial mass tourism. It means responsible travel to natural areas, conserving the environment, and improving the well-being of the local people."},
            {"name": "Geotourism",
             "info": "Geotourism deals with the natural and built environments. Geotourism was first defined in England. Their objective is to search for the protected patrimony through the conservation of their resources and of the tourist’s Environmental Awareness. For that, the use of the interpretation of the patrimony makes it accessible to the lay public, promoting its popularization and the development of the Earth sciences”"},
            {"name": "3D virtual tourism",
             "info": "3DVT (or 3D virtual tourism) is the realistic 3D geovisualisation of virtual environments, which allows the user to explore physical places without physical travel.3DVT typically creates a virtual tour that uses 3D models and 2D panoramic images, a sequence of hyperlinked still or video images, and image-based models of the real world, with additional elements such as sound effects, music, narration, and text. "}
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(TRAVEL) - 1)

        if travel is not None:
            user_travel = [m for m in TRAVEL if m.get("name").lower() == travel.lower()]

            if user_travel:
                response = user_travel[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know what that is. How about {}?"""]
                response = sntns[rand].format(TRAVEL[arand].get("name"))
        else:
            response = "Pardon?"
        dispatcher.utter_message(response)
        return [SlotSet("travel", None)]


##################################################################################
## chae 19 : action_place // 장소 정보에 관한 행동
## 사용하는 슬롯 : place
##################################################################################
class ActionPlace(Action):

    def name(self) -> Text:
        return "action_place"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        place = tracker.get_slot('place')

        PLACE = [
            {"name": "Statue of Liberty",
             "info": "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor within New York City, in the United States. The copper statue, a gift from the people of France to the people of the United States, was designed by French sculptor Frédéric Auguste Bartholdi and its metal framework was built by Gustave Eiffel. The statue was dedicated on October 28, 1886."},
            {"name": "Eiffel Tower",
             "info": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889 as the entrance to the 1889 World's Fair, it was initially criticised by some of France's leading artists and intellectuals for its design, but it has become a global cultural icon of France and one of the most recognisable structures in the world."},
            {"name": "Saint Basil's Cathedral",
             "info": "The Cathedral of Vasily the Blessed, commonly known as Saint Basil's Cathedral, is a Christian church in Red Square in Moscow, Russia and is regarded as a cultural symbol of the country. The building, now a museum, is officially known as the Cathedral of the Intercession of the Most Holy Theotokos on the Moat or Pokrovsky Cathedral."},
            {"name": "Great Sphinx of Giza",
             "info": "The Great Sphinx of Giza, commonly referred to as the Sphinx of Giza or just the Sphinx, is a limestone statue of a reclining sphinx, a mythical creature with the body of a lion and the head of a human. Facing directly from West to East, it stands on the Giza Plateau on the west bank of the Nile in Giza, Egypt. The face of the Sphinx is generally believed to represent the pharaoh Khafre.["},
            {"name": "Great Wall",
             "info": "The Great Wall of China is the collective name of a series of fortification systems generally built across the historical northern borders of China to protect and consolidate territories of Chinese states and empires against various nomadic groups of the steppe and their polities. "},
            {"name": "Taj Mahal",
             "info": "The Taj Mahal is an ivory-white marble mausoleum on the southern bank of the river Yamuna in the Indian city of Agra. It was commissioned in 1632 by the Mughal emperor Shah Jahan (reigned from 1628 to 1658) to house the tomb of his favourite wife, Mumtaz Mahal; it also houses the tomb of Shah Jahan himself."},
            {"name": "Machu Picchu",
             "info": "Machu Picchu is a 15th-century Inca citadel, located in the Eastern Cordillera of southern Peru, on a 2,430-metre (7,970 ft) mountain ridge. It is located in the Machupicchu District within Urubamba Province above the Sacred Valley, which is 80 kilometres (50 mi) northwest of Cuzco. The Urubamba River flows past it, cutting through the Cordillera and creating a canyon with a tropical mountain climate."},
            {"name": "Mecca",
             "info": "Makkah, officially Makkah al-Mukarramah and commonly shortened to Mecca, is the holiest city in Islam and the capital of the Makkah Province of Saudi Arabia. The city is 70 km (43 mi) inland from Jeddah on the Red Sea, in a narrow valley 277 m (909 ft) above sea level. Its last recorded population was 1,578,722 in 2015."},
            {"name": "Loch Ness",
             "info": "Loch Ness is a large, deep, freshwater loch in the Scottish Highlands extending for approximately 37 kilometres (23 miles) southwest of Inverness. Its surface is 16 metres (52 feet) above sea level. Loch Ness is best known for alleged sightings of the cryptozoological Loch Ness Monster, also known affectionately as 'Nessie'. It is connected at the southern end by the River Oich and a section of the Caledonian Canal to Loch Oich."},
            {"name": "Mont-Saint-Michel",
             "info": "Le Mont-Saint-Michel is a tidal island and mainland commune in Normandy, France. The island lies approximately one kilometer (0.6 miles) off the country's northwestern coast, at the mouth of the Couesnon River near Avranches and is 7 hectares (17 acres) in area. The mainland part of the commune is 393 hectares (971 acres) in area so that the total surface of the commune is 400 hectares (988 acres)."},
            {"name": "Capitol Hill",
             "info": "Capitol Hill, in addition to being a metonym for the United States Congress, is the largest historic residential neighborhood in Washington, D.C., stretching easterly in front of the United States Capitol along wide avenues. It is one of the oldest residential neighborhoods in Washington, D.C. and, with roughly 35,000 people in just under 2 square miles (5 km2), it is also one of the most densely populated."},
            {"name": "Niagara Falls",
             "info": "Niagara Falls is a group of three waterfalls at the southern end of Niagara Gorge, spanning the border between the province of Ontario in Canada and the state of New York in the United States. The largest of the three is Horseshoe Falls, also known as Canadian Falls, which straddles the international border of the two countries. The smaller American Falls and Bridal Veil Falls lie within the United States."},
            {"name": "Opera house",
             "info": "An opera house is a theatre building used for performances of opera. It usually includes a stage, an orchestra pit, audience seating, and backstage facilities for costumes and building sets. While some venues are constructed specifically for operas, other opera houses are part of larger performing arts centers. Indeed the term opera house is often used as a term of prestige for any large performing-arts center."},
            {"name": "Mount Kilimanjaro",
             "info": "Mount Kilimanjaro is a dormant volcano in Tanzania. It has 3 volcanic cones: Kibo, Mawenzi and Shira. It is the highest mountain in Africa and the highest single free-standing mountain in the world: 5,895 metres (19,341 ft) above sea level and about 4,900 metres (16,100 ft) above its plateau base. Kilimanjaro is the 4th most topographically prominent peak on Earth."},
            {"name": "Colosseum",
             "info": "The Colosseum, also known as the Flavian Amphitheatre, is an oval amphitheatre in the centre of the city of Rome, Italy. Built of travertine limestone, tuff (volcanic rock), and brick-faced concrete, it was the largest amphitheatre ever built at the time and held 50,000 to 80,000 spectators. The Colosseum is just east of the Roman Forum."},
            {"name": "Empire State Building",
             "info": "The Empire State Building is a 102-story Art Deco skyscraper in Midtown Manhattan in New York City. It was designed by Shreve, Lamb & Harmon and built from 1930 to 1931. Its name is derived from 'Empire State', the nickname of the state of New York. The building has a roof height of 1,250 feet (380 m) and stands a total of 1,454 feet (443.2 m) tall, including its antenna."},
            {"name": "Lotus Temple",
             "info": "The Lotus Temple, located in Delhi, India, is a Baháʼí House of Worship that was dedicated in December 1986. Notable for its flowerlike shape, it has become a prominent attraction in the city. Like all Baháʼí Houses of Worship, the Lotus Temple is open to all, regardless of religion or any other qualification. "},
            {"name": "Aden",
             "info": "Aden is a port city and, since 2015, the temporary capital of Yemen, located by the eastern approach to the Red Sea (the Gulf of Aden), some 170 km (110 mi) east of Bab-el-Mandeb. Its population is approximately 800,000 people. Aden's natural harbour lies in the crater of a dormant volcano, which now forms a peninsula joined to the mainland by a low isthmus. This harbour, Front Bay, was first used by the ancient Kingdom of Awsan between the 5th and 7th centuries BC."},
            {"name": "Avarua",
             "info": "Avarua (meaning 'Two Harbours' in Cook Islands Māori) is a town and district in the north of the island of Rarotonga, and is the national capital of the Cook Islands. The town is served by Rarotonga International Airport (IATA Airport Code: RAR) and Avatiu Harbour. The population of Avarua District is 4,906 (census of 2016)."},
            {"name": "Beirut",
             "info": "Beirut is the capital and largest city of Lebanon. As of 2007 it had an estimated population of slightly more than 1 million to 2.2 million as part of Greater Beirut, which makes it the third-largest city in the Levant region and the fifteenth-largest in the Arab world. On 4 August 2020, a massive explosion in the Port of Beirut resulted in the death of at least 190 people and the wounding of more than 6,000."},
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(PLACE) - 1)

        if place is not None:
            user_place = [m for m in PLACE if m.get("name").lower() == place.lower()]

            if user_place:
                response = user_place[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that place. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know where that is. How about {}?"""]
                response = sntns[rand].format(PLACE[arand].get("name"))
        else:
            response = "Pardon?"
        dispatcher.utter_message(response)
        return [SlotSet("place", None)]


##################################################################################
## chae 20 : action_animal // 동물 정보에 관한 행동
## 사용하는 슬롯 : animal
##################################################################################
class ActionAnimal(Action):

    def name(self) -> Text:
        return "action_animal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        animal = tracker.get_slot('animal')

        ANIMAL = [
            {"name": "albatross",
             "info": "Albatrosses are very large seabirds in the family Diomedeidae. They range widely in the Southern Ocean and the North Pacific. They are absent from the North Atlantic, although fossil remains show they once occurred there and occasional vagrants are found. "},
            {"name": "ape",
             "info": "Apes (Hominoidea) are a branch of Old World tailless simians native to Africa and Southeast Asia. They are the sister group of the Old World monkeys, together forming the catarrhine clade. They are distinguished from other primates by a wider degree of freedom of motion at the shoulder joint as evolved by the influence of brachiation. "},
            {"name": "badger",
             "info": "Badgers are short-legged omnivores in the families Mustelidae (which also includes the otters, polecats, weasels, and ferrets), and Mephitidae (which also includes the skunks). Badgers are a polyphyletic grouping, and are not a natural taxonomic grouping: badgers are united by their squat bodies, adapted for fossorial activity."},
            {"name": "beaver",
             "info": "Beavers (genus Castor) are large, semiaquatic rodents of the Holarctic realm. There are two extant species, the North American beaver (Castor canadensis) and the Eurasian beaver (C. fiber). Beavers are the second largest rodents after the capybaras. "},
            {"name": "bluebird",
             "info": "The bluebirds are a group of medium-sized, mostly insectivorous or omnivorous birds in the order of Passerines in the genus Sialia of the thrush family (Turdidae). Bluebirds are one of the few thrush genera in the Americas. They have blue, or blue and rose beige, plumage. Female birds are less brightly colored than males, although color patterns are similar and there is no noticeable difference in size between the two birds."},
            {"name": "buffalo",
             "info": "The African buffalo or Cape buffalo (Syncerus caffer) is a large sub-Saharan African bovine. Syncerus caffer caffer, the Cape buffalo, is the typical subspecies, and the largest one, found in Southern and East Africa. S. c. nanus (the forest buffalo) is the smallest subspecies, common in forest areas of Central and West Africa, while S. c. brachyceros is in West Africa and S. c. aequinoctialis is in the savannas of East Africa."},
            {"name": "camel",
             "info": "A camel is an even-toed ungulate in the genus Camelus that bears distinctive fatty deposits known as 'humps' on its back. Camels have long been domesticated and, as livestock, they provide food (milk and meat) and textiles (fiber and felt from hair). Camels are working animals especially suited to their desert habitat and are a vital means of transport for passengers and cargo."},
            {"name": "chinchilla",
             "info": "Chinchillas are either of two species (Chinchilla chinchilla and Chinchilla lanigera) of crepuscular rodents of the parvorder Caviomorpha. They are slightly larger and more robust than ground squirrels, and are native to the Andes mountains in South America."},
            {"name": "cheetah",
             "info": "The cheetah (Acinonyx jubatus) is a large cat native to Africa and central Iran. It is the fastest land animal, capable of running at 80 to 128 km/h (50 to 80 mph), and as such has several adaptations for speed, including a light build, long thin legs and a long tail. Cheetahs typically reach 67–94 cm (26–37 in) at the shoulder, and the head-and-body length is between 1.1 and 1.5 m (3.6 and 4.9 ft). "},
            {"name": "coyote",
             "info": "The coyote (Canis latrans) is a species of canine native to North America. It is smaller than its close relative, the wolf, and slightly smaller than the closely related eastern wolf and red wolf. It fills much of the same ecological niche as the golden jackal does in Eurasia, though it is larger and more predatory, and it is sometimes called the American jackal by zoologists."},
            {"name": "cuckoo",
             "info": "The cuckoos are a family of birds, Cuculidae, the sole taxon in the order Cuculiformes. The cuckoo family includes the common or European cuckoo, roadrunners, koels, malkohas, couas, coucals and anis. The coucals and anis are sometimes separated as distinct families, the Centropodidae and Crotophagidae respectively. "},
            {"name": "deer",
             "info": "Deer or true deer are hoofed ruminant mammals forming the family Cervidae. The two main groups of deer are the Cervinae, including the muntjac, the elk (wapiti), the red deer, the fallow deer, and the chital; and the Capreolinae, including the reindeer (caribou), the roe deer, the mule deer, and the moose."},
            {"name": "elephant seal",
             "info": "Elephant seals are large, oceangoing earless seals in the genus Mirounga. The two species, the northern elephant seal (M. angustirostris) and the southern elephant seal (M. leonina), were both hunted to the brink of extinction by the end of the 19th century, but their numbers have since recovered."},
            {"name": "falcon",
             "info": "Falcons (/ˈfɒlkən, ˈfɔːl-, ˈfæl-/) are birds of prey in the genus Falco, which includes about 40 species. Falcons are widely distributed on all continents of the world except Antarctica, though closely related raptors did occur there in the Eocene."},
            {"name": "ferret",
             "info": "The ferret (Mustela putorius furo) is the domesticated form of the European polecat, a mammal belonging to the same genus as the weasel, Mustela, in the family Mustelidae. Their fur is typically brown, black, white, or mixed. They have an average length of 51 cm (20 in), including a 13 cm (5.1 in) tail, weigh about between 0.7 and 2.0 kg (1.5 and 4.4 lb), and have a natural lifespan of 7 to 10 years."},
            {"name": "flycatcher",
             "info": "The Old World flycatchers are a large family, the Muscicapidae, of small passerine birds mostly restricted to the Old World (Europe, Africa and Asia). These are mainly small arboreal insectivores, many of which, as the name implies, take their prey on the wing. The family includes 324 species and is divided into 51 genera."},
            {"name": "dog",
             "info": "The dog (Canis familiaris when considered a distinct species or Canis lupus familiaris when considered a subspecies of the wolf) is a domesticated carnivore of the family Canidae. It is part of the wolf-like canids, and is the most widely abundant terrestrial carnivore. The dog and the extant gray wolf are sister taxa as modern wolves are not closely related to the wolves that were first domesticated, which implies that the direct ancestor of the dog is extinct."},
            {"name": "cat",
             "info": "The cat (Felis catus) is a domestic species of small carnivorous mammal. It is the only domesticated species in the family Felidae and is often referred to as the domestic cat to distinguish it from the wild members of the family. A cat can either be a house cat, a farm cat or a feral cat; the latter ranges freely and avoids human contact. Domestic cats are valued by humans for companionship and their ability to hunt rodents."},
            {"name": "horse",
             "info": "The horse (Equus ferus caballus) is one of two extant subspecies of Equus ferus. It is an odd-toed ungulate mammal belonging to the taxonomic family Equidae. The horse has evolved over the past 45 to 55 million years from a small multi-toed creature, Eohippus, into the large, single-toed animal of today. "},
            {"name": "yak",
             "info": "The domestic yak (Bos grunniens) is a long-haired domesticated cattle found throughout the Himalayan region of the Indian subcontinent, the Tibetan Plateau, Northern Myanmar, Yunnan, Sichuan and as far north as Mongolia and Siberia. It is descended from the wild yak (Bos mutus)."},
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(ANIMAL) - 1)

        if animal is not None:
            user_animal = [m for m in ANIMAL if m.get("name").lower() == animal.lower()]

            if user_animal:
                response = user_animal[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know that. How about {}?"""]
                response = sntns[rand].format(ANIMAL[arand].get("name"))

        else:
            response = "Sorry?"
        dispatcher.utter_message(response)
        return [SlotSet("animal", None)]



##################################################################################
## chae 21 : action_nation // 국가 정보에 관한 행동
## 사용하는 슬롯 : nation
##################################################################################
class ActionNation(Action):

    def name(self) -> Text:
        return "action_nation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nation = tracker.get_slot('nation')

        NATION = [
            {"name": "China",
             "info": "China, officially the People's Republic of China (PRC), is a country in East Asia. It is the world's most populous country, with a population of around 1.4 billion in 2019. Covering approximately 9.6 million square kilometers (3.7 million mi2), it is the world's third or fourth largest country by area."},
            {"name": "India",
             "info": "India (Hindi: Bhārat), officially the Republic of India (Hindi: Bhārat Gaṇarājya),[23] is a country in South Asia. It is the second-most populous country, the seventh-largest country by land area, and the most populous democracy in the world. Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west"},
            {"name": "United States",
             "info": "The United States of America (USA), commonly known as the United States (US or U.S.) or America, is a country primarily located in central North America, between Canada and Mexico. It consists of 50 states, a federal district, five self-governing territories, and several other island possessions."},
            {"name": "Indonesia",
             "info": "Indonesia, officially the Republic of Indonesia is a country in Southeast Asia and Oceania, between the Indian and Pacific oceans. It consists of more than seventeen thousand islands, including Sumatra, Java, Borneo (Kalimantan), Sulawesi, and New Guinea (Papua)."},
            {"name": "Pakistan",
             "info": "Pakistan, officially the Islamic Republic of Pakistan, is a country in South Asia. It is the world's fifth-most populous country with a population exceeding 212.2 million. It has the world's second-largest Muslim population. It is the 33rd-largest country by area, spanning 881,913 square kilometres (340,509 square miles)."},
            {"name": "Brazil",
             "info": "Brazil (Portuguese: Brasil; Brazilian Portuguese: [bɾaˈziw]), officially the Federative Republic of Brazil (Portuguese: About this soundRepública Federativa do Brasil), is the largest country in both South America and Latin America. At 8.5 million square kilometers (3.2 million square miles) and with over 211 million people, Brazil is the world's fifth-largest country by area and the sixth most populous."},
            {"name": "Nigeria",
             "info": "Nigeria, officially the Federal Republic of Nigeria, is a sovereign country in West Africa bordering Niger in the north, Chad in the northeast, Cameroon in the east, and Benin in the west. Its southern coast is on the Gulf of Guinea in the Atlantic Ocean. Nigeria is a federal republic comprising 36 states and the Federal Capital Territory, where the capital, Abuja, is located."},
            {"name": "Bangladesh",
             "info": "Bangladesh, officially the People's Republic of Bangladesh, is a country in South Asia. It is the eighth-most populous country in the world, with a population exceeding 162 million people. In terms of landmass, Bangladesh ranks 92nd, spanning 148,460 square kilometres (57,320 sq mi), making it one of the most densely-populated countries in the world. Bangladesh shares land borders with India to the west, north, and east, Myanmar to the southeast, and the Bay of Bengal to the south."},
            {"name": "Russia",
             "info": "Russia, or the Russian Federation, is a transcontinental country located in Eastern Europe and Northern Asia. It extends from the Baltic Sea in the west to the Pacific Ocean in the east, and from the Arctic Ocean in the north to the Black Sea and the Caspian Sea in the south. Russia covers over 17,125,200 square kilometres (6,612,100 sq mi), spanning more than one-eighth of the Earth's inhabited land area, stretching eleven time zones, and bordering 16 sovereign nations."},
            {"name": "Mexico",
             "info": "Mexico, officially the United Mexican States, is a country in the southern portion of North America. It is bordered to the north by the United States; to the south and west by the Pacific Ocean; to the southeast by Guatemala, Belize, and the Caribbean Sea; and to the east by the Gulf of Mexico."},
            {"name": "Japan",
             "info": "Japan or Nihon is an island country in East Asia located in the northwest Pacific Ocean. It is bordered by the Sea of Japan to the west and extends from the Sea of Okhotsk in the north to the East China Sea and Taiwan in the south. Part of the Pacific Ring of Fire, Japan comprises an archipelago of 6,852 islands covering 377,975 square kilometers (145,937 sq mi); the country's five main islands, from north to south, are Hokkaido, Honshu, Shikoku, Kyushu, and Okinawa."},
            {"name": "Philippines",
             "info": "The Philippines, officially the Republic of the Philippines, is an archipelagic country in Southeast Asia. Situated in the western Pacific Ocean, it consists of about 7,641 islands that are broadly categorized under three main geographical divisions from north to south: Luzon, Visayas, Mindanao."},
            {"name": "Egypt",
             "info": "Egypt, officially the Arab Republic of Egypt, is a transcontinental country spanning the northeast corner of Africa and southwest corner of Asia by a land bridge formed by the Sinai Peninsula. Egypt is a Mediterranean country bordered by the Gaza Strip (Palestine) and Israel to the northeast, the Gulf of Aqaba and the Red Sea to the east, Sudan to the south, and Libya to the west."},
            {"name": "Ethiopia",
             "info": "Ethiopia, officially the Federal Democratic Republic of Ethiopia, is a landlocked country in East Africa. It shares borders with Eritrea to the north, Djibouti to the northeast, Somalia to the east, Kenya to the south, South Sudan to the west and Sudan to the northwest. With over 109 million inhabitants as of 2019, Ethiopia is the 12th most populous country in the world, the second most populous nation on the African continent (after Nigeria), and most populous landlocked country in the world. "},
            {"name": "Vietnam",
             "info": "Vietnam, officially the Socialist Republic of Vietnam, is a country in Southeast Asia and the easternmost country on the Indochinese Peninsula. With an estimated 96.2 million inhabitants as of 2019, it is the 15th most populous country in the world. Vietnam shares its land borders with China to the north, and Laos and Cambodia to the west."},
            {"name": "Iran",
             "info": "Iran, also called Persia, and officially the Islamic Republic of Iran, is a country in Western Asia. It is bordered to the west by Iraq, to the northwest by Turkey, Armenia, and Azerbaijan,[a] to the north by the Caspian Sea, to the northeast by Turkmenistan, to the east by Afghanistan and Pakistan, and to the south by the Gulf of Oman and the Persian Gulf. "},
            {"name": "Turkey",
             "info": "Turkey (Turkish: Türkiye [ˈtyɾcije]), officially the Republic of Turkey, is a transcontinental country located mainly on the Anatolian peninsula in Western Asia, with a smaller portion on the Balkan peninsula in Southeastern Europe. East Thrace, the part of Turkey in Europe, is separated from Anatolia by the Sea of Marmara, the Bosporus and the Dardanelles (collectively called the Turkish Straits)."},
            {"name": "Germany",
             "info": "Germany, officially the Federal Republic of Germany is a country in Central and Western Europe. Covering an area of 357,022 square kilometres (137,847 sq mi), it lies between the Baltic and North seas to the north, and the Alps to the south. It borders Denmark to the north, Poland and the Czech Republic to the east, Austria and Switzerland to the south, and France, Luxembourg, Belgium and the Netherlands to the west."},
            {"name": "France",
             "info": "France, officially the French Republic, is a country consisting of metropolitan France in Western Europe and several overseas regions and territories. The metropolitan area of France extends from the Rhine to the Atlantic Ocean and from the Mediterranean Sea to the English Channel and the North Sea. It borders Belgium, Luxembourg and Germany to the northeast, Switzerland, Monaco and Italy to the east and Andorra and Spain to the south."},
            {"name": "United Kingdom",
             "info": "The United Kingdom of Great Britain and Northern Ireland, commonly known as the United Kingdom (UK or U.K.) or Britain, is a sovereign country located off the north­western coast of the European mainland. The United Kingdom includes the island of Great Britain, the north­eastern part of the island of Ireland, and many smaller islands. Northern Ireland shares a land border with the Republic of Ireland."},
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(NATION) - 1)

        if nation is not None:
            user_nation = [m for m in NATION if m.get("name").lower() == nation.lower()]

            if user_nation:
                response = user_nation[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that place. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know where that is. How about {}?"""]
                response = sntns[rand].format(NATION[arand].get("name"))
        else:
            response = "Sorry?"
        dispatcher.utter_message(response)
        return [SlotSet("nation", None)]


##################################################################################
## chae 22 : ActionDisease // 질병 주제에 관한 발화
## 사용하는 슬롯 : disease
##################################################################################
class ActionDisease(Action):

    def name(self) -> Text:
        return "action_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disease = tracker.get_slot('disease')

        if (disease == 'covid-19'):
            disease == 'COVID'

        DISEASE = [
            {"name": "Coronary artery disease",
             "info": "Coronary artery disease (CAD), also known as coronary heart disease (CHD), ischemic heart disease (IHD), or simply heart disease, involves the reduction of blood flow to the heart muscle due to build-up of plaque (atherosclerosis) in the arteries of the heart. It is the most common of the cardiovascular diseases. Types include stable angina, unstable angina, myocardial infarction, and sudden cardiac death. A common symptom is chest pain or discomfort which may travel into the shoulder, arm, back, neck, or jaw. Occasionally it may feel like heartburn. "},
            {"name": "Stroke",
             "info": "A stroke is a medical condition in which poor blood flow to the brain causes cell death. There are two main types of stroke: ischemic, due to lack of blood flow, and hemorrhagic, due to bleeding. Both cause parts of the brain to stop functioning properly. Signs and symptoms of a stroke may include an inability to move or feel on one side of the body, problems understanding or speaking, dizziness, or loss of vision to one side. Signs and symptoms often appear soon after the stroke has occurred."},
            {"name": "Lower respiratory tract infection",
             "info": "Lower respiratory tract infection (LRTI) is a term often used as a synonym for pneumonia but can also be applied to other types of infection including lung abscess and acute bronchitis. Symptoms include shortness of breath, weakness, fever, coughing and fatigue. A routine chest X-ray is not always necessary for people who have symptoms of a lower respiratory tract infection."},
            {"name": "Chronic obstructive pulmonary disease",
             "info": "Chronic obstructive pulmonary disease (COPD) is a type of obstructive lung disease characterized by long-term breathing problems and poor airflow. The main symptoms include shortness of breath and cough with sputum production. COPD is a progressive disease, meaning it typically worsens over time. Eventually, everyday activities such as walking or getting dressed become difficult."},
            {"name": "Lung cancer",
             "info": "Lung cancer, also known as lung carcinoma, is a malignant lung tumor characterized by uncontrolled cell growth in tissues of the lung. This growth can spread beyond the lung by the process of metastasis into nearby tissue or other parts of the body. Most cancers that start in the lung, known as primary lung cancers, are carcinomas. The two main types are small-cell lung carcinoma (SCLC) and non-small-cell lung carcinoma (NSCLC). The most common symptoms are coughing (including coughing up blood), weight loss, shortness of breath, and chest pains."},
            {"name": "Diabetes",
             "info": "Diabetes mellitus (DM), commonly known as diabetes, is a group of metabolic disorders characterized by a high blood sugar level over a prolonged period of time. Symptoms often include frequent urination, increased thirst, and increased appetite. If left untreated, diabetes can cause many complications. Acute complications can include diabetic ketoacidosis, hyperosmolar hyperglycemic state, or death."},
            {"name": "Alzheimer's",
             "info": "Alzheimer's disease (AD), also referred to simply as Alzheimer's, is a chronic neurodegenerative disease that usually starts slowly and gradually worsens over time. It is the cause of 60–70% of cases of dementia. The most common early symptom is difficulty in remembering recent events. As the disease advances, symptoms can include problems with language, disorientation (including easily getting lost), mood swings, loss of motivation, not managing self-care, and behavioural issues. As a person's condition declines, they often withdraw from family and society."},
            {"name": "Diarrhea",
             "info": "Diarrhea, also spelled diarrhoea, is the condition of having at least three loose, liquid, or watery bowel movements each day. It often lasts for a few days and can result in dehydration due to fluid loss. Signs of dehydration often begin with loss of the normal stretchiness of the skin and irritable behaviour. This can progress to decreased urination, loss of skin color, a fast heart rate, and a decrease in responsiveness as it becomes more severe. Loose but non-watery stools in babies who are exclusively breastfed, however, are normal."},
            {"name": "Tuberculosis",
             "info": "Tuberculosis (TB) is an infectious disease usually caused by Mycobacterium tuberculosis (MTB) bacteria. Tuberculosis generally affects the lungs, but can also affect other parts of the body. Most infections show no symptoms, in which case it is known as latent tuberculosis. About 10% of latent infections progress to active disease which, if left untreated, kills about half of those affected. The classic symptoms of active TB are a chronic cough with blood-containing mucus, fever, night sweats, and weight loss."},
            {"name": "Cirrhosis",
             "info": "Cirrhosis, also known as liver cirrhosis or hepatic cirrhosis, is a condition in which the liver does not function properly due to long-term damage. This damage is characterized by the replacement of normal liver tissue by scar tissue. Typically, the disease develops slowly over months or years. Early on, there are often no symptoms. As the disease worsens, a person may become tired, weak, itchy, have swelling in the lower legs, develop yellow skin, bruise easily, have fluid buildup in the abdomen, or develop spider-like blood vessels on the skin. The fluid build-up in the abdomen may become spontaneously infected."},
            {"name": "Chickenpox",
             "info": "Chickenpox, also known as varicella, is a highly contagious disease caused by the initial infection with varicella zoster virus (VZV). The disease results in a characteristic skin rash that forms small, itchy blisters, which eventually scab over. It usually starts on the chest, back, and face. It then spreads to the rest of the body. Other symptoms may include fever, tiredness, and headaches. Symptoms usually last five to seven days."},
            {"name": "Diphtheria",
             "info": "Diphtheria is an infection caused by the bacterium Corynebacterium diphtheriae. Signs and symptoms may vary from mild to severe. They usually start two to five days after exposure. Symptoms often come on fairly gradually, beginning with a sore throat and fever. In severe cases, a grey or white patch develops in the throat. This can block the airway and create a barking cough as in croup. The neck may swell in part due to enlarged lymph nodes. A form of diphtheria which involves the skin, eyes or genitals also exists."},
            {"name": "AIDS",
             "info": "Human immunodeficiency virus infection and acquired immune deficiency syndrome (HIV/AIDS) is a spectrum of conditions caused by infection with the human immunodeficiency virus (HIV). Following initial infection a person may not notice any symptoms, or may experience a brief period of influenza-like illness. Typically, this is followed by a prolonged period with no symptoms. If the infection progresses, it interferes more with the immune system, increasing the risk of developing common infections such as tuberculosis, as well as other opportunistic infections, and tumors which are otherwise rare in people who have normal immune function."},
            {"name": "Malaria",
             "info": "Malaria is a mosquito-borne infectious disease that affects humans and other animals. Malaria causes symptoms that typically include fever, tiredness, vomiting, and headaches. In severe cases, it can cause yellow skin, seizures, coma, or death. Symptoms usually begin ten to fifteen days after being bitten by an infected mosquito. If not properly treated, people may have recurrences of the disease months later."},
            {"name": "Measles",
             "info": "Measles is a highly contagious infectious disease caused by measles virus. Symptoms usually develop 10–12 days after exposure to an infected person and last 7–10 days. Initial symptoms typically include fever, often greater than 40 °C (104 °F), cough, runny nose, and inflamed eyes. Small white spots known as Koplik's spots may form inside the mouth two or three days after the start of symptoms. A red, flat rash which usually starts on the face and then spreads to the rest of the body typically begins three to five days after the start of symptoms."},
            {"name": "Tetanus",
             "info": "Tetanus, also known as lockjaw, is a bacterial infection characterized by muscle spasms. In the most common type, the spasms begin in the jaw and then progress to the rest of the body. Each spasm usually lasts a few minutes. Spasms occur frequently for three to four weeks. Some spasms may be severe enough to fracture bones. Other symptoms of tetanus may include fever, sweating, headache, trouble swallowing, high blood pressure, and a fast heart rate. Onset of symptoms is typically three to twenty-one days following infection."},
            {"name": "Viral hepatitis",
             "info": "Viral hepatitis is liver inflammation due to a viral infection. It may present in acute form as a recent infection with relatively rapid onset, or in chronic form. The most common causes of viral hepatitis are the five unrelated hepatotropic viruses hepatitis A, B, C, D, and E. Other viruses can also cause liver inflammation, including cytomegalovirus, Epstein-Barr virus, and yellow fever. There also have been scores of recorded cases of viral hepatitis caused by herpes simplex virus."},
            {"name": "Salmonellosis",
             "info": "Salmonellosis is a symptomatic infection caused by bacteria of the Salmonella type. The most common symptoms are diarrhea, fever, abdominal cramps, and vomiting. Symptoms typically occur between 12 hours and 36 hours after exposure, and last from two to seven days. Occasionally more significant disease can result in dehydration. The old, young, and others with a weakened immune system are more likely to develop severe disease.[1] Specific types of Salmonella can result in typhoid fever or paratyphoid fever."},
            {"name": "Shingles",
             "info": "Shingles, also known as zoster or herpes zoster, is a viral disease characterized by a painful skin rash with blisters in a localized area. Typically the rash occurs in a single, wide stripe either on the left or right side of the body or face. Two to four days before the rash occurs there may be tingling or local pain in the area. Otherwise there are typically few symptoms though some may have fever or headache, or feel tired. The rash usually heals within two to four weeks; however, some people develop ongoing nerve pain which can last for months or years, a condition called postherpetic neuralgia (PHN). In those with poor immune function the rash may occur widely."},
            {"name": "COVID",
             "info": "Coronavirus disease 2019 (COVID-19) is a contagious respiratory and vascular (blood vessel) disease. It is caused by becoming infected with severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2), which is a specific type of coronavirus. Common symptoms include fever, cough, fatigue, shortness of breath or breathing difficulties, and loss of smell and taste. The incubation period, which is the time between becoming infected with the virus and showing symptoms, may range from one to fourteen days."},
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(DISEASE) - 1)

        if disease is not None:
            user_disease = [m for m in DISEASE if m.get("name").lower() == disease.lower()]

            if user_disease:
                response = user_disease[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know what that is. How about {}?"""]
                response = sntns[rand].format(DISEASE[arand].get("name"))
        else:
            response = "Pardon?"
        dispatcher.utter_message(response)
        return [SlotSet("disease", None)]

##################################################################################
## chae 23 : ActionSymptom // 증상 주제에 관한 발화
## 사용하는 슬롯 : symtom
##################################################################################
class ActionSymptom(Action):

    def name(self) -> Text:
        return "action_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptom = tracker.get_slot('symptom')

        SYMPTOM = [
            {"name": "Abdominal pain",
             "info": "Abdominal pain, also known as a stomach ache, is a symptom associated with both non-serious and serious medical issues. Common causes of pain in the abdomen include gastroenteritis and irritable bowel syndrome. About 15% of people have a more serious underlying condition such as appendicitis, leaking or ruptured abdominal aortic aneurysm, diverticulitis, or ectopic pregnancy. In a third of cases the exact cause is unclear."},
            {"name": "Chronic pain",
             "info": "Chronic pain is pain that lasts a long time. In medicine, the distinction between acute and chronic pain is sometimes determined by the amount of time since onset. Two commonly used markers are pain that continues at 3 months and 6 months since onset, but some theorists and researchers have placed the transition from acute to chronic pain at 12 months. Others apply the term acute to pain that lasts less than 30 days, chronic to pain of more than six months duration, and subacute to pain that lasts from one to six months."},
            {"name": "Fever",
             "info": "Fever, also referred to as pyrexia, is defined as having a temperature above the normal range due to an increase in the body's temperature set point. There is not a single agreed-upon upper limit for normal temperature with sources using values between 37.2 and 38.3 °C (99.0 and 100.9 °F) in humans. The increase in set point triggers increased muscle contractions and causes a feeling of cold."},
            {"name": "Paresthesia",
             "info": "Paresthesia is an abnormal sensation of the skin (tingling, pricking, chilling, burning, numbness) with no apparent physical cause. Paresthesia may be transient or chronic, and may have any of dozens of possible underlying causes. Paresthesias are usually painless and can occur anywhere on the body, but most commonly occur in the arms and legs."},
            {"name": "Shortness of breath",
             "info": "Shortness of breath (SOB), also known as dyspnea (BrE: dyspnoea) is a feeling of not being able to breathe well enough. The American Thoracic Society defines it as 'a subjective experience of breathing discomfort that consists of qualitatively distinct sensations that vary in intensity', and recommends evaluating dyspnea by assessing the intensity of the distinct sensations, the degree of distress involved, and its burden or impact on activities of daily living."},
            {"name": "Lightheadedness",
             "info": "Lightheadedness is a common and typically unpleasant sensation of dizziness or a feeling that one may faint. The sensation of lightheadedness can be short-lived, prolonged, or, rarely, recurring. In addition to dizziness, the individual may feel as though their head is weightless. The individual may also feel as though the room is 'spinning' or moving (vertigo) associated with lightheadedness."},
            {"name": "Anorexia ",
             "info": "Anorexia is a decreased appetite. While the term in non-scientific publications is often used interchangeably with anorexia nervosa, many possible causes exist for a decreased appetite, some of which may be harmless, while others indicate a serious clinical condition or pose a significant risk."},
            {"name": "Cachexia",
             "info": "Cachexia is a complex syndrome associated with an underlying illness causing ongoing muscle loss that is not entirely reversed with nutritional supplementation. A range of diseases can cause cachexia, most commonly cancer, congestive heart failure, chronic obstructive pulmonary disease, chronic kidney disease and AIDS. Systemic inflammation from these conditions can cause detrimental changes to metabolism and body composition."},
            {"name": "Convulsion",
             "info": "A convulsion is a medical condition where body muscles contract and relax rapidly and repeatedly, resulting in uncontrolled actions of the body. Because epileptic seizures typically include convulsions, the term convulsion is sometimes used as a synonym for seizure. However, not all epileptic seizures lead to convulsions, and not all convulsions are caused by epileptic seizures."},
            {"name": "Jaundice",
             "info": "Jaundice, also known as icterus, is a yellowish or greenish pigmentation of the skin and whites of the eyes due to high bilirubin levels. Jaundice in adults is typically a sign indicating the presence of underlying diseases involving abnormal heme metabolism, liver dysfunction, or biliary-tract obstruction."},
            {"name": "Arrhythmia",
             "info": "Arrhythmia, also known as cardiac arrhythmia or heart arrhythmia, is a group of conditions in which the heartbeat is irregular, too fast, or too slow. The heart rate that is too fast – above 100 beats per minute in adults – is called tachycardia, and a heart rate that is too slow – below 60 beats per minute – is called bradycardia."},
            {"name": "Bradycardia",
             "info": "Bradycardia is a condition typically defined wherein an individual has a resting heart rate of under 60 beats per minute (BPM) in adults, although some studies use a heart rate of less than 50 BPM. Bradycardia typically does not cause symptoms until the rate drops below 50 BPM. When symptomatic, it may cause fatigue, weakness, dizziness, sweating, and at very low rates, fainting."},
            {"name": "Xerostomia",
             "info": "Xerostomia, also known as dry mouth, is dryness in the mouth, which may be associated with a change in the composition of saliva, or reduced salivary flow, or have no identifiable cause. This symptom is very common and is often seen as a side effect of many types of medication. It is more common in older people (mostly because this group tend to take several medications) and in persons who breathe through their mouths."},
            {"name": "Nosebleed",
             "info": "A nosebleed, also known as epistaxis, is bleeding from the nose. Blood can also flow down into the stomach and cause nausea and vomiting. In more severe cases blood may come out of both nostrils. Rarely bleeding may be so significant low blood pressure occurs. Rarely the blood can come up the nasolacrimal duct and out from the eye."},
            {"name": "Bloating",
             "info": "Abdominal bloating is a symptom that can appear at any age, generally associated with functional gastrointestinal disorders or organic diseases, but can also appear alone. The person feels a full and tight abdomen. Although this term is usually used interchangeably with abdominal distension, these symptoms probably have different pathophysiological processes, which are not fully understood."},
            {"name": "Dysphagia",
             "info": "Dysphagia is difficulty in swallowing. Although classified under 'symptoms and signs' in ICD-10, in some contexts it is classified as a condition in its own right. It may be a sensation that suggests difficulty in the passage of solids or liquids from the mouth to the stomach, a lack of pharyngeal sensation or various other inadequacies of the swallowing mechanism."},
            {"name": "Hematemesis",
             "info": "Hematemesis is the vomiting of blood. The source is generally the upper gastrointestinal tract, typically above the suspensory muscle of duodenum. Patients can easily confuse it with hemoptysis (coughing up blood), although the latter is more common. Hematemesis 'is always an important sign'."},
            {"name": "Heartburn",
             "info": "Heartburn, also known as pyrosis, cardialgia or acid indigestion, is a burning sensation in the central chest or upper central abdomen. The discomfort often rises in the chest and may radiate to the neck, throat, or angle of the arm."},
            {"name": "Hair loss",
             "info": "Hair loss, also known as alopecia or baldness, refers to a loss of hair from part of the head or body. Typically at least the head is involved. The severity of hair loss can vary from a small area to the entire body. Inflammation or scarring is not usually present. Hair loss in some people causes psychological distress.["},
            {"name": "Rhinorrhea",
             "info": "Rhinorrhea or rhinorrhoea is the free discharge of a thin nasal mucus fluid. The condition, commonly known as a runny nose, occurs relatively frequently. Rhinorrhea is a common symptom of allergies (hay fever) or certain viral infections, such as the common cold. It can be a side effect of crying, exposure to cold temperatures, cocaine abuse[, or withdrawal, such as from opioids like methadone."},
        ]

        rand = random.randint(0, 2)
        arand = random.randint(0, len(SYMPTOM) - 1)

        if symptom is not None:
            user_symptom = [m for m in SYMPTOM if m.get("name").lower() == symptom.lower()]

            if user_symptom:
                response = user_symptom[0].get("info")
            else:
                sntns = ["""I am sorry but not sure about that. What about {}?""",
                         """Sorry, I'm not sure about that. I recommend you to search about {}.""",
                         """Sorry, I don't know what that is. How about {}?"""]
                response = sntns[rand].format(SYMPTOM[arand].get("name"))
        else:
            response = "Pardon?"
        dispatcher.utter_message(response)
        return [SlotSet("symptom", None)]

########################################################

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_custom_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_asking_rephrase")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]