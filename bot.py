# -*- coding: utf-8 -*-
import redis
import os
import telebot
import math
import random
import threading
import info
import test
from telebot import types
from emoji import emojize
from pymongo import MongoClient
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

games={}

client1=os.environ['database']
client=MongoClient(client1)
db=client.god
user=db.users
token=db.tokens
mob=db.mobs

def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)


те боту /start!')
    
    
@bot.message_handler(commands=['start'])
def start(m):
    x=user.find_one({'id':m.from_user.id})
    if x==None:      
        user.insert_one({'id':m.from_user.id,
                         'name':m.from_user.first_name,
                         'win':0,
                         'loose':0,
                         'games':0,
                         'red':0,
                         'blue':0,
                         'yellow':0,
                         'agent':0,
                         'killer':0,
                         'glavar':0,
                         'prohojii':0,
                         'primanka':0,
                         'mirotvorets':0,
                         'gangster':0,
                         'podrivnik':0,
                         'redprimanka':0,
                         'telohranitel':0,
                         'alive':0
                        })
        print('Юзер создал аккаунт! Его имя: '+m.from_user.first_name)
    x=m.text.split('/start')
    if len(x)==2:
       try:
        if m.from_user.id==m.chat.id:
         if m.from_user.id not in games[int(x[1])]['players']:
          if len(games[int(x[1])]['players'])<10:
           if int(x[1])<0:
            i=0              
            if games[int(x[1])]['play']==0:
                games[int(x[1])]['players'].update(createuser(m.from_user.id, m.from_user.first_name))
                text=''           
                for ids in games[int(x[1])]['players']:
                    if games[int(x[1])]['players'][ids]['id']==m.from_user.id:
                        player=games[int(x[1])]['players'][ids]
                bot.send_message(m.from_user.id, 'Вы успешно присоединились!')
                b=0
                for g in games[int(x[1])]['players']:
                    text+=games[int(x[1])]['players'][g]['name']+'\n'
                    b+=1
                medit('Игроки: '+str(b)+'\n\n*'+text+'*', games[int(x[1])]['id'], games[int(x[1])]['users'])
                games[int(x[1])]['userlist']+=text+'\n'
                bot.send_message(games[int(x[1])]['id'], player['name']+' присоединился!')
          else:
            bot.send_message(m.from_user.id, 'Слишком много игроков! Мест не осталось!')
       except:
        if m.chat.id==m.from_user.id:
            bot.send_message(m.from_user.id, 'Игра crossfire')

            
@bot.message_handler(commands=['extend']) 
def extendd(m):
    if m.chat.id in games:
        if games[m.chat.id]['play']!=1:
            if m.from_user.id in games[m.chat.id]['players']:
                x=m.text.split('/extend')
                if len(x)==2:
                    try:
                        if int(x[1])>=1:
                            games[m.chat.id]['timebeforestart']+=int(x[1])
                            if games[m.chat.id]['timebeforestart']>=300:
                                games[m.chat.id]['timebeforestart']=300
                                bot.send_message(m.chat.id, 'Время до начала перестрелки увеличено! Осталось 5 минут.')
                            else:
                                bot.send_message(m.chat.id, 'Время до начала перестрелки увеличено на '+x[1]+'! Осталось '+str(games[m.chat.id]['timebeforestart'])+' секунд.')
                        else:
                            x=bot.get_chat_administrators(m.chat.id)
                            i=10
                            for z in x:       
                                if m.from_user.id==z.user.id:
                                    i=1
                                else:
                                    if i!=1:
                                        i=10
                            if i==1:
                                games[m.chat.id]['timebeforestart']+=int(x[1])
                                a=x[1]
                                if games[m.chat.id]['timebeforestart']<=0:
                                    pass
                                else:
                                    bot.send_message(m.chat.id,'Время до начала перестрелки увеличено на '+a+'! Осталось '+str(games[m.chat.id]['timebeforestart'])+' секунд.')
                            else:
                                bot.send_message(m.chat.id, 'Только администратор может использовать эту команду!')
                    except:
                        games[m.chat.id]['timebeforestart']+=30
                        if games[m.chat.id]['timebeforestart']>=300:
                            games[m.chat.id]['timebeforestart']=300
                        bot.send_message(m.chat.id, 'Время до начала перестрелки увеличено на 30! Осталось '+str(games[m.chat.id]['timebeforestart'])+' секунд.')
                else:
                    games[m.chat.id]['timebeforestart']+=30
                    if games[m.chat.id]['timebeforestart']>=300:
                            games[m.chat.id]['timebeforestart']=300
                    bot.send_message(m.chat.id, 'Время до начала перестрелки увеличено на 30! Осталось '+str(games[m.chat.id]['timebeforestart'])+' секунд.')
    
            
@bot.message_handler(commands=['flee'])
def flee(m):
    if m.chat.id in games:
     if games[m.chat.id]['play']!=1:
      if m.from_user.id in games[m.chat.id]['players']:
        del games[m.chat.id]['players'][m.from_user.id]
        text=''
        for g in games[m.chat.id]['players']:
            text+=games[m.chat.id]['players'][g]['name']+'\n'
        bot.send_message(m.chat.id, m.from_user.first_name+' сбежал!')
        medit('Игроки: \n\n*'+text+'*', m.chat.id, games[m.chat.id]['users'])
  


@bot.message_handler(commands=['players'])
def playerss(m):
    if m.chat.id in games:
        bot.send_message(m.chat.id, 'Вот список игроков', reply_to_message_id=games[m.chat.id]['users'])

            
def secnd(id):
    games[id]['timebeforestart']-=1
    if games[id]['timebeforestart']<=0:
        begin(id)
    else:
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/crossfirebot?start='+str(id)))
        if games[id]['timebeforestart']==180:
            msg=bot.send_message(id, 'Осталось 3 минуты! Жмите "Присоединиться", чтобы поучаствовать в перестрелке!', reply_markup=Keyboard)
            games[id]['todel'].append(msg.message_id)
        elif games[id]['timebeforestart']==60:
            msg=bot.send_message(id, 'Осталось 60 секунд! Жмите "Присоединиться", чтобы поучаствовать в перестрелке!', reply_markup=Keyboard)
            games[id]['todel'].append(msg.message_id)
        elif games[id]['timebeforestart']==30:
            msg=bot.send_message(id, 'Осталось 30 секунд! Жмите "Присоединиться", чтобы поучаствовать в перестрелке!', reply_markup=Keyboard)
            games[id]['todel'].append(msg.message_id)
        elif games[id]['timebeforestart']==10:
            msg=bot.send_message(id, 'Осталось 10 секунд! Жмите "Присоединиться", чтобы поучаствовать в перестрелке!', reply_markup=Keyboard)
            games[id]['todel'].append(msg.message_id)
        t=threading.Timer(1, secnd, args=[id])
        t.start()
            
            
@bot.message_handler(commands=['startgame'])
def startgame(m):
  if m.chat.id<0:
    if m.chat.id not in games:
        games.update(creategame(m.chat.id))  
        tt=threading.Timer(1, secnd, args=[m.chat.id])
        tt.start()
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/crossfirebot?start='+str(m.chat.id)))
        msg=bot.send_message(m.chat.id, m.from_user.first_name+' Начал(а) игру! Жмите кнопку ниже, чтобы присоединиться', reply_markup=Keyboard)
        msg2=bot.send_message(m.chat.id, 'Игроки:\n', parse_mode='markdown')
        games[m.chat.id]['users']=msg2.message_id
        for ids in games:
            if games[ids]['id']==m.chat.id:
                game=games[ids]
        game['todel'].append(msg.message_id)
    else:
      if games[m.chat.id]['play']==0:
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/warofwildsbot?start='+str(m.chat.id)))
        msg=bot.send_message(m.chat.id, 'Игра уже запущена! Жмите "присоединиться"!', reply_markup=Keyboard)
        for ids in games:
            if games[ids]['id']==m.chat.id:
                game=games[ids]
        game['todel'].append(msg.message_id)
  else:
    bot.send_message(m.chat.id, 'Играть можно только в группах!')
    
   
def begin(id):
  if id in games:
   if games[id]['play']==0:
    if len(games[id]['players'])>=2:
        for ids in games[id]['todel']:
            try:
                bot.delete_message(id, ids)
            except:
                pass
        i=1
        for ids in games[id]['players']:
            games[id]['players'][ids]['number']=i
            i+=1
        bot.send_message(id, 'Игра начинается!')
        games[id]['play']=1
        xod(games[id])
    else:
        for ids in games[id]['todel']:
            try:
                bot.delete_message(id, ids)
            except:
                pass
        bot.send_message(id, 'Недостаточно игроков!')
        try:
            del games[id]
        except:
            pass

        
@bot.message_handler(commands=['forcestart'])
def forcem(m):
  if m.chat.id in games:
    i=0
    x=bot.get_chat_administrators(m.chat.id)
    for z in x:       
        if m.from_user.id==z.user.id:
           i=1
        else:
            if i!=1:
                i=10
    if i==1:
        if m.chat.id in games:
            games[m.chat.id]['timebeforestart']=1
    else:
        bot.send_message(m.chat.id, 'Только администратор может использовать эту команду!')
        
        

def xod(game):
    pass
        
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
   pass

     
        
def creategame(id):
    return {id:{
        'players':{},
        'id':id,
        'todel':[],
        'toedit':[],
        'play':0,
        'timebeforestart':300,
        'users':None,
        'userlist':'Игроки:\n\n'
    }
           }
        

def createuser(id, name):
    return{id:{
        'role':None,
        'name':name,
        'id':id,
        'number':None,
        'text':'',
        'shuffle':0,
        'target':None,
        'target2':None,
        'killed':0,
        'cankill':0,
        'defence':0,
        'killany':None,
        'killany2':None,
        'candef':0,
        'blue':0,
        'red':0,
        'yellow':0,
        'win':0,
        'golos':1,
        'message':0,
        'picks':2,
        'killedby':[]
    }
          }
    
                      
                      
                      



while True:
   
    try:
        bot.polling()
    except(ReadTimeout, ConnectionError):
        pass


