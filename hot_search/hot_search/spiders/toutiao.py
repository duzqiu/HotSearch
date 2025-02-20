import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urlencode
import requests

class SendBark:
    def __init__(self, key):
        self.key = key

    def send_t_c(self, title, content):
        self.url = f"https://api.day.app/{self.key}/{title}/{content}"
        requests.get(self.url)

class ToutiaoSpider(scrapy.Spider):
    name = "toutiao"
    allowed_domains = ["toutiao.com"]
    base_url = "https://www.toutiao.com/hot-event/hot-board/"
    params = {
        "origin": "toutiao_pc",
        "_signature": "_02B4Z6wo00901vT9yYgAAIDCE.2en18RBNL02c0AANqVEIvz9cMx2zoZxvPsiiDsn54EeZCrLWwuGED-O85.I7udeWSbMkOxtZelfOtaXbVAdZX3UBhXMN2o4BWqZ2MjraVG4CaycB2ctUa586"
    }
    url = f"{base_url}?{urlencode(params)}"
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, method='GET')

    def parse(self, response):
        new_list = []
        for i in range(10):
            new_list.append(response.json()["data"][i]['Title'])
        key = "UZ9juRSNtAMpnzWEQokJYF"
        title = "今日头条热榜"
        content = f"""
{new_list[0]}

{new_list[1]}

{new_list[2]}

{new_list[3]}

{new_list[4]}

{new_list[5]}

{new_list[6]}

{new_list[7]}

{new_list[8]}

{new_list[9]}
        """
        bark = SendBark(key)
        bark.send_t_c(title, content)


