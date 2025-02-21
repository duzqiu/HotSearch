import scrapy
#from scrapy_splash import SplashRequest
from urllib.parse import urlencode
import requests
from datetime import datetime

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
        for i in range(15):
            new_list.append(response.json()["data"][i]['Title'])
        key = "UZ9juRSNtAMpnzWEQokJYF"
        
        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M")
        title = f"头条热榜 {formatted}"
        content = f"""
🏆{new_list[0]}

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
        bark = SendBark(key)
        bark.send_t_c(title, content)


