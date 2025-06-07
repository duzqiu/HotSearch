from typing import Any
import scrapy
from urllib.parse import urlencode
import requests
from datetime import datetime
import time

from scrapy.http import Response


class SendBark:
    def __init__(self, key):
        self.key = key

    def send_t_c(self, title, content):
        self.url = f"https://api.day.app/{self.key}/{title}/{content}"
        requests.get(self.url)


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.com"]
    base_url = "https://weibo.com/ajax/side/searchBand"
    params = {
        "type": "hot", # hot-热搜 mine-我的
        "last_tab": "hot",
        "last_tab_time": str(time.time()).split(".")[0]
    }
    url = f"{base_url}?{urlencode(params)}"
    cookies = {
        "SUB":"_2AkMQ67k-f8NxqwFRmf8czWrlbY9yyAnEieKmt0jlJRMxHRl-yT9xqhQLtRB6O2uX0dKCEqWssn81NmN1RDZ6iLPGnXt7",
        "SUBP": "0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5uL9nx.FLwOfrwNTwByMBX",
        "SINAGLOBAL": "5257790297634.743.1740060224397",
        "ULV": "1740060224502:1:1:1:5257790297634.743.1740060224397:",
        "XSRF-TOKEN": "wNMDWJzIa629dOB3vbn5_46E",
        "WBPSESS": "wmtK4rVYDqg_ZQgKuCoP3sxSHrkVI9Z8imWEBurptik4G_j42TdnnFd5cl2Y9DJ-STZLJB_XNacggYe5FOEMDZTsu4qFfm8WzduWVCrzi-Xjt-KCT4m8QtiX3YHNsalFvpX-EUgrYKR44FN2yFhwaB7wwn47GtBMvz_kVAtZJNc="
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, cookies=self.cookies, callback=self.parse, method='GET')

    def parse(self, response: Response, **kwargs: Any) -> Any:
        wb_hot_data = response.json()['data']
        hot_gov = wb_hot_data['hotgov']['name'].replace("#","@")
        new_list = []
        for real_time in wb_hot_data['realtime']:
            new_list.append(real_time['word'])

        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M")
        title = f"微博热搜 {formatted}"

        content = f"""
🏆{hot_gov}

🥇{new_list[0]}

🥈{new_list[1]}

🥉{new_list[2]}

4️⃣{new_list[3]}

5️⃣{new_list[4]}

6️⃣{new_list[5]}

7️⃣{new_list[6]}

8️⃣{new_list[7]}

9️⃣{new_list[8]}

🔟{new_list[9]}
        """
        print(content)
        key = "UZ9juRSNtAMpnzWEQokJYF"
        bark = SendBark(key)
        bark.send_t_c(title, content)


