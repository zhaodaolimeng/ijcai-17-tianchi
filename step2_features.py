"""
目标：针对每个shop预测未来两周的数据

X_train：
shop_info.location_id
shop_info.per_pay
shop_info.score
shop_info.shop_level
shop_day.datetime.year
shop_day.datetime.month
shop_day.datetime.day
shop_day.datetime.day_of_week

y_train:
cnt
"""

import codecs
import pickle
import pandas as pd
import numpy as np
import xgboost
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


def save_cnt_to_file():
    shop_day_dict = pickle.load(open("data/shop_day.pickle", "rb"))
    shop_dict = pickle.load(open("data/shop_info.pickle", "rb"))

    result_list = []
    cate_dict_list = [{}, {}, {}]
    cate_cnt_list = [0, 0, 0]
    numeric_feature_name = ['shop_id','location_id','per_pay', 'score','comment_cnt', 'shop_level']

    for shop_id, day_pay in shop_day_dict.items():
        for time_stamp, pay_cnt in day_pay.items():
            item_list = []
            item_name = []
            # 数值类型
            for f_name in numeric_feature_name:
                item_list.append(int(shop_dict[shop_id][f_name]))
                item_name.append(f_name)

            # 转换非数值类型
            for dummy_i in range(3):
                key = 'cate_' + str(dummy_i + 1) + '_name'
                val = shop_dict[shop_id][key]
                if val not in cate_dict_list[dummy_i]:
                    cate_dict_list[dummy_i][val] = cate_cnt_list[dummy_i]
                    cate_cnt_list[dummy_i] += 1
                item_list.append(cate_dict_list[dummy_i][val])
                item_name.append(key)

            item_list.append(time_stamp.year)
            item_list.append(time_stamp.month)
            item_list.append(time_stamp.day)
            item_list.append(pay_cnt)

            item_name.append('year')
            item_name.append('month')
            item_name.append('day')
            item_name.append('cnt')

            result_list.append(item_list)

    with codecs.open('data/features.csv', 'w') as f:
        f.write(','.join(item_name) + '\n')
        for item_list in result_list:
            f.write(','.join([str(it) for it in item_list]) + '\n')

    return result_list


if __name__ == "__main__":

    # 将每个shop的统计信息写入到文本文件中
    # result = save_cnt_to_file()

    # 将文件加载成dataframe的形式
    train_df = pd.read_csv('data/features.csv', header=0)

    # 生成训练集和测试集
    train_selected = train_df.query("~(year == 2016 & month == 10 & day >= 18)")
    train_X = train_selected.ix[:, train_selected.columns != 'cnt'].as_matrix()
    train_y = train_selected['cnt']

    test_selected = train_df.query("year==2016 & month==10 & day>=18")  # 2016.10.18 - 2016.10.31
    test_X = train_selected.ix[:, train_selected.columns != 'cnt'].as_matrix()

    # 调用xgboost
    gbm = xgboost.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05).fit(train_X, train_y)
    test_y = gbm.predict(test_X)

    # 生成结果
    submission = pd.DataFrame({'shop_id': test_X['shop_id'],
                               'year': test_X['year'],
                               'month': test_X['month'],
                               'day': test_X['day'],
                               'cnt': test_y['cnt']})
    submission.to_csv("data/submission.csv", index=False)
