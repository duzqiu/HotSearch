from typing import Any
import scrapy
import requests
from scrapy.http import Response
from datetime import datetime


class SendBark:
    def __init__(self, key):
        self.key = key

    def send_t_c(self, title, content):
        self.url = f"https://api.day.app/{self.key}/{title}/{content}"
        requests.get(self.url)

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    url = "https://www.baidu.com"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, method='GET')

    def parse(self, response: Response, **kwargs: Any) -> Any:
        baidu_search_list = response.xpath("//ul[@id='hotsearch-content-wrapper']")
        new_list = []
        for baidu_search in baidu_search_list.xpath('.//li'):
            new_list.append(baidu_search.xpath('.//a/span[2]/text()').get().replace("#", "@"))
        # print(new_list)
        key = "UZ9juRSNtAMpnzWEQokJYF"

        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M")
        title = f"百度热搜 {formatted}"
        content = f"""
🏆{new_list[0]}

🥈{new_list[2]}

🥉{new_list[4]}

4️⃣{new_list[6]}

5️⃣{new_list[8]}

6️⃣{new_list[1]}

7️⃣{new_list[3]}

8️⃣{new_list[5]}

9️⃣{new_list[7]}

🔟{new_list[9]}
            """
        # print(content)
        bark = SendBark(key)
        bark.send_t_c(title, content)