create DATABASE if not EXISTS ijcai17;
use ijcai17;

-- 商户信息
create table shop_info(
shop_id varchar(255),
city_name varchar(255),
location_id varchar(255),
per_pay int,
score int,
comment_cnt int,
shop_level int,
cate_1_name varchar(255),
cate_2_name varchar(255),
cate_3_name varchar(255)
);
/*
mysqlimport --ignore-lines=0 \
            --fields-terminated-by=, \
            --local -u root \
            -p ijcai17 \
            shop_info.txt
*/

-- 用户支付信息
create table user_pay(
user_id varchar(255),
shop_id varchar(255),
time_stamp datetime
);
/*
mysqlimport --ignore-lines=0 \
            --fields-terminated-by=, \
            --local -u root \
            -p ijcai17 \
            user_pay.txt
*/

-- 用户浏览行为
create table user_view(
user_id varchar(255),
shop_id varchar(255),
time_stamp datetime
);
/*
mysqlimport --ignore-lines=0 \
            --fields-terminated-by=, \
            --local -u root \
            -p ijcai17 \
            user_view.txt
*/

-- 测试集
create table prediction(
shop_id varchar(255),
day_1 float,
day_2 float,
day_3 float,
day_4 float,
day_5 float,
day_6 float,
day_7 float,
day_8 float,
day_9 float,
day_10 float,
day_11 float,
day_12 float,
day_13 float,
day_14 float
);

