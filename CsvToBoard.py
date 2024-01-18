import email.message
import smtplib #信箱憑證
import pandas as pd
import os
import dotenv

def contentPassengerCombiner(passenger_info):
    passenger_stationList = passenger_info['station'].split(',')
    if passenger_info['direction'] == '南下' :
        passenger_info['start'] = passenger_stationList[0].strip()
        passenger_info['End'] = passenger_stationList[-1].strip()
    else:
        passenger_info['start'] = passenger_stationList[-1].strip()
        passenger_info['End'] = passenger_stationList[0].strip()

with open('BoardContent.txt',"w", encoding="utf8") as file_out:
    file_out.write('')

# 【2.書寫信件內容】
# 讀取Rawdata
df_rawData = pd.read_csv('rawData.csv', dtype={'手機電話 (選填)': str}).fillna('')
df_rawData = df_rawData.rename(columns={'電子郵件地址':'Email', '你的稱呼':'name','你的身份':'identity','請問您預計的出發日期?':'date', '請問您的路線方向是?':'direction', '您的預計路線(起點和終點都需要勾選), 司機可追加願意停靠地點。':'station', '手機電話 (選填)':'phone','Line ID (選填)':'lineID','有沒有其他要跟 乘客、司機說的話? (選填)':'remark'})
df_driver = df_rawData[df_rawData['identity']=='我是自駕司機，協助乘客']
# print(df_rawData)

# 依序讀取資料
for row in range(0,df_driver.shape[0]):
    passenger_info = df_driver.iloc[row]
    contentPassengerCombiner(passenger_info)
    passenger_info['remark'] = passenger_info['remark'].replace("\n","")
    # print(passenger_info)
    # 撰寫信件內容
    content = f"""
徵乘客
日期：{passenger_info['date']}
起點：{passenger_info['start']}
終點：{passenger_info['End']}
特殊需求：{passenger_info['remark']}
-------
[聯絡方式]
司機姓名：{passenger_info['name']}
Email：{passenger_info['Email']}
"""

    with open('BoardContent.txt',"a", encoding="utf8") as file_out:
        file_out.write(content)
        print(content)