import math
from pybit.unified_trading import HTTP
import pandas as pd
import log

logger = log.log_set_up()

class Non_trade():

    session = HTTP(testnet=False)

    def get_current_coin_price(self, coin_symbol):
        print("get_current_coin_price_func\n")
        current_coin_data = self.session.get_tickers(
            category="linear",
            symbol=coin_symbol,
        )

        current_coin_data

        if current_coin_data["result"]["list"][0]["markPrice"]:
            current_coin_price = float(current_coin_data["result"]["list"][0]["markPrice"])
        else:
            current_coin_price = None
            logger.info('get_current_coin_price failed')
        return current_coin_price

    def get_coin_qty_limit(self, coin_symbol):
        print("get_coin_qty_limit_func\n")
        qty_limit_data = self.session.get_instruments_info(
            category="linear",
            symbol=coin_symbol,
        )

        if qty_limit_data["result"]["list"][0]["lotSizeFilter"]:
            min_qty = qty_limit_data["result"]["list"][0]["lotSizeFilter"]["minOrderQty"]
            max_qty = qty_limit_data["result"]["list"][0]["lotSizeFilter"]["maxOrderQty"]
            min_price = qty_limit_data["result"]["list"][0]["priceFilter"]["minPrice"]
            max_price = qty_limit_data["result"]["list"][0]["priceFilter"]["maxPrice"]
        else:
            min_qty = None
            max_qty = None
            min_price = None
            max_price = None
            logger.info('get_current_coin_price failed')
        return min_qty, max_qty, min_price, max_price

    def get_instruments_info(self,coin_symbol):
        print("get_instruments_info_func\n")
        l = self.session.get_instruments_info(
            category="linear",
            symbol=coin_symbol)
        status = l["result"]["list"][0]["status"]
        maxLeverage = float(l["result"]["list"][0]["leverageFilter"]["maxLeverage"])
        minPrice = str(l["result"]["list"][0]["priceFilter"]["minPrice"])
        maxPrice = str(l["result"]["list"][0]["priceFilter"]["maxPrice"])
        maxMktOrderQty = str(l["result"]["list"][0]["lotSizeFilter"]["maxMktOrderQty"])
        minOrderQty = str(l["result"]["list"][0]["lotSizeFilter"]["minOrderQty"])
        fundingInterval = l["result"]["list"][0]["fundingInterval"]

        data = {
                "status":status,
                "maxLeverage":maxLeverage,
                "minPrice":minPrice,
                "maxPrice":maxPrice,
                "maxMktOrderQty":maxMktOrderQty,
                "minOrderQty":minOrderQty,
                "fundingInterval":fundingInterval
                }
        pd_data = pd.DataFrame([data])
        return pd_data

class Trade_adjustments():
    def __init__(self, pd_data):
        self.pd_data = pd_data
        self.min_price = self.pd_data.loc[0, "minPrice"]
        self.max_price = self.pd_data.loc[0, "maxPrice"]
        self.maxMktOrderQty = self.pd_data.loc[0, "maxMktOrderQty"]
        self.minOrderQty = self.pd_data.loc[0, "minOrderQty"]

    def prices_adjust_range(self, user_prices):
        print("prices_adjust_range_func\n")
        # 將用戶價格調整至有效範圍內
        if user_prices < float(self.min_price):
            user_prices = float(self.min_price)
        elif user_prices > float(self.max_price):
            user_prices = float(self.max_price)
        else:
            decimal_count = len(self.min_price.split('.')[1]) if '.' in self.min_price else 0
            user_prices = round(user_prices, decimal_count)
        print(f"min_price:{self.min_price},max_price:{self.max_price}")

        return user_prices

    # 略過這裡的程式碼，因為這部分沒有問題

    def qty_adjust_range(self,split_no ,max_num, min_num , total_num):
        print("qty_adjust_range_func\n")
        #判定分拆次數
        if max_num > float(self.maxMktOrderQty):
            print(f"max_num > float(self.maxMktOrderQty)")
            min_split_count = max_num / float(self.maxMktOrderQty)
            min_split_count = math.floor(min_split_count)
            print(f"min_split_count:{min_split_count}")

            if split_no > min_split_count:
                print(f"split_no > min_split_count")
                split_no = split_no

            else:
                print(f"split_no < min_split_count")
                split_no = min_split_count

        elif min_num < float(self.minOrderQty):
            print("min_num < float(self.minOrderQty)")
            split_no = math.floor(total_num /float(self.minOrderQty))

        else:
            print("no need to split order")
            split_no =  split_no

        return split_no

    def bit_adjust_range(self,split_no, min_num ,total_num):

        print("bit_adjust_range_func\n")
        if min_num < 5: #min 5 usdt in one order
            print("min_num < 5")
            split_no = math.floor(total_num / 5)
        else:
            split_no = split_no

        return split_no

    def qty_decimel_adjust(self,qty):
        print("qty_decimel_adjust_func\n")
        if '.' in (self.minOrderQty):
            print("place1：數量是分拆後qty是小數，平台限制不是整數")
            parts = (self.minOrderQty).split('.')[1]
            print("len:",len(parts))
            if int(parts) > 0:
                l = len((parts))
                print(f"len:{len(parts)}")
                qty = round(qty, l)
                print(f"split_qty：{qty}")
        else:
            print("place2：數量是分拆後qty是小數，平台限制是整數")

            qty = round(qty,0)
            qty = int(qty)

        return qty

if __name__ == '__main__':
    coin_symbol = "BTCUSDT"
    pd_data = Non_trade().get_instruments_info(coin_symbol)
    print(f"pd_data:{pd_data}")
    max_num = float(pd_data.loc[0, 'maxMktOrderQty'])
    min_num = 10
    total_num = 100
    split_no = 10

    split_no = Trade_adjustments(pd_data).qty_adjust_range(split_no ,max_num, min_num , total_num)
    print(f"split_no:{split_no}")
