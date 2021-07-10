import scrapy
import json
import pytz
from datetime import datetime
import requests

DIVIDENTS_CONTRACT = "cx203d9cd2a669be67177e997b8948ce2c35caffae"

class txDetail(scrapy.Item):
    txHash = scrapy.Field()
    date = scrapy.Field()
    BALN_claimed = scrapy.Field()
    bnUSD_claimed = scrapy.Field()
    sICX_claimed = scrapy.Field()


def getpagecount(user_address):
    page_count = 0
    url = f'https://tracker.icon.foundation/v3/address/txList?page=1&count=1&address={user_address}'
    res = requests.get(url).json()
    if res["totalSize"] % 100 != 0:
        page_count = int(1 + (res["totalSize"] / 100))
    return page_count


class TxSpider(scrapy.Spider):
    name = "iconTx"
    start_urls = ['https://tracker.icon.foundation/']
    headers = {
        "authority": "tracker.icon.foundation",
        "method": "GET",
        "scheme": "https",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Mobile Safari/537.36"
    }

    def __init__(self, address='', **kwargs):  # The category variable will have the input URL.
        super().__init__(**kwargs)
        self.userAddress = address
        self.pageCount = any

    custom_settings = {'FEED_URI': 'outputfile.json',
                       'CLOSESPIDER_TIMEOUT': 0}

    def parse(self, response):
        self.pageCount = getpagecount(self.userAddress)
        for page in range(1, self.pageCount + 1, 1):
            url = f'https://tracker.icon.foundation/v3/address/txList?page={page}&count=100&address={self.userAddress}'
            yield scrapy.Request(url,
                                 callback=self.parse_json,
                                 headers=self.headers)

    def parse_json(self, response):
        raw_data = response.body
        data = json.loads(raw_data)

        for tx in data["data"]:
            if datetime.strptime(tx["createDate"][:10], "%Y-%m-%d") < datetime.strptime("2021-07-01",
                                                                                                     "%Y-%m-%d"):
                break
            else:
                if tx['toAddr'] == DIVIDENTS_CONTRACT:
                    tx_hash = tx['txHash']
                    yield scrapy.Request(
                        f"https://tracker.icon.foundation/v3/transaction/txDetail?txHash={tx_hash}",
                        callback=self.parse_Tx,
                        headers=self.headers,
                    )

    def parse_Tx(self, response):
        data = json.loads(response.body)
        yield txDetail(
            txHash=data["data"]["txHash"],
            date=data["data"]["createDate"],
            BALN_claimed=data["data"]["tokenTxList"][0]["quantity"],
            bnUSD_claimed=data["data"]["tokenTxList"][1]["quantity"],
            sICX_claimed=data["data"]["tokenTxList"][2]["quantity"],
        )
