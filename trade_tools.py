import random
import datetime

class Trade_tool():

    def randomiz_num(self, num):
        print("randomiz_num_func\n")
        range_bit = 0.3
        max_num = (num * (1 + range_bit / 2))
        print(f"max_bit:{max_num}")
        min_num = (num * (1 - range_bit / 2))
        print(f"min_bit:{min_num}")
        ram_num = (random.uniform(min_num, max_num))

        return ram_num , max_num , min_num

    def randomiz_p(self, p , price_range):
        print("randomiz_p_func\n")

        range_p = price_range

        max_p = (p * (1 + (range_p / 2)))
        print(f"max_p:{max_p}")
        min_p = (p * (1 - (range_p / 2)))
        print(f"min_p:{min_p}")
        ram_p = round(random.uniform(min_p, max_p), 5)

        return ram_p

    def randomiz_time(self, no_time_idex, time, split_no):
        print("random_time_func\n")
        sec = 1
        one_min = 60 * sec
        one_hour = 60 * one_min
        one_day = 24 * one_hour

        if time == "sec":
            total_t = no_time_idex * sec
            print("sec")

        elif time == "min":
            total_t = no_time_idex * one_min
            print("min")
        elif time == "hour":
            total_t = no_time_idex * one_hour

        elif time == "day":
            total_t = no_time_idex * one_day
        else:
            print("輸入錯誤的單位")
        print(f"totol_t:{total_t}")
        range_t = 0.3
        print(total_t / split_no)
        aver_total_t = total_t / split_no
        max_aver_total_t = int(aver_total_t * (1 + range_t / 2))
        print(f"max_aver_total_t:{max_aver_total_t}")
        min_aver_total_t = int(aver_total_t * (1 - range_t / 2))
        print(f"min_aver_total_t:{min_aver_total_t}")

        ram_t = random.randint(min_aver_total_t, max_aver_total_t)
        print(f"ram_t:{ram_t}")


        return ram_t , total_t

    def is_within_time_range_func(self,start_time_str, end_time_str):
        print("is_within_time_range_func")
        # 定义时间格式
        time_format = "%d/%m/%Y, %H:%M"

        # 将字符串转换为 datetime 对象
        start_time = datetime.strptime(start_time_str, time_format)
        end_time = datetime.strptime(end_time_str, time_format)

        # 获取当前时间
        current_time = datetime.now()

        # 判断当前时间是否在开始时间和结束时间之间
        if start_time <= current_time <= end_time:
            within_time = True

        else:
            within_time = False

        return within_time

if __name__ == '__main__':
    p = 0.0011142442342
    p = Trade_tool().randomiz_p(p)
    print(p)