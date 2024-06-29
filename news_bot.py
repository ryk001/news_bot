from pyshorteners import Shortener
from dateutil.parser import parse
from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import requests
import re
import os

class news_bot():
    def __init__(self, token, keywords):
        self.__token=token
        self.__keywords=keywords

    def get_news(self, keyword):

        # empty
        title=[]
        url=[]
        source=[]
        time=[]

        # fetch news data
        period = '3d' if dt.datetime.today().weekday() == 0 else '1d'
        res = requests.get(f'https://news.google.com/search?q="{keyword}"%20when%3A{period}&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant')
        if res.status_code != 200:
            return pd.DataFrame()
        
        content = res.content
        soup = BeautifulSoup(content, "html.parser")

        # title & url
        for item in soup.find_all("a", class_="JtKRv"):
            title.append(str(item.get_text()))
            try:
                url.append(Shortener().tinyurl.short(item.get('href').replace('.', 'https://news.google.com', 1)))
            except:
                url.append(item.get('href').replace('.', 'https://news.google.com', 1))

        # source
        for item in soup.find_all("div", class_="vr1PYe"):
            source.append(item.get_text())

        # time
        for item in soup.find_all("div", class_="UOVeFe"):
            time.append(re.sub(r'(\b\d\b) 小時前', r'0\1 小時前', item.find("time").get_text()))

        # collect as df
        df = pd.DataFrame({
            'keyword':[keyword] * len(title),
            'title': title,
            'time': time,
            'source': source,
            'url': url,
        })

        # only relevant news
        useless_news = ['對帳單', '加權指數', '盤中焦點股', '熱門']
        df = df[(~df['title'].str.contains('|'.join(useless_news))) & (df['title'].str.contains(keyword.split(' ')[0]))]

        # only finance source
        relevant_source = ['中時新聞網', '工商時報', '經濟日報', '自由財經', 'Yahoo奇摩新聞', 'Anue鉅亨', 'ETtoday財經雲']
        df = df[df['source'].isin(relevant_source)]

        # return news_dataframe
        return df\
            .sort_values(by='time', ascending=True)\
            .reset_index(drop=True)

    def generate_message(self, df):
        keyword = df['keyword'][0]
        message = f'*{keyword}*\n'
        for i in range(len(df)):
            title = df["title"][i]
            time = df["time"][i]
            source = df["source"][i]
            url = df["url"][i]

            message += f"\n{title}\n{time}{' | '}{source}\n{url}\n"
        return message

    def send_message(self, msg):
        headers = {
            "Authorization": f"Bearer {self.__token}",
            "Content-Type" : "application/x-www-form-urlencoded"
            }
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return r.status_code

    def send_news(self):
        for keyword in self.__keywords:
            df = self.get_news(keyword)
            if not df.empty:
                msg = self.generate_message(df)
                self.send_message(msg)

# send news with keywords
token = os.environ['LINE_NOTIFY_TOKEN'] # token
keywords = os.environ['KEYWORDS'].split('\n') # keywords
bot = news_bot(token, keywords)
bot.send_news()
