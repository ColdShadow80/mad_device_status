import json
import requests
import time
import locale
import configparser
import mysql.connector as mariadb
import datetime

config = configparser.ConfigParser()
config.read('config.ini')

statusURL = config.get('CONFIG', 'statusURL')

dbhost = config.get('DATABASE', 'MAD_db_host')
MADdb = config.get('DATABASE', 'db_name')
dbuser = config.get('DATABASE', 'db_user')
dbpass = config.get('DATABASE', 'db_pass')


dateStr=datetime.datetime.now()
dateStr=f'{dateStr:%Y-%m-%d-%h-%m}'


query="select DEVICE.name as origin,if(STATUS.lastProtoDateTime='','Unknown',time_format(STATUS.lastProtoDateTime,'%H:%i')) as lastProtoDateTime , if(STATUS.lastProtoDateTime='','Unknown',time_format(STATUS.lastProtoDateTime,'%H:%i')) - time_format(now(),'%H:%i') as "lastProtomin"  from trs_status STATUS left join settings_device DEVICE on STATUS.device_id=DEVICE.device_id where (STATUS.lastProtoDateTime < now() - interval 10 minute or STATUS.lastProtoDateTime = '') order by STATUS.device_id;"
mariadb_connection = mariadb.connect(host=dbhost, user=dbuser, database=MADdb, password=dbpass)
cursor = mariadb_connection.cursor()
cursor.execute(query)

for origin,lastProtoDateTime in cursor:

    originStr="{}".format(origin)
    protoStr="{}".format(lastProtoDateTime)
    protoStrTimeNotSeen="{}".format(lastProtomin)

    data = {
                "username": "Alert >10min no data!!",
                "avatar_url": "https://www.iconsdb.com/icons/preview/red/exclamation-xxl.png",
                "embeds": [
                {
                "title": "",
                "url": "",
                "color": 16711680,
                "description": "__**"+originStr+"**__ last data at "+protoStr+" - Not sending data for: "+protoStrTimeNotSeen+"  ",
                "image": 
                {
        "url": ""
                }
        }]
                }

    result = requests.post(statusURL, json=data)
    print(result)
    time.sleep(1)


mariadb_connection.close()
