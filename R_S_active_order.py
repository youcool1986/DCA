import trade_tools as t_tool
import trade_api as t_api
import non_trade_api as n_t_api
import pandas as pd
import time
import math
from input import random_split_orders
from retrying import retry

trade_api = t_api.Trade
trade_adjust = n_t_api.Trade_adjustments
trade_tools = t_tool.Trade_tool

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def read_data(test_real,Accs):
    # 读取 Excel 文件
    file_path = test_real
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"读取 Excel 文件时出错：{e}")
        exit()

    # 将 Acc_Name 列设为索引，以便将其用作字典键
    df.set_index("Acc_Name", inplace=True)

    # 准备一个字典来存储匹配结果
    accs_info = {}

    # 匹配 Accs 列表中的每个 Acc_Name，并获取其对应的 Api_key 和 Api_secret
    for acc_name in Accs:
        try:
            api_key = df.loc[acc_name, "Api_key"]
            api_secret = df.loc[acc_name, "Api_secret"]
            accs_info[acc_name] = {"Api_key": api_key, "Api_secret": api_secret}
        except KeyError:
            print(f"无法找到 Acc_Name 为 {acc_name} 的信息。")

    return accs_info

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def trading_session(acc_name , accs_info):
    print("trading_session_fuc\n")
    trade_session = trade_api(acc_name, accs_info['Api_key'], accs_info['Api_secret'])
    print(acc_name, accs_info['Api_key'], accs_info['Api_secret'])
    return trade_session

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def checking_in_out_data(trade_session, coin_symbol, capital_ratio, side):
    print("checking_in_out_data_func\n")
    non_trade_api = n_t_api.Non_trade
    cur_price = non_trade_api().get_current_coin_price(coin_symbol)
    df_position_val = trade_session.get_position_value(coin_symbol)
    print(f"df_position_val:{df_position_val}")
    total_position_val, total_equity = trade_session.wallet_balance()
    position_val = float(df_position_val.loc[0, 'total_val'])
    position_size = float(df_position_val.loc[0, 'qty'])
    position_side = df_position_val.loc[0, 'side']

    trade_size = position_size * (capital_ratio / 100)
    trade_equity = total_equity * (capital_ratio / 100)

    print("position_size:", position_size, "position_val:", position_val)

    pd_data = non_trade_api().get_instruments_info(coin_symbol)
    print(f"pd_data:{pd_data}")
    trade_adjustment = trade_adjust(pd_data)
    print(f"trade_adjustment:{trade_adjustment}")
    minOrderQty = float(pd_data.loc[0, 'minOrderQty'])
    maxMktOrderQty = float(pd_data.loc[0, 'maxMktOrderQty'])
    min_pos_val = 6  # 5usdt 平台限制

    return cur_price, trade_equity, position_side, trade_size, side, trade_adjustment, minOrderQty, maxMktOrderQty, min_pos_val

def re_define_p(p,cur_price):
    print("re_define_p\n")
    if order_type == "Market":
        print(f"p:{p}")
        p = cur_price

    return p

def re_define_trade_capital(flat_order,p,trade_equity,trade_size,min_amount):
    print("re_define_trade_capital\n")

    if flat_order == True:
        print("flat_order== True")
        print(f"trade_size:{trade_size}")
        trade_capital = trade_size
        trade_equity = trade_size * p

    else:
        print("active_order == True")
        trade_capital = trade_equity

        if trade_capital < min_amount and trade_capital > 0:
            trade_capital = min_amount

    return trade_capital,trade_equity  # 确保返回值在函数的最外层

def particule_define(p,min_pos_val,minOrderQty,maxMktOrderQty):

    print("particule_define_func\n")
    print(f"{type(min_pos_val)}{type(minOrderQty)}p:{p}{type(p)}")
    if min_pos_val < (minOrderQty * p):
        # print(f"(minOrderQty * p):{(minOrderQty * p)}, "
        # f"min_amount is minOrderQty {minOrderQty* p}")
        min_amount = (minOrderQty * p)

    else:
        # print("min_amount is min_pos_val*p")
        min_amount = min_pos_val

    max_amount = math.floor((maxMktOrderQty * p) / min_amount)
    # print(f"max_amount is {max_amount} of min_amount")

    particule_val = min_amount
    # print(f"particule_val is {particule_val}")

    min_amount = 1
    # print(f"min_amount is {min_amount} unit\n")

    return  max_amount , min_amount ,particule_val

def re_split_no(p,particule_val,split_no,trade_equity,maxMktOrderQty,trade_capital):

    print("re_split_no func")
    min_bit = (trade_equity/split_no) * 0.7
    print(f"min_bit:{min_bit}")
    max_bit_posit = (maxMktOrderQty * p)
    print(f"max_bit_posit:{max_bit_posit}")
    max_split_no = math.floor(trade_equity / particule_val)
    print(f"trade_capital:{trade_equity},max_split_no:{max_split_no}")
    if max_split_no == 0:
        max_split_no = 1

    if split_no > max_split_no:

        split_no = max_split_no

    elif min_bit > max_bit_posit:
        split_no = (trade_capital / max_bit_posit)*1.3

    return split_no

def re_define_bit(split_no,flat_order,trade_capital,trade_size):

    bit = trade_capital / split_no
    if flat_order == True:
        bit = trade_size / split_no
    print(f"bit:{bit}")

    return bit

def randomized_max_min_bit(flat_order,bit,min_amount,max_amount,minOrderQty,maxMktOrderQty):

    print("randomized_max_min_bit func\n")
    ram_bit , max_bit , min_bit = trade_tools().randomiz_num(bit)
    print(f"ram_bit:{ram_bit}.max_bit:{max_bit}.min_bit:{min_bit}")
    if flat_order == False:
        if min_amount > max_bit: min_bit = min_amount
        if max_amount < max_bit: max_bit = max_amount
        print(f"re:min_bit:{min_bit},max_bit:{max_bit}")
    else:
        if minOrderQty > max_bit: min_bit = min_amount
        if maxMktOrderQty < max_bit: max_bit = max_amount
        print(f"re:min_bit:{min_bit},max_bit:{max_bit}")

    return max_bit , min_bit

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def active_trade(ram_bit,qty,ram_p,trade_capital,side,trade_adjustment,trade_session,particule_val,t):

    print("active_trade_func\n")

    trade_dic_2 = {}
    print(f"qty:{qty}")
    qty = trade_adjustment.qty_decimel_adjust(qty)
    print(f"trade_qty:{qty}")

    trade_session.active_order(coin_symbol, side, qty, ram_p, order_type)
    trade_dic = {
        "coin_symbol": coin_symbol,
        "side": side,
        "qty": qty,
        "ram_p": ram_p,
        "order_type_input": order_type
    }
    trade_capital = trade_capital - ram_bit
    time.sleep(t)
    print(f"t:{t}\n")

    if ram_bit > trade_capital and trade_capital > particule_val:
        print("Limit_remain_order\n")
        qty = trade_adjustment.qty_decimel_adjust(qty)
        print(f"re_qty:{qty}")
        p = trade_adjustment.prices_adjust_range(ram_p)
        print(f"re_p:{ram_p}")
        trade_session.active_order(coin_symbol, side, qty, ram_p, order_type)

        trade_dic_2 = {
            "coin_symbol": coin_symbol,
            "side": side,
            "qty": qty,
            "ram_p": ram_p,
            "order_type_input": order_type
        }
        time.sleep(t)
        print(f"t:{t}\n")
        break_pt = True
        print("break")

    elif ram_bit > trade_capital and trade_capital < particule_val:

        print("no need to trade for remain\n")
        break_pt = True

    else:
        break_pt = False

    return break_pt, trade_dic ,trade_capital , trade_dic_2

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def flat_order_side(position_side,side):
    print("flat_order_side_func\n")

    if position_side == "Buy":
        side = "Sell"
    elif position_side == "Sell":
        side = "Buy"
    else:
        side = side

    return side

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def flat_trade(ram_bit,qty,ram_p,trade_capital,side,trade_adjustment,minOrderQty,t):
    print("flat_trade\n")

    trade_dic_2 = {}

    print(f"qty:{qty}")
    qty = trade_adjustment.qty_decimel_adjust(qty)
    print(f"trade_qty:{qty}")
    print("trade")
    # trade_session.active_order(coin_symbol, side, qty, ram_p, order_type)
    trade_dic = {
        "coin_symbol": coin_symbol,
        "side": side,
        "qty": qty,
        "ram_p": ram_p,
        "order_type_input": order_type
    }
    trade_capital = trade_capital - qty
    time.sleep(t)
    print(f"t:{t}\n")

    if ram_bit > trade_capital and trade_capital > minOrderQty:
        print("remain_order\n")
        qty = trade_capital
        qty = trade_adjustment.qty_decimel_adjust(qty)
        print(f"remain_qty:{qty}")
        # trade_session.active_order(coin_symbol, side, qty, ram_p, order_type)
        print("trade")

        trade_dic_2 = {
            "coin_symbol": coin_symbol,
            "side": side,
            "qty": qty,
            "ram_p": ram_p,
            "order_type_input": order_type
        }
        time.sleep(t)
        print(f"t:{t}\n")
        break_pt = True
        print("break")

    else:
        break_pt = False

    return break_pt , trade_dic , trade_capital ,trade_dic_2


def trade_list_func(trade_list,trade_dic,trade_dic_2):

    print(f"trade_list_func\n")
    trade_list.append(trade_dic)
    if trade_dic_2 != {}:
        trade_list.append(trade_dic_2)
    return trade_list

@retry(stop_max_attempt_number=100, wait_fixed=2000)
def detect_tigger_p_func(tp):
    print("detect_tigger_p_func\n")
    non_trade_api = n_t_api.Non_trade
    cur_p = non_trade_api().get_current_coin_price(coin_symbol)
    print(f"tp:{tp},cur_p:{cur_p}")
    while True:
        non_trade_api = n_t_api.Non_trade
        cur_p = non_trade_api().get_current_coin_price(coin_symbol)
        if tp < cur_p:
            print("waiting for tigger_p")
            time.sleep(2)
        else:
            print("tigger_P > cur_p , start_trade")
            break

@retry(stop_max_attempt_number=5, wait_fixed=2000)
def trade_start_func(trade_capital,max_bit,min_bit,p, side,trade_adjustment,tp,position_side,cur_price,trade_session,particule_val,t,minOrderQty,flat_order,price_range):

    print("trade_start func")
    break_pt = False
    trade_list = []

    while trade_capital > 0 and break_pt == False :

        detect_tigger_p_func(tp)
        print(f"trade_capital:{trade_capital}")
        ram_bit, t_max_bit, t_min_bit = trade_tools.randomiz_num(max_bit ,min_bit)
        ram_p  = trade_tools().randomiz_p(p,price_range)
        print(f"ram_bit:{ram_bit},t_max_bit:{t_max_bit},t_min_bit:{t_min_bit}")
        print(f"remain_capital:{trade_capital}")
        ram_p = trade_adjustment.prices_adjust_range(ram_p)
        print(f"trade_ram_p:{ram_p}")

        if order_type == "Limit":

            if flat_order == False:
                print("Limit_active_order\n")
                print(f"p:{ram_p}")
                qty = ram_bit / ram_p
                print(f"qty:{qty},ram_bit:{ram_bit},ram_p:{ram_p},trade_capital:{trade_capital},side:{side}")
                break_pt, trade_dic ,trade_capital , trade_dic_2 = active_trade(ram_bit,qty,ram_p,trade_capital,side,trade_adjustment,trade_session,particule_val,t)


            else:
                print("Limit_flat_order\n")
                side = flat_order_side(position_side,side)
                qty = ram_bit
                break_pt , trade_dic , trade_capital ,trade_dic_2 = flat_trade(ram_bit,qty,ram_p,trade_capital,side,trade_adjustment,minOrderQty,t)

        else:

            if flat_order == False:
                print("Market_active_order\n")
                qty = ram_bit / cur_price
                print(f"qty:{qty}")
                break_pt, trade_dic ,trade_capital , trade_dic_2  = active_trade(ram_bit,qty,ram_p,trade_capital,side,trade_adjustment,trade_session,particule_val,t)

            else:
                print("Market_flat_order\n")
                side = flat_order_side(position_side,side)
                qty = ram_bit
                break_pt, trade_dic , trade_capital,trade_dic_2 = flat_trade(ram_bit,qty,ram_p,trade_capital,side,trade_adjustment,minOrderQty,t)

        trade_list = trade_list_func(trade_list,trade_dic,trade_dic_2)
        if break_pt == True: break

    return trade_list

def run_func(test_real, coin_symbol, flat_order, side, order_type, p, capital_ratio, Accs, split_no,time_index, time_unit, price_range,tp):

    accs_info = read_data(test_real,Accs)
    print(f"accs_info:{accs_info}")
    for acc_name, info in accs_info.items():
        print(f"acc_name:{acc_name},info:{info}")
        trade_session = trading_session(acc_name, info)

        cur_price , trade_equity, position_side, trade_size, side, trade_adjustment, minOrderQty, maxMktOrderQty, min_pos_val = checking_in_out_data(trade_session, coin_symbol, capital_ratio, side)
        print(f"cur_price:{cur_price},trade_equity:{trade_equity},position_side:{position_side},"
              f"trade_size:{trade_size}"
              f",trade_adjustment:{trade_adjustment},minOrderQty:{minOrderQty}"
              f",maxMktOrderQty:{maxMktOrderQty},min_pos_val:{min_pos_val}\n")

        p = re_define_p(p,cur_price)
        print(f"p:{p},type_p:{type(p)}")
        max_amount, min_amount, particule_val = particule_define(p,min_pos_val,minOrderQty,maxMktOrderQty,)
        print(f"max_amount:{max_amount},min_amount:{min_amount},particule_val:{particule_val}\n")
        trade_capital,trade_equity = re_define_trade_capital(flat_order,p,trade_equity,trade_size,min_amount)
        print(f"p:{p},trade_capital:{trade_capital}\n")
        test_capital = trade_capital

        if trade_capital > 0:

            split_no = re_split_no(p,particule_val , split_no,trade_equity,maxMktOrderQty,trade_capital)
            print(f"re_define split_no:{split_no}\n")
            bit = re_define_bit(split_no,flat_order,trade_capital,trade_size)
            print(f"bit:{bit}")
            max_bit , min_bit = randomized_max_min_bit(flat_order,bit,min_amount,max_amount,minOrderQty,maxMktOrderQty)
            print(f"max_bit:{max_bit},max_bit:{min_bit}\n")
            t, total_t = trade_tools().randomiz_time(time_index, time_unit, split_no)
            print(f"t:{t}\n")


            trade_list = trade_start_func(trade_capital,max_bit,min_bit,p, side,trade_adjustment,tp,position_side,cur_price,trade_session,particule_val,t,minOrderQty,flat_order,price_range)

            print(f"trade_list:{trade_list}\n")
            total_qty = sum(trade_dic['qty'] for trade_dic in trade_list)
            print(f"total_qty:{total_qty}\n")

            # test assume check
            # position_val = 100
            if order_type == "Limit":
                qty = test_capital / p
            else:
                p = cur_price
                qty = test_capital / p

            trade_input_result = {
                "coin_symbol": coin_symbol,
                "side_input": side,
                "qty": qty,
                "price": p,
                "order_type_input": order_type
            }
            print(f"trade_input_result:{trade_input_result}")

if __name__ == "__main__":



    test_real, coin_symbol, flat_order, \
    side, order_type, p, \
    capital_ratio, Accs, split_no, \
    time_index, time_unit, price_range = random_split_orders().execute_all()
    print(f"test_real:{test_real},coin_symbol:{coin_symbol},flat_order:\n"
          f"flat_order:{flat_order},side:{side}\n"
          f"order_type:{order_type},p:{p},capital_ratio:{capital_ratio}\n"
          f"Accs:{Accs}\n")

    tp = 0.012
    # import test_trade
    # flat_order , randomize, split_no, no_time_idex, time_str, coin_symbol, \
    # order_type, p, reduce_ratio, side, Accs, test_real, accs_info = test_trade.test_r_l_small()
    # print(randomize, split_no, no_time_idex, time_str, coin_symbol, \
    # order_type, p, reduce_ratio, side, Accs, test_real, accs_info)

    run_func(test_real, coin_symbol, flat_order, side, order_type, p, capital_ratio, Accs, split_no,time_index, time_unit, price_range,tp)