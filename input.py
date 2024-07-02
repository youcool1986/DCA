import pandas as pd
import re
class active_orders():

    def __init__(self):
        self.randomize = False
        self.test = "请输入 (1) test 或 (2) real: "
        self.coin = "币种（例如：BTC, ETH）： "
        self.order_type = "订单类型 (1) Limit or (2) Market："
        self.capital_ratio = "佔資本比率：， 1 - 100 ："
        self.flat = " (1)平倉  或 （2)加倉: "
        self.side = "请输入 (1) Buy 或 (2) Sell："
        self.price = "請輸入訂單限價價格："
        self.Accs = "請輸入 Acc_Name (輸入空白結束) , all ＝ 全部: "

    def test_real_acc_input(self):

        while True:
            user_input = input(self.test).strip().lower()

            if user_input == '1':
                user_input = "New_Testnet_Api_Acc_name.xlsx"
                return user_input

            elif user_input == '2':
                user_input = "New_Api_Acc_name.xlsx"
                return user_input

            else:
                print("输入无效，请重新输入。")

    def coin_input(self):

        while True:
            user_input = input(self.coin).upper()
            if user_input.isalpha():  # 检查是否只包含英文字母
                coin_symbol = user_input + "USDT"
                return coin_symbol
            else:
                print("输入错误，请只输入英文。")

    def flat_input(self):
        while True:
            user_input = input(self.flat).capitalize()
            if user_input == "1":
                user_input = True
                side = "flat"
                return user_input, side

            elif user_input == "2":
                user_input = False
                side = ""
                return user_input, side

            else:
                print("输入错误，请重新输入。")

    def side_input(self , side):
        while True:
            if side == "flat":
                user_input = ""
                return user_input

            else:
                user_input = input(self.side).capitalize()
                if user_input == "1":
                    user_input = "Buy"
                    return user_input

                elif user_input == "2":
                    user_input = "Sell"
                    return user_input

                else:
                    print("输入无效，请重新输入。")

    def order_type_input(self):
        while True:
            user_input = input(self.order_type).capitalize()
            if user_input == "1":
                user_input = "Limit"
                return user_input
            elif user_input == "2":
                user_input = "Market"
                return user_input
            else:
                print("输入错误，请重新输入。")

    def price_input(self , order_type):
        if order_type == "Market":
            limit_price = "現價"

        else:
            while True:
                ltd_price = float(input(self.price).replace(" ", ""))  # 去除空格
                try:
                    limit_price = float(ltd_price)

                except ValueError:
                    print("输入内容不符合要求，请重新输入。")

                return limit_price

        return limit_price

    def capital_ratio_input(self):

        while True:
            user_input = int(input(self.capital_ratio))
            if 1 <= user_input <= 100:
                return user_input
            else:
                print("输入不在范围内，请重新输入。")

    def Acc_name_input(self,test_real):

        Accs = []  # 儲存使用者輸入的 Acc_Name

        try:
            # 讀取 Excel 檔案
            first_df = pd.read_excel(test_real)

        except Exception as e:
            print(f"讀取 Excel 檔案時出現錯誤：{e}")

        # 使用迴圈不斷讓使用者輸入
        Acc_name_data = first_df['Acc_Name'].tolist()
        print(Acc_name_data)

        while True:
            user_input = input(self.Accs)

            if user_input == "":
                break
            elif user_input.upper() == "ALL":
                Accs = Acc_name_data.copy()
                break
            elif user_input in Acc_name_data:
                Accs.append(user_input)

            else:
                print("输入错误，请重新输入。")

        return Accs

    def confirm_input(self, confirmed):
        print(confirmed)

        while True:
            confirm = input("确认输入是否正确？(Y/N): ").strip().lower()

            if confirm == "y":
                return True
            elif confirm == "n":
                return False
            else:
                print("无效输入，请输入 Y 或 N。")

    def execute_all(self):
        # 按顺序执行所有方法

        test_real_result = self.test_real_acc_input()
        print(f"test_real_result:{test_real_result}")

        if test_real_result == "New_Testnet_Api_Acc_name.xlsx":
            test_real_str = "測試"
        else:
            test_real_str = "真實"

        coin_input_result = self.coin_input()

        flat_input_result,side_result = self.flat_input()

        if flat_input_result == True:
            flat_input_str = "平倉"
        else:
            flat_input_str = "加倉"

        side_input_result = self.side_input(side_result)

        if side_input_result == 'Buy':
            side_str = "買入"
        elif side_input_result == 'Sell':
            side_str = "沽出"

        elif side_input_result == "":
            side_str = "平倉"

        order_type_result = self.order_type_input()

        if order_type_result == 'Limit':
            order_type_str = "限價"
        else:
            order_type_str = "市價"

        price_result = self.price_input(order_type_result)

        capital_ratio_result = self.capital_ratio_input()

        acc_name_result = self.Acc_name_input(test_real_result)

        confirmed = self.confirm_input("\n"
                                        f"這是一個{test_real_str}交易\n"
                                       f"{acc_name_result}\n"
                                       f"({flat_input_str}) ({capital_ratio_result})%的資產\n"
                                       f"以({order_type_str}) ({price_result})的價格 "
                                       f"({side_str}) ({coin_input_result}) \n"
                                       )

        if confirmed:
            print("输入确认成功，继续执行其他操作...")
            return test_real_result,coin_input_result,flat_input_result,\
                   side_input_result,order_type_result,price_result,\
                   capital_ratio_result,acc_name_result
            # 在这里执行其他操作
        else:
            print("输入不正确，请重新输入。")


class random_split_orders(active_orders):

    def __init__(self):
        super().__init__()
        self.randomize = True
        self.split_no = "請輸入分拆數量 整數 1 - 5000: "
        self.time_index = "请输入(時間單位)整數數字 1 , 2 , 1200....: "
        self.time_unit ="请输入(時間單位) '1' sec, '2' min , '3' hour' ,'4' day: "
        self.price_range = "請輸入下單價格 波動範圍 1 - 100 (%): "

    # 删除 confirm_input 方法，以继承自父类的实现

    def split_no_input(self):
        while True:
            user_input = input(self.split_no).strip()
            try:
                split_number = int(user_input)
                if 1 <= split_number <= 5000:
                    return split_number
                else:
                    print("输入的数字不在有效范围内，请输入 1 到 5000 之间的整数。")
            except ValueError:
                print("输入无效，请输入有效的整数。")

    def time_index_input(self):
        while True:
            user_input = input(self.time_index)
            try:
                integer_input = int(user_input)
                return integer_input
            except ValueError:
                print("输入无效，请输入一个整数。")

    def time_unit_input(self):
        valid_units = {
            '1': 'sec',
            '2': 'min',
            '3': 'hour',
            '4': 'day'
        }
        while True:
            user_input = input(self.time_unit).strip()
            if user_input in valid_units:
                return valid_units[user_input]
            else:
                print("输入无效，请输入有效的时间单位（'1', '2', '3', '4'）。")

    def price_range_input(self):
        while True:
            user_input = input(self.price_range).strip()
            try:
                price_range = int(user_input)
                if 1 <= price_range <= 100:
                    price_range = price_range / 100
                    return price_range
                else:
                    print("输入的数字不在有效范围内，请输入 1 到 100 (%) 之间的数值。")
            except ValueError:
                print("输入无效，请输入有效的数值。")

    def execute_all(self):
        test_real_result = self.test_real_acc_input()

        if test_real_result == "New_Testnet_Api_Acc_name.xlsx":
            test_real_str = "Test"
        else:
            test_real_str = "Real"

        coin_input_result = self.coin_input()

        flat_input_result, side_result = self.flat_input()

        if flat_input_result == True:
            flat_input_str = "平倉"
        else:
            flat_input_str = "加倉"

        side_input_result = self.side_input(side_result)

        if side_input_result == 'Buy':
            side_str = "買入"
        elif side_input_result == 'Sell':
            side_str = "沽出"
        elif side_input_result == "":
            side_str = "平倉"

        order_type_result = self.order_type_input()

        if order_type_result == 'Limit':
            order_type_str = "限價"
        else:
            order_type_str = "市價"

        price_result = self.price_input(order_type_result)

        capital_ratio_result = self.capital_ratio_input()

        acc_name_result = self.Acc_name_input(test_real_result)

        split_no_result = self.split_no_input()

        time_index_result = self.time_index_input()

        time_unit_result = self.time_unit_input()

        price_range_result = self.price_range_input()

        confirmed = self.confirm_input("\n"
                                       f"這是一個隨機分注版的({test_real_str})交易\n"
                                       f"{acc_name_result}\n"
                                       f"({flat_input_str}) ({capital_ratio_result})%的資產\n"
                                       f"以({order_type_str}) ({price_result})的價格，價格闊度{price_range_result} "
                                       f"({side_str}) ({coin_input_result}) \n"
                                       f"分({split_no_result})注，以({time_index_result}{time_unit_result})進行"
                                       )

        if confirmed:
            print("输入确认成功，继续执行其他操作...\n")
            return test_real_result, coin_input_result, flat_input_result, \
                   side_input_result, order_type_result, price_result, \
                   capital_ratio_result, acc_name_result, split_no_result, \
                   time_index_result, time_unit_result, price_range_result
        else:
            print("输入不正确，请重新输入。\n")

class cancel_orders(active_orders):

    def __init__(self):
        super().__init__()
        self.order_type = "请输 取消 的訂單類別 (1)平倉 (2)加倉 (3)止盈 (4)止損："
        self.price = "请输入 （訂單价格）: "

    def c_order_type_input(self):

        while True:
            user_input = input(self.order_type).capitalize()
            if user_input == "1":
                user_input = "flat_order"
                return user_input

            elif user_input == "2":
                user_input = "add_order"
                return user_input

            elif user_input == "3":
                user_input = "SP"
                return user_input

            elif user_input == "4":
                user_input = "SL"
                return user_input

            else:
                print("输入错误，请重新输入。")

    def c_price_input(self , c_order_type_result):

        if c_order_type_result == "SP" or c_order_type_result == "SL":

            user_input = "SPSL"

            return user_input

        else:
            while True:
                try:
                    user_input = float(input(self.price))

                    if user_input < 0:
                        print("价格不能为负数，请重新输入。")
                        continue

                    return user_input

                except ValueError:
                    print("输入无效，请输入数字。")


    def execute_all(self):

        test_real_result = self.test_real_acc_input()
        print(f"test_real_result:{test_real_result}")

        if test_real_result == "New_Testnet_Api_Acc_name.xlsx":
            test_real_str = "Test"
        else:
            test_real_str = "Real"

        coin_input_result = self.coin_input()

        c_order_type_result = self.c_order_type_input()

        c_price_result = self.c_price_input(c_order_type_result)

        if c_order_type_result == 'flat_order':
            c_order_type_str = "限價"
        elif c_order_type_result == 'add_order':
            c_order_type_str = "加倉"
        elif c_order_type_result == 'SP':
            c_order_type_str = "止盈"
        elif c_order_type_result == 'SL':
            c_order_type_str = "止損"

        acc_name_result = self.Acc_name_input(test_real_result)

        confirmed = self.confirm_input("\n"
                                       f"這是一個{test_real_str}交易\n"
                                       f"{acc_name_result}\n"
                                       f"將要取消({coin_input_result})\n"
                                       f"的價格為({c_price_result}) 的({c_order_type_str})的訂單\n"
                                       )

        if confirmed:
            print("输入确认成功，继续执行其他操作...")
            return test_real_result, coin_input_result, c_order_type_result, \
                   c_price_result, acc_name_result

            # 在这里执行其他操作

        else:
            print("输入不正确，请重新输入。")

class change_orders(cancel_orders):

    def __init__(self):
        super().__init__()
        self.change_p = "请输入 （更改後价格）: "

    def change_price_input(self):

        while True:
            try:
                user_input = float(input(self.change_p))

                if user_input < 0:
                    print("价格不能为负数，请重新输入。")
                    continue

                return user_input

            except ValueError:
                print("输入无效，请输入数字。")

    def execute_all(self):

        test_real_result = self.test_real_acc_input()
        print(f"test_real_result:{test_real_result}")

        if test_real_result == "New_Testnet_Api_Acc_name.xlsx":
            test_real_str = "Test"
        else:
            test_real_str = "Real"

        coin_input_result = self.coin_input()

        c_order_type_result = self.c_order_type_input()

        if c_order_type_result == 'flat_order':
            c_order_type_str = "限價"
        elif c_order_type_result == 'add_order':
            c_order_type_str = "加倉"
        elif c_order_type_result == 'SP':
            c_order_type_str = "止盈"
        elif c_order_type_result == 'SL':
            c_order_type_str = "止損"

        c_price_result = self.c_price_input(c_order_type_result)

        change_price_result = self.change_price_input()

        acc_name_result = self.Acc_name_input(test_real_result)

        confirmed = self.confirm_input("\n"
                                       f"這是一個{test_real_str}交易\n"
                                       f"{acc_name_result}\n"
                                       f"將要更改({coin_input_result})\n"
                                       f"把價格由({c_price_result}) \n"
                                       f"改成({change_price_result})\n"
                                       f"({c_order_type_str})的訂單\n"
                                       )

        if confirmed:
            print("输入确认成功，继续执行其他操作...")
            return test_real_result, coin_input_result, c_order_type_result, \
                   c_price_result,change_price_result ,acc_name_result

            # 在这里执行其他操作

        else:
            print("输入不正确，请重新输入。")

class Range_trade(active_orders):

    def __init__(self):
        super().__init__()
        self.TBP = "請輸入訂單 (觸發開倉價格)："
        self.CL = "請輸入訂單 (止損價格)："
        self.order_type = "Limit"
        self.flat_p = "請輸入訂單平倉價格：\n"

    def TBP_input_func(self):
        while True:
            user_input = input(self.TBP).replace(" ", "")  # 去除空格
            # 检查输入是否是有效的数字（包括整数和浮点数）
            if re.match(r'^-?\d+(\.\d+)?$', user_input):
                TBP_price = float(user_input)
                return TBP_price
            else:
                print("输入内容不符合要求，请重新输入。")

    def CL_input_func(self):
        while True:
            user_input = input(self.CL).replace(" ", "")  # 去除空格
            # 检查输入是否是有效的数字（包括整数和浮点数）
            if re.match(r'^-?\d+(\.\d+)?$', user_input):
                CL_price = float(user_input)
                return CL_price
            else:
                print("输入内容不符合要求，请重新输入。")

    def flat_p_input_func(self):
        while True:
            user_input = input(self.flat_p).replace(" ", "")  # 去除空格
            # 检查输入是否是有效的数字（包括整数和浮点数）
            if re.match(r'^-?\d+(\.\d+)?$', user_input):
                flat_p = float(user_input)
                return flat_p
            else:
                print("输入内容不符合要求，请重新输入。")

    def execute_all(self):
        # 按顺序执行所有方法

        test_real_result = self.test_real_acc_input()
        print(f"test_real_result:{test_real_result}")

        if test_real_result == "New_Testnet_Api_Acc_name.xlsx":
            test_real_str = "測試"
        else:
            test_real_str = "真實"

        coin_input_result = self.coin_input()

        flat_input_result = False
        side_result = ""
        side_input_result = self.side_input(side_result)

        if side_input_result == 'Buy':
            side_str = "買入"
        elif side_input_result == 'Sell':
            side_str = "沽出"

        elif side_input_result == "":
            side_str = "平倉"


        capital_ratio_result = self.capital_ratio_input()

        acc_name_result = self.Acc_name_input(test_real_result)

        TBP_result = self.TBP_input_func()

        price_result = TBP_result * 0.9995

        CL_result = self.CL_input_func()

        flat_p_result = self.flat_p_input_func()

        confirmed = self.confirm_input("\n"
                                        f"這是一個{test_real_str}《區間交易》\n"
                                       f"{acc_name_result}\n"
                                       f"觸發價{TBP_result}\n"
                                       f"開倉{side_str}價{price_result}\n"
                                       f"平倉價{flat_p_result}\n"
                                       f"止損價{CL_result}\n"
                                       f"以 ({capital_ratio_result})%的資產進行\n"
                                       f"({side_str}) ({coin_input_result}) \n"
                                       )

        if confirmed:
            print("输入确认成功，继续执行其他操作...")
            return test_real_result,coin_input_result,flat_input_result,\
                   side_input_result,self.order_type,price_result,\
                   capital_ratio_result,TBP_result,CL_result,\
                   flat_p_result,acc_name_result
            # 在这里执行其他操作
        else:
            print("输入不正确，请重新输入。")


if __name__ == "__main__":
    """active_order_inputs"""
    # active_orders_instance = active_orders()
    # test_real, coin_symbol, flat_order, \
    # side, order_type, p, \
    # capital_ratio, Accs = active_orders_instance.execute_all()
    # print(f"test_real: {test_real} (type: {type(test_real)})")
    # print(f"coin_symbol: {coin_symbol} (type: {type(coin_symbol)})")
    # print(f"flat_order: {flat_order} (type: {type(flat_order)})")
    # print(f"side: {side} (type: {type(side)})")
    # print(f"order_type: {order_type} (type: {type(order_type)})")
    # print(f"p: {p} (type: {type(p)})")
    # print(f"capital_ratio: {capital_ratio} (type: {type(capital_ratio)})")
    # print(f"Accs: {Accs} (type: {type(Accs)})")

    """random_split_inputs"""
    # random_split_orders_instance = random_split_orders()
    # test_real, coin_symbol, flat_order, \
    # side, order_type, p, \
    # capital_ratio, Accs, split_no, \
    # time_index, time_unit, price_range = random_split_orders_instance.execute_all()
    #
    # print(f"test_real:{test_real}, coin_symbol:{coin_symbol}, flat_order:{flat_order},\n"
    #       f"side:{side}, order_type:{order_type}, p:{p}, capital_ratio:{capital_ratio},\n"
    #       f"Accs:{Accs}, split_no:{split_no}, time_index:{time_index},\n"
    #       f"time_unit:{time_unit}, price_range:{price_range}")

    """cancel_orders_inputs"""
    # cancel_orders_instance = cancel_orders()
    # test_real, coin_symbol, order_type, \
    # p, Accs = cancel_orders_instance.execute_all()
    #
    # print(f"test_real:{test_real},coin_symbol:{coin_symbol}\n"
    #       f"order_type:{order_type},p:{p},acc_name:{Accs}\n")

    """change_orders_inputs"""
    # change_orders_instance = change_orders()
    # test_real, coin_symbol, order_type, \
    # p,change_p, Accs = change_orders_instance.execute_all()
    #
    # print(f"test_real:{test_real},coin_symbol:{coin_symbol}\n"
    #       f"order_type:{order_type},p:{p},\n"
    #       f"change_p:{change_p},acc_name:{Accs}\n")

    """change_orders_inputs"""
    range_trade_instance = Range_trade()
    test_real, coin_symbol, flat_order, \
    side, order_type, p, \
    capital_ratio, TBP, CL, \
    flat_p, Accs = range_trade_instance.execute_all()

    print(f"test_real:{test_real}, coin_symbol:{coin_symbol}, flat_order:{flat_order},\n"
          f"side:{side}, order_type:{order_type}, p:{p}, capital_ratio:{capital_ratio},\n"
          f"Accs:{Accs}, TBP:{TBP}, CL:{CL},\n"
          f"flat_p:{flat_p}")
