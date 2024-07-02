from pybit.unified_trading import HTTP
import log
import pandas as pd

logger = log.log_set_up()

class Trade():

    def __init__(self, Acc_name, api_key, api_secret):
        self.Acc_name = Acc_name
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = HTTP(
                testnet=False,
                api_key=self.api_key,
                api_secret=self.api_secret,
            )
        self.order_id_to_check = None
        self.order_status = None

    def update_order_status(self,order_ids):

        updated_order_ids = order_ids.copy()  # 复制字典，避免修改原始字典

        for order_type, order_info in order_ids.items():

            print ("order_type:",order_type,"order_info:",order_info)
            order_id = order_info['orderID']

            if order_id != None:  # 如果orderID不为None，则尝试获取订单状态
                order_status = self.session.get_open_orders(
                    category="linear",
                    orderId=order_id,  # 注意这里是order_id，而不是order_ids
                )

                if order_status != None and "result" in order_status and "list" in order_status["result"] and \
                        order_status["result"]["list"]:

                    updated_order_ids[order_type]["order_status"] = order_status["result"]["list"][0]["orderStatus"]

              # 如果orderID为None，则说明可能是旧单，需要进一步确认
                # 假设你有一个函数叫做get_order_history来获取历史订单信息
                # 你需要根据你的实际情况来实现这个函数
            elif order_id != None:

                order_history = self.session.get_order_history(
                    category="linear",
                    orderId=order_id,  # 注意这里是order_id，而不是order_ids
                )
                updated_order_ids[order_type]["order_status"] = order_history["result"]["list"][0]["orderStatus"]

            else:
                pass

        return updated_order_ids


    def active_order(self,coin_symbol,side ,qty
                     ,price,order_type): #開倉


        Real_trade = self.session.place_order(
            category='linear',
            symbol=coin_symbol,
            side= side,
            orderType= order_type,
            qty=str(qty),
            price=str(price)
        )

        try:
            Real_trade

            logger.info(f"（開倉）買價:{coin_symbol},{side}'，數量：{qty}買價：{price}")
            if Real_trade['retMsg'] == 'OK':
                logger.info(f'{self.Acc_name}交易{coin_symbol}成功！！！')
            else:
                logger.info(f'Warning！！！{self.Acc_name}交易{coin_symbol}失敗！！！')

            order_data = Real_trade['result']
            return order_data

        except Exception as e:

            logger.info(f'{self.Acc_name}沒有{coin_symbol}數量可減少或平倉！！！{e}')
            pass


    def cancel_order(self, coin_symbol, cancel_order_ID):

        try:
            cancel_active_order = self.session.cancel_order(
                category="linear",
                symbol=coin_symbol,
                orderId=cancel_order_ID,
            )
            logger.info('Real_trade result is:%s' % (cancel_active_order))
            if cancel_active_order['retMsg'] == 'OK':
                logger.info(f'{self.Acc_name}取消訂單成功！！！')
            else:
                logger.info(f'Warning！！！{self.Acc_name}取消{coin_symbol}訂單失败！！！')
            # 添加取消结果到结果列表中
            trade_data =  cancel_active_order['result']

            return trade_data
        except Exception as e:
            # 记录异常信息
            logger.error(f"{self.Acc_name}沒有{coin_symbol}訂單可減少！！！: {e}")
            pass


    def change_order(self,coin_symbol,order_type, change_price , change_order_ID):
        print("change_order_func\n")
        print(f"order_type:{order_type}")

        if order_type == "add_order" or order_type == "flat_order":
            print("add_order or flat_order")
            try:
                amend_order = self.session.amend_order(
                    category="linear",
                    symbol=coin_symbol,
                    orderId=change_order_ID,
                    # qty="0.15",
                    price= str(change_price),
                    )

                amend_order

                logger.info(f'{self.Acc_name}改變{coin_symbol}訂單成功！！！')
                amend_order_data = {
                    'change_order_ID': amend_order['result']['orderId'],
                }

            except Exception as e:

                logger.error(f"{self.Acc_name}沒有{coin_symbol}訂單可減少！！！: {e}")
                pass

        elif order_type == "SP":
            print("SP")
            print(f"coin_symbol:{coin_symbol},change_order_ID:{change_order_ID},change_price:{change_price}")
            try:
                amend_order = self.session.amend_order(
                    category="linear",
                    symbol=coin_symbol,
                    orderId=change_order_ID,
                    # qty="0.15",
                    triggerPrice=str(change_price),
                )

                amend_order

                logger.info(f'{self.Acc_name}改變{coin_symbol}訂單成功！！！')
                amend_order_data = {
                    'change_order_ID': amend_order['result']['orderId'],
                }

            except Exception as e:

                logger.error(f"{self.Acc_name}沒有{coin_symbol}訂單可減少！！！: {e}")
                pass

        elif order_type == "SL":
            print("SL")
            try:
                amend_order = self.session.amend_order(
                    category="linear",
                    symbol=coin_symbol,
                    orderId=change_order_ID,
                    # qty="0.15",
                    triggerPrice=str(change_price)
                )

                amend_order

                logger.info(f'{self.Acc_name}改變{coin_symbol}訂單成功！！！')
                amend_order_data = {
                    'change_order_ID': amend_order['result']['orderId'],
                }

            except Exception as e:

                logger.error(f"{self.Acc_name}沒有{coin_symbol}訂單可減少！！！: {e}")
                pass


    def get_all_tickers(self):
        open_orders_data = self.session.get_tickers(
            category="linear",
        )
        print(open_orders_data)

    def wallet_balance(self):
        print("wallet_balance_func\n")
        get_positions = self.session.get_positions(
            category="linear",
            settleCoin="USDT",
            limit=100
        )

        total_position_val = 0.0  # 初始化总余额为浮点数0.0

        # 获取 positions 列表
        positions_list = get_positions["result"]["list"]
        # 遍历 positions 列表，并计算总余额
        for position in positions_list:
            total_position_val += float(position["positionValue"])  # 将字符串转换为浮点数

        wallet_balance_info = self.session.get_wallet_balance(
            accountType="UNIFIED",
        )
        total_equity = float(wallet_balance_info["result"]["list"][0]["totalEquity"])

        return total_position_val, total_equity

    def check_orders(self, coin_symbol):
        print("check_orders_func\n")
        if coin_symbol != "ALL":
            get_open_orders = self.session.get_open_orders(
                category="linear",
                symbol=coin_symbol,
                openOnly=0,
                limit=1000,
            )
        else:
            get_open_orders = self.session.get_open_orders(
                category="linear",
                settleCoin="USDT",
                openOnly=0,
                limit=1000,
            )
        check_orders = get_open_orders["result"]["list"]
        return check_orders

    def order_type(self, check_orders , position_side , p):
        new_orders = [order['orderId'] for order in check_orders if (order['side'] == position_side or position_side == None ) and order["price"] == str(p) ]
        return new_orders

    def get_position_value(self, coin_symbol):
        print("get_position_value_func\n")
        if coin_symbol == "ALL":
            get_position_data = self.session.get_positions(
                category="linear",
                settleCoin="USDT"
            )
            coin_list = get_position_data["result"]["list"]
            if coin_list == []:
                print("no_coins_holding")
                return None

            else:

                symbol = get_position_data["result"]["list"][0]["symbol"]
                avg_price = get_position_data["result"]["list"][0]["avgPrice"]
                position_size = float(get_position_data["result"]["list"][0]["size"])
                position_side = get_position_data["result"]["list"][0]["side"]
                position_val = float(get_position_data["result"]["list"][0]["positionValue"])

        else:

            get_position_data = self.session.get_positions(
                category="linear",
                symbol = coin_symbol,
            )

            symbol = get_position_data["result"]["list"][0][ "symbol"]
            avg_price = get_position_data["result"]["list"][0]["avgPrice"]

            if avg_price == "" or avg_price == "0" or avg_price == "0.0":
                position_size = 0
                position_side = None
                position_val = 0

            else:
                position_size = float(get_position_data["result"]["list"][0]["size"])
                position_side = get_position_data["result"]["list"][0]["side"]
                position_val = float(get_position_data["result"]["list"][0][ "positionValue"])

        data = {
            'coins_symbol': [symbol],
            'avg_price':[avg_price],
            'qty': [position_size],
            'side': [position_side],
            'total_val': [position_val]
        }

        df_position_val = pd.DataFrame(data)

        return df_position_val

class Order_type_class(Trade):

    def __init__(self, acc_name, api_key, api_secret):
        super().__init__(acc_name, api_key, api_secret)

    def check_hv_position_func(self, coin_symbol):
        df_position_val = self.get_position_value(coin_symbol)
        position_val = float(df_position_val.loc[0, 'total_val'])
        position_side = df_position_val.loc[0, 'side']
        if position_val > 0 or position_val != "":
            hv_position = True
        else:
            position_side = None
            hv_position = False

        return hv_position, position_side

    def new_orders_func(self, check_orders, position_side):
        print("new_orders_func\n")
        return [order['orderId'] for order in check_orders if (order['side'] == position_side or position_side == None)]

    def flat_orders_func(self,check_orders, hv_position, position_side):
        if position_side == "Buy":
            flat_side = "Sell"
        elif position_side == "Sell":
            flat_side = "Buy"
        else:
            flat_side = None

        return [order['orderId'] for order in check_orders if order['side'] == flat_side and hv_position == True and order['stopOrderType'] == "" ]

    def SP_orders_func(self,check_orders):
        return [order['orderId'] for order in check_orders if order['stopOrderType'] == "TakeProfit"]

    def SL_orders_func(self,check_orders):
        return [order['orderId'] for order in check_orders if order['stopOrderType'] == "StopLoss"]

    def type_of_orders_cancel_func(self, coin_symbol):
        check_orders = self.check_orders(coin_symbol)
        hv_position, position_side = self.check_hv_position_func(coin_symbol)
        print("find_out which type of orders do u need\n")
        new_orders = self.new_orders_func(check_orders, position_side)
        flat_orders = self.flat_orders_func(check_orders, hv_position, position_side)
        SP_orders = self.SP_orders_func(check_orders)
        SL_orders = self.SL_orders_func(check_orders)

        return new_orders , flat_orders,SP_orders ,SL_orders

    def check_specific_orders_func(self,orderID):
        check_specific_orders = self.session.get_open_orders(
            category="linear",
            orderId=orderID,
        )

        check_specific_orders

        return check_specific_orders

    def check_old_orders_func(self,orderID):
        check_old_orders = self.session.get_order_history(
            category="linear",
            orderId=orderID,
        )

        check_old_orders

        return check_old_orders

    def define_order_status_func(self,orderID):
        check_new_orders = self.check_specific_orders_func(orderID)
        if check_new_orders['result']['list'] != []:
            order_status = check_new_orders["result"]["list"][0]["orderStatus"]

        else:
            check_old_orders = self.check_old_orders_func(orderID)
            order_status = check_old_orders["result"]["list"][0]["orderStatus"]
        # print(f"old_order_status:{old_order_status}")
        return order_status

if __name__ == '__main__':
    # real_acc
    # acc_name = "Fa"
    # Api_key = "Z94F3wUEkimNlSFUuh"
    # Api_secret = "ubRoQf6lNyy7T6eUcSc9i2sGNrrcApKsyhbj"

    # testnet
    acc_name = "test"
    Api_key = "Spm9ezsVIdKTpVuFc1"
    Api_secret = "24jbLNUNsc2tpLUHarItASOvcMvEmeYuRORp"
    Trade_instance = Trade(acc_name, Api_key, Api_secret)
    coin_symbol = "DOGEUSDT"
    side = "Buy"
    qty = "60"
    price = "0.11"
    order_type = "Limit"

    Order_type_instance = Order_type_class(acc_name, Api_key, Api_secret)

    # order_ID = Trade_instance.active_order(coin_symbol,side ,qty,price,order_type)
    coin_symbol = "DOGEUSDT"
    check_orders = Trade_instance.check_orders(coin_symbol)
    print(f"check_orders:{check_orders}")
    for order in check_orders:
        order_ids = order['orderId']
    print(f"order_ids:{order_ids}type{type(order_ids)}")
    order_status = Order_type_instance.define_order_status_func(order_ids)
    print(f"order_status:{order_status}{type(order_status)}")
    # check_specific_orders = Order_type_instance.check_specific_orders_func(order_ids)
    # check_old_orders = Order_type_instance.check_old_orders_func(order_ids)
    # print(f"check_specific_orders:{check_specific_orders},check_old_orders:{check_old_orders}")
    # order_status = Order_type_instance.define_order_status_func(order_ids)
    # print(f"order_status:{order_status}")
    # trade_data = Trade_instance.cancel_order(coin_symbol,order_ids)
    # print(f"trade_data['orderId']:{trade_data['orderId']}{type(trade_data['orderId'])}")

