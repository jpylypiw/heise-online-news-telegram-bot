from datetime import datetime
from html.parser import HTMLParser
from threading import Thread
from time import sleep

import requests
import xmltodict

from bot import Bot
from config import Config
from log import Log
from users import Users


class News(object):

    def __init__(self, configpath, newspath, userspath, dispatcher):
        self.newsconfig = Config(newspath)
        self.users = Users(userspath)
        self.log = Log(configpath)
        self.bot = Bot(configpath, userspath)
        self.stopflag = False
        self.dispatcher = dispatcher

    def get_rss_content(self):
        url = self.newsconfig.get_value("NEWS", "url")
        headers = {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "Sec-Fetch-User": "?1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Referer": "https://www.heise.de/news-extern/news.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "de-DE,de;q=0.9,en-GB;q=0.8,en;q=0.7"
        }
        return requests.get(url, headers=headers).text

    def start_thread(self):
        thread = Thread(target=self.run_thread, args=())
        thread.start()

    def check_for_news(self):
        xml = self.get_rss_content()
        news = xmltodict.parse(xml)
        news = news["feed"]["entry"]
        last_news_id = self.newsconfig.get_value("NEWS", "last_id")
        if last_news_id == "":
            last_news_id = news[0]["id"]
            self.newsconfig.set_value("NEWS", "last_id", last_news_id)
        if news[0]["id"] != last_news_id:
            self.send_news(news, last_news_id)

    def send_news(self, newsdict, last_news_id):
        for news in newsdict:
            if news["id"] == last_news_id:
                break
            else:
                for chat_id in self.users.get_user_list():
                    title = news["title"]["#text"]
                    published = datetime.fromisoformat(news["published"])
                    published = "{0:%d.%m.%Y %H:%M}".format(published)
                    description = news["summary"]["#text"]
                    url_article = "[To Article](" + news["link"]["@href"] + ")"
                    html_parser = ImgParse()
                    html_parser.feed(news["content"]["#text"])
                    url_image = html_parser.img_src
                    url_image = "[To Image](" + url_image + ")"
                    text = "*" + title + "*\n" + published + "\n\n" + description + "\n\n" + url_image + " - " + url_article
                    self.bot.send_message(chat_id, text, self.dispatcher.bot.send_message, "Markdown", False)
                self.newsconfig.set_value("NEWS", "last_id", news["id"])

    def run_thread(self):
        slept = 60
        while True:
            if not self.stopflag:
                sleep(1)
                slept = slept + 1
                if slept >= 60:
                    self.check_for_news()
                    slept = 0
            else:
                break


class ImgParse(HTMLParser):
    img_src = ""

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.img_src = dict(attrs)["src"]

    def error(self, message):
        raise message
