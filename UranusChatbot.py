#Ref: https://github.com/NijatZeynalov/Scraper-Chatbot?tab=readme-ov-file 
#
# REMEMBER to pip install everything below from the terminal
# pip install pyttsx3 SpeechRecognition datetime wikipedia requests bs4 google-api-python-client oauth2client httplib2 googletrans

import pyttsx3
import speech_recognition
import datetime
import wikipedia
import webbrowser
import os
import time
import requests
from bs4 import BeautifulSoup
import re
import random
import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
from googletrans import Translator
from bs4 import BeautifulSoup
import holidays
import yfinance as yf
translator = Translator(service_urls=['translate.google.com','https://www.deepl.com/en/translator',])

b="Spartan: "
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greetings():
    h=int(datetime.datetime.now().hour)
    if h>8 and h<12:
        print(b,'Good Morning. My name is Spartan. Version 1.00')
        speak('Good morning. My name is Spartan. Version 1.00')
    elif h>=12 and h<17:
        print(b,"Good afternoon. My name is Spartan. Version 1.00")
        speak('Good afternoon. My name is Spartan. Version 1.00')
    else:
        print(b,'Good evening! My name is Spartan. Version 1.00')
        speak('Good evening My name is Spartan. Version 1.00')
    print(b,'How can I help you, EE104?')
    speak('How can I help you, EE104?')

motiv="Sometimes later becomes never. Do it now. EE104, I believe you, you have made me."
need_list=['EE104, what can I do for you?', 'Do you want something else?', 'EE104, give me questions or tasks', 'I want to take time with you, do you want to know something else?','EE104, what is on your mind?', 'I can not think like you-humans, but can give answer your all questions',"Let's discover this world! What do you want to learn today?" ]
sorry_list=['EE104, I am sorry I dont know the answer', 'I dont have an idea about it, EE104','Sorry, EE104! try again']
bye_list=['Good bye, EE104. I will miss you','See you EE104','Bye, dont forget I will always be here']
comic_list=['It is not a joke, EE104. I was serious','Do you think that it is a joke? Be nice!']
greet_list=['Hi EE104', 'Hi my dear']


# https://www.geeksforgeeks.org/how-to-extract-weather-data-from-google-in-python/ 
def weather_Spartan(city):
    import requests
    from bs4 import BeautifulSoup

    city=city.replace('weather','')

    try:

        # creating url and requests instance
        url = "https://www.google.com/search?q="+"weather"+city
        html = requests.get(url).content

        # getting raw data
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

        # formatting data
        data = str.split('\n')
        time = data[0]
        sky = data[1]

        # getting all div tag
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        strd = listdiv[5].text

        # getting other required data
        pos = strd.find('Wind')
        other_data = strd[pos:]

        # printing all data
        print("At ", city)
        print("Temperature is", temp)
        print("Time: ", time)
        print("Sky Description: ", sky)
        print(other_data)



    except:
        sorry=random.choice(sorry_list)
        print(b, sorry)
        speak(sorry)


def show_news_headlines(): #1
    try:
        url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        news_list = soup.findAll('item')[:5] 

        print("Here are the top news headlines:")
        for news in news_list:
            print("-", news.title.text)
            speak(news.title.text)
    except Exception as e:
        print("Sorry, I couldn't fetch the news headlines at the moment.")
        print(e)
def get_upcoming_holidays(days=60): #2
    today = datetime.date.today()
    upcoming_holidays = []
    us_holidays = holidays.US()
    
    for day in range(1, days + 1):
        potential_holiday = today + datetime.timedelta(days=day)
        if potential_holiday in us_holidays:
            upcoming_holidays.append(us_holidays[potential_holiday])
    return upcoming_holidays

def get_stock_price(symbol): #3
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period='1d')['Close'].iloc[-1]
        return price
    except Exception as e:
        return f"Failed to fetch the stock price for {symbol}: {e}"
    
def takeCommand():
    
    while True:
        print(" ")
        query=input("EE104: ")
        if 'who is' in query.lower():
            try:
                query=query.replace('who is','')
                result=wikipedia.summary(query, sentences=2)  #see more here https://www.geeksforgeeks.org/wikipedia-module-in-python/ 
                print(b,result)
                speak(result)
                need=random.choice(need_list)
                print(b, need)
                speak(need)
            except:
                sorry=random.choice(sorry_list)
                print(b, sorry)
                speak(sorry)
        elif 'hello'==query:
            greet=random.choice(greet_list)
            print(b, greet)
            speak(greet)
        elif 'news' in query.lower(): #checking news
            show_news_headlines()
            need = random.choice(need_list)
            print(b, need)
            speak(need) 
        elif 'holiday' in query or 'holidays' in query:
            upcoming_holidays = get_upcoming_holidays()
            if upcoming_holidays:
                print(b, "Here are some upcoming holidays in the next 60 days:")
                for holiday in upcoming_holidays:
                    print(b, f"- {holiday}")
                    speak(f"The upcoming holiday in the next 60 days is {holiday}")
            else:
                print(b, "There are no upcoming holidays within the next 60 days.")
                speak("There are no upcoming holidays within the next 60 days.")
        elif 'stock price' in query.lower():
            stocks = {'SP500': '^GSPC', 'Microsoft': 'MSFT', 'Google': 'GOOGL', 'Apple': 'AAPL', 'Tesla': 'TSLA'}
            for company, symbol in stocks.items():
                try:
                    price = get_stock_price(symbol)
                    price = round(price, 2)
                    print(f"The current price of {company}: {price}")
                    speak(f"The current price of {company}: {price}") 
                except Exception as e:
                    print(f"Failed to fetch the stock price for {company}: {e}") 
            need = random.choice(need_list)
            print(b, need)
            speak(need)
        elif 'play' in query.lower():
            query=query.replace('play','')
            url='https://www.youtube.com/results?search_query='+query
            webbrowser.open(url)
            time.sleep(2)
            speak('There are a lot of music, select one.')
            time.sleep(3)
            need=random.choice(need_list)
            print(b, need)
            speak(need)
        elif query=='exit' or query=="bye":
            bye=random.choice(bye_list)
            print(b, bye)
            speak(bye)
            break
        elif 'haha' in query:
            comic=random.choice(comic_list)
            print(b, comic)
            speak(comic)
        elif 'motivate' in query:
            print(b, motiv)
            speak(motiv)
        elif 'facebook' in query:
            url2='https://www.facebook.com/friends/requests/?fcref=jwl'
            webbrowser.open(url2)
        elif 'weather' in query.lower():
            weather_Spartan(query)
            need=random.choice(need_list)
            print(b, need)
            speak(need)
        elif 'shutdown laptop' in query.lower():
            os.system("shutdown /s /t 1");
        elif 'what is' in query.lower():
            try:
                query=query.replace('what is','')
                result=wikipedia.summary(query, sentences=2)  #see more here https://www.geeksforgeeks.org/wikipedia-module-in-python/ 
                print(b,result)
                speak(result)
                need=random.choice(need_list)
                print(b, need)
                speak(need)
            except:
                sorry=random.choice(sorry_list)
                print(b, sorry)
                speak(sorry)
    
        
        elif "when" or "how" or "is" or "are" in query:
            query=query.replace('when','')
            query=query.replace('how','')
            query=query.replace('who','')
            query=query.replace('is','')
            query=query.replace('are','')
            page2=requests.get("https://search.yahoo.com/search;_ylt=AwrOqlzV2QFmRC05hTpDDWVH;_ylc=X1MDMTE5NzgwNDg2NwRfcgMyBGZyAwRmcjIDcDpzLHY6c2ZwLG06c2Esc2FfbWs6MTMEZ3ByaWQDUHVRUDZTT09URU93TEEuVEpVV0Y1QQRuX3JzbHQDMARuX3N1Z2cDMTAEb3JpZ2luA3NlYXJjaC55YWhvby5jb20EcG9zAzEEcHFzdHIDZ2UEcHFzdHJsAzIEcXN0cmwDMTcEcXVlcnkDZ2VvcmdlJTIwd2FzaGluZ3RvbgR0X3N0bXADMTcxMTM5NzM1NAR1c2VfY2FzZQM-?p={search}&fr=sfp&fr2=p%3As%2Cv%3Asfp%2Cm%3Asa%2Csa_mk%3A13&iscqry=&mkr=13",query)
            
            soup=BeautifulSoup(page2.content, "html.parser")
            
            #name = soup.find("div",{"class":"dd algo fst AnswrsV2"})
            name = soup.find("div",{"class":"dd fst lst algo algo-sr relsrch richAlgo"})
            try:
                for link in name.findAll('a', attrs={'href': re.compile("^https://answers.yahoo.com/question")}):
                    a= (link.get('href'))
                    
                page1=requests.get(a)
                
                soup=BeautifulSoup(page1.content, "html.parser")
                
                name = soup.find("div",{"class":"AnswersList__container___3vQdv"}).text.replace("\n","").strip()
                temp=name.rsplit("Favorite Answer",1)
                temp=temp[1].split('.')
                
                for i in temp[:2]:
                    print(b, i)
                    speak(i)
                need=random.choice(need_list)
                print(b, need)
                speak(need)
            except Exception as e:
                sorry=random.choice(sorry_list)
                print(b, sorry)
                speak(sorry)
        
time.sleep(2)
print('Initializing...')
time.sleep(2)
print('Spartan is preparing...')
time.sleep(2)
print('Environment is building...')
time.sleep(2)
greetings()
takeCommand()
  
