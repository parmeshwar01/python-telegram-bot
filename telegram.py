import os
import random
import telebot
import requests
import json
import praw


API_KEY = os.getenv('API_KEY')
CHAT_ID = os.getenv('CHAT_ID')
WEATHER_KEY = os.getenv('WEATHER_KEY')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
username = os.getenv('username')
password = os.getenv('password')

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['greet'])
def greet(message):
  bot.reply_to(message,"Hey! how are you?")


"""
getting user_id
@bot.message_handler(commands=['chatid'])
def chst(message):
  userid = message.from_user.id
  bot.reply_to(message,userid)  """





@bot.message_handler(commands=['dog'])
def dog(message):
  contents = requests.get('https://random.dog/woof.json').json()    
  url = contents['url']
  chat_id = CHAT_ID
  bot.send_photo(chat_id=chat_id, photo=url)


@bot.message_handler(commands=['meme'])
def meme(message):
  reddit = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    username=username,
                    password=password,
                    user_agent="anything")
  subreddit= reddit.subreddit("dankmemes")   

  all_subs =[]
  top = subreddit.top(limit=50)
  for submission in top:
    all_subs.append(submission) 
  random_sub= random.choice(all_subs)
  url = random_sub.url  
  chat_id = CHAT_ID                 
  bot.send_photo(chat_id=chat_id, photo=url)



  """dice"""   
@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
  
  if message.text[0:4]=="dice":
    dice = [
        str(random.choice(range(1, 7)))
        for _ in range(int(message.text[5:6]))
    ]
    
    bot.reply_to(message, ', '.join(dice))


  elif message.text[0:7]=="weather":
      BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
      CITY = message.text[8:len(message.text)]
      URL = BASE_URL + "q=" + CITY + "&appid=" + WEATHER_KEY
      response = requests.get(URL)
      if response.status_code == 200:
          data = response.json()
  
          main = data['main']
          wind = data['wind']
          con = data['sys']
          temperature = int(main['temp'])-273
          humidity = main['humidity']
          w = wind['speed']
          pressure = main['pressure']
          contury = con['country']
          report = data['weather']

          bot.reply_to(message,f"{CITY:-^30} \n Temperature: {temperature}°C \n Humidity : {humidity}% \n Pressure:{pressure}Pa \n {report[0]['description']} \n Wind : {w}mps \n Country : {contury}")
   
      else:

          bot.reply_to(message,"city not found")

  elif message.text[0:4]=="cool":
    url = "https://cool-name-api.glitch.me/coolify?name=" +  message.text[5:len(message.text)]
    r = requests.get(url).json()
    bot.reply_to(message,f"{r['cool_name_alphanum']} \n \n {r['cool_name_square']} \n \n {r['cool_name_symbolic']} \n \n {r['cool_name_upsidedown']} \n \n {r['cool_name_doublestruck']} \n \n {r['cool_name_xabovebelow']} \n \n {r['cool_name_unicodemix']} \n \n {r['cool_name_emoji']} ")



bot.polling()            
   
