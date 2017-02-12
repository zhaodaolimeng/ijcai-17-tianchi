"""
数据检查：
1. 统计用户数目
select count(DISTINCT user_id) from user_pay; -- 19583949
2. 统计不同日期不同商店的消费数目
"""

import os
import pickle
import mysql.connector as c
import matplotlib.pyplot as plt
import collections


def fetch_pay_per_shop_and_day():

    max_fetch_item = 1000000
    cursor = con.cursor()
    cursor.execute("select shop_id,time_stamp from user_pay")
    result_set = cursor.fetchmany(max_fetch_item)
    shop_day_dict = dict()
    counter = 0

    while len(result_set) != 0:
        for shop_id, time_stamp in result_set:
            if shop_id not in shop_day_dict:
                shop_day_dict[shop_id] = dict()
            this_day = time_stamp.date()
            if this_day not in shop_day_dict[shop_id]:
                shop_day_dict[shop_id][this_day] = 0
            shop_day_dict[shop_id][this_day] += 1
        result_set = cursor.fetchmany(max_fetch_item)
        counter += 1
        print(counter)

    # 使用pickle保存结果
    pickle.dump(shop_day_dict, open('data/shop_day.pickle', 'bw'))


def fetch_shop_info():

    shop_dict = dict()
    cursor = con.cursor()
    cursor.execute("""
        select shop_id, location_id, per_pay, score, comment_cnt, shop_level,
        cate_1_name, cate_2_name, cate_3_name from shop_info
    """)
    for shop_id, location_id, per_pay, score, comment_cnt, shop_level, \
        cate_1_name, cate_2_name, cate_3_name \
            in cursor.fetchall():
        item_dict = {'shop_id': shop_id,
                     'location_id': location_id,
                     'per_pay': per_pay,
                     'score': score,
                     'comment_cnt': comment_cnt,
                     'shop_level': shop_level,
                     'cate_1_name': cate_1_name,
                     'cate_2_name': cate_2_name,
                     'cate_3_name': cate_3_name}
        shop_dict[shop_id] = item_dict

    pickle.dump(shop_dict, open('data/shop_info.pickle', 'bw'))


def draw_fig():
    cursor = con.cursor()
    cursor.execute("select shop_id, city_name from shop_info")

    shop_day_dict = pickle.load(open("data/shop_day.pickle", "rb"))
    shop_city_dict = {shop_id: city_name for shop_id, city_name in cursor.fetchall()}

    for shop_id, day_pay in shop_day_dict.items():
        day_pay_ordered = collections.OrderedDict(sorted(day_pay.items()))

        pay_time = []
        pay_cnt = []
        for t, cnt in day_pay_ordered.items():
            pay_time.append(t)
            pay_cnt.append(cnt)

        fig = plt.figure(figsize=(20, 5))
        plt.plot(pay_time, pay_cnt)

        directory = "visual/" + shop_city_dict[shop_id]
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(directory + "/" + shop_id + '.png')
        plt.close(fig)

if __name__ == "__main__":
    con = c.connect(user='root', password='ictwsn', host='127.0.0.1', database='ijcai17')
    # fetch_pay_per_shop_and_day()
    fetch_shop_info()

