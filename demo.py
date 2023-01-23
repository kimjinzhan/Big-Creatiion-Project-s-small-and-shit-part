import json
import time
from pymysql import connect
import pymysql.cursors
import pynmea2
import requests
import serial
from sms_python.tencent_cloud_sample import sample

key = 'e2760a653e3dbcaebfc6f086f4faed31'
sms_time_limit = 300


def gps_get():
    # 创建gps串口的句柄
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
    count = 0
    while (True):
        try:
            try:
                if count == 100:
                    return -1
                # 将读取到的字节码转化成字符串（去掉前2位的无用字符）
                line = str(str(ser.readline())[2:])
                print("Loading GPS")
            except serial.SerialException:
                print("GPS初始化中")
                count += 1
                continue
            if line.startswith('$GPRMC'):
                line = line.replace('\\r\\n\'', '')  # 字符串结尾的无用换行符
                rmc = pynmea2.parse(line)
                if rmc.latitude and rmc.latitude:
                    location = str(rmc.longitude) + ',' + str(rmc.latitude)
                    return location
            continue
        except pynmea2.ParseError:
            print("GPS初始化中")
            count += 1
            continue


def get_location_x_y(place: str):
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    parameters = {
        'key': key,
        'address': place,
    }
    back = requests.get(url, params=parameters)
    text = back.text
    data = json.loads(text)
    location = data["geocodes"][0]["location"]
    return location


def from_gps_get_now_location():
    location = gps_get()
    if location == -1:
        print("请在室外使用")
    ampa_location = gps_to_ampa_gps(location)
    return ampa_location


def gps_to_ampa_gps(gps_location):
    parameters = {
        'key': key,
        'locations': gps_location,
        'coordsys': 'gps'
    }
    url = "https://restapi.amap.com/v3/assistant/coordinate/convert?parameters"
    back = requests.get(params=parameters, url=url)
    text = back.text
    data = json.loads(text)
    return data["locations"]


# 从数据库中获取dest字段

conn_obj = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='kimserver2002K',
    database='demo',
    charset='utf8',
    autocommit=True
)


def main():
    while 1:
        # 获取数据的循环
        cursor1 = conn_obj.cursor()
        time.sleep(5)
        sql1 = "select * from dest where status = 0"
        print("Waiting data from demo")
        conn_obj.ping(reconnect=True)
        data_exist_flag = cursor1.execute(sql1)
        now = cursor1.fetchone()
        if data_exist_flag == 1:
            id = now[0]
            dest = now[1]
            phone_num = str("+86" + str(now[3]))
        else:
            continue
        while True:
            # 获取到数据，进入GPS循环
            time.sleep(15)
            parameters = {
                'key': key,
                'origin': from_gps_get_now_location(),
                'destination': get_location_x_y(dest),
            }
            url = "https://restapi.amap.com/v4/direction/bicycling?parameters"
            back = requests.get(url, params=parameters)
            text = back.text
            data = json.loads(text)
            time_to_arrive = int(data["data"]["paths"][0]["duration"])
            if time_to_arrive < sms_time_limit:
                sms_ret = sample.sms(phone_num)
                status = sms_ret["SendStatusSet"][0]["Code"]
                if status == "Ok":
                    # 写回数据库
                    cursor2 = conn_obj.cursor()
                    sql2 = f"UPDATE `demo`.`dest` SET `status` = '1' WHERE (`id` = '{id}')"
                    connect.ping(reconnect=True)
                    res = cursor2.execute(sql2)
                    break
                else:
                    # 提示骑手
                    break


main()
