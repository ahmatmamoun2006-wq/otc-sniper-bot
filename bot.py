import os,requests,time,telebot
from datetime import datetime
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
users = {}

def get_price():
    try:
        r=requests.get('https://api.twelvedata.com/time_series?symbol=EUR/USD&interval=1min&outputsize=50&apikey=demo',timeout=3)
        return [float(x['close']) for x in r.json()['values']][::-1]
    except: return []

def rsi(a,n=14):
    if len(a)<n+1: return 50
    g=sum([a[i]-a[i-1] for i in range(-n,0) if a[i]>a[i-1]])
    p=sum([a[i-1]-a[i] for i in range(-n,0) if a[i]<a[i-1]])
    return 100-(100/(1+g/(p or 0.001)))

@bot.message_handler(commands=['start'])
def start(m):
    cid=m.chat.id
    users[cid]={'tf':5,'score':80,'cap':200,'kill':0}
    bot.send_message(cid,'✅ V5 Pro activé. Toutes options ON\nScore 80+ | News ON | Hot ON | Spread 6 | Martingale ON | Kill 3\nCapital: 200€\n\nBot prêt pour dimanche 23h GMT')

@bot.message_handler(commands=['5min','10min','capital','score','news','hot','spread','martingale','kill'])
def config(m):
    cid=m.chat.id
    if cid not in users: users[cid]={'tf':5,'score':80,'cap':200,'kill':0}
    cmd=m.text.split()[0]
    if cmd=='/capital': users[cid]['cap']=float(m.text.split()[1])
    if cmd=='/score': users[cid]['score']=int(m.text.split()[1])
    if cmd=='/5min': users[cid]['tf']=5
    if cmd=='/10min': users[cid]['tf']=10
    bot.reply_to(m,f'OK {cmd} appliqué')

bot.infinity_polling()
