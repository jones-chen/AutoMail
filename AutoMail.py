import email.message
import smtplib #信箱憑證
import pandas as pd
import os
import dotenv

def contentPassengerCombiner(num, passenger_info):
    passenger_stationList = passenger_info['station'].split(',')
    if passenger_info['direction'] == '南下' :
        passenger_info['start'] = passenger_stationList[0].strip()
        passenger_info['End'] = passenger_stationList[-1].strip()
    else:
        passenger_info['start'] = passenger_stationList[-1].strip()
        passenger_info['End'] = passenger_stationList[0].strip()
    return f'''
<div>
    <h3>【乘客】</h3>
    <ul>
        <li>姓名：{passenger_info['name']}</li>
        <li>Email：{passenger_info['Email']}</li>
        <li>手機：{passenger_info['phone']}</li>
        <li>Line：{passenger_info['lineID']}</li>
        <li>起點：{passenger_info['start']}</li>
        <li>終點：{passenger_info['End']}</li>
        <li>特殊需求：{passenger_info['remark']}</li>
    </ul>
</div>
'''
def contentCombiner(driver_info, contentPassengers):
    driver_stationList = driver_info['station'].split(',')
    if driver_info['direction'] == '南下' :
        driver_info['start'] = driver_stationList[0].strip()
        driver_info['End'] = driver_stationList[-1].strip()
    else:
        driver_info['start'] = driver_stationList[-1].strip()
        driver_info['End'] = driver_stationList[0].strip()
    #         
    return f'''
    <div style="color: #000000;">
        <h1>[民眾順風車] "模糊匹配" 媒合成功通知</h1>
        <p style="color: red">此媒合為民眾順風車最後一次媒合，由於您的路線在路線剛好沒有媒合成功。</p>
        <p style="color: red">在此提供您<strong>類似相關路線</strong>的司機，若您還尚未取得返鄉投票的車位，可以試著與該司機聯繫，希望能提供您最後一線希望。</p>
        
        <p>以下幾件事情告知，並希望您協助：</p>
        <ol>
            <li>本平台系統統一以寄送 Email 的方式通知 駕駛與乘客雙方</li>
            <li>請乘客與司機互相聯繫，確認彼此的上車時間與地點</li>
            <li>媒合的結果僅供雙方參考，實際狀況請雙方進行溝通與協調。</li>
            <li>由於考量到事後溝通有未媒合成功的可能性，系統會給予每名駕駛多於座位的乘客數量。所以可能會有乘客已滿的問題。</li>
            <li>另歡迎多利用本平台另外架設的<a href="https://padlet.com/teamkpgo/padlet-s86sodpizxo8p7jt">佈告欄</a>，提供駕駛與乘客進行自行媒合。</li>
        </ol>

        <p>出發日期：{driver_info['date']}</p>
        <p>路線方向：{driver_info['direction']}</p>

        <h1>與您媒合到的共乘名單：</h1>
        <h3>【司機】</h3>
        <ul>
            <li>姓名：{driver_info['name']}</li>
            <li>Email：{driver_info['Email']}</li>
            <li>手機：{driver_info['phone']}</li>
            <li>Line：{driver_info['lineID']}</li>
            <li>起點：{driver_info['start']}</li>
            <li>終點：{driver_info['End']}</li>
            <li>特殊需求：{driver_info['remark']}</li>
        </ul>
        <div>{contentPassengers}</div>
        
        <strong>【最後聲明】本平台只提供媒合服務，不抽取任何費用與任何擔保安全，請將此旅程告知親友，並保護自身安全！</strong>
        
        <p>若兩方乘客與司機談妥成功，為了協助後台完善，麻煩填寫 <a href="https://forms.gle/GKkwyPJKcvzZoTG17">意見回饋表單<a> 讓我們知道，謝謝！！</p>
        <p>再次感謝您的配合與支持！感謝你！</p>
        <p>By 民眾順風車 小草志工團</p>
        ---------------------------
        <h4>【補充：歡迎加入監票部隊】</h4>
        <p>大家加油，最後一哩路了！我們努力了這麼久，不要被有心人士做弊做掉了！</p>
        <p>裡面也有監票的QR code和外監注意事項。外監不會太困難，加入後都會有教學！</p>
        <li><a href="https://www.youtube.com/live/n-Agvwt7V1Q?si=p8f2IDQSUXFA6QYC">1、比特王-做票的影片</a></li>
        <li><a href="https://kpvote.tpp.org.tw/#/login">2、加入監票部隊-眾所矚目監票計畫</a></li>
        <li><a href="https://drive.google.com/drive/folders/172QmHfh6-j4dtaGPItrg2YWFXYUfRlvG">3、過往做票全紀錄</a></li>
    </div>
'''

# 載入 .env 文件中的環境變數
dotenv.load_dotenv()
EmailPassword = os.getenv("EMAILPASSWORD")


# 【2.書寫信件內容】
# 讀取Rawdata
df_rawData = pd.read_csv('rawData.csv', dtype={'手機電話 (選填)': str}).fillna('')
df_rawData = df_rawData.rename(columns={'電子郵件地址':'Email', '你的稱呼':'name', '請問您預計的出發日期?':'date', '請問您的路線方向是?':'direction', '您的預計路線(起點和終點都需要勾選), 司機可追加願意停靠地點。':'station', '手機電話 (選填)':'phone','Line ID (選填)':'lineID','有沒有其他要跟 乘客、司機說的話? (選填)':'remark'})
# print(df_rawData)

# 讀取媒合結果
df_matched = pd.read_csv('matched.csv').fillna('')
df_matched.columns = ['駕駛ID','乘客ID']
# print(df_matched)

# 依序讀取資料
for row in range(0,df_matched.shape[0]):
    driver = df_matched.iloc[row]['駕駛ID']
    passengerList = [df_matched.iloc[row]['乘客ID']]

    # 取得司機資訊
    driver_info = df_rawData.iloc[driver]
    # print(f"司機：{driver_info['Email']}")
    
    if driver_info['Email'] in ['td14010@gmail.com','uranus.lin@gmail.com','quickitpn@gmail.com','b10103210@gmail.com','sytan0422@gmail.com']:
        continue
    
    # 取得乘客資訊
    num = 0
    contentPassenger = ''
    for perPassenger in passengerList:
        num += 1
        passenger_info = df_rawData.iloc[int(perPassenger)]
        # print(f"乘客{num}：{passenger_info['Email']}")
        contentPassenger = contentPassenger + contentPassengerCombiner(num, passenger_info)
        # print(contentPassenger)
    
    # 撰寫信件內容
    content = contentCombiner(driver_info, contentPassenger)
    # print(content)

    # 【1.設定信件封包】
    msg=email.message.EmailMessage()
    msg["to"] = [passenger_info['Email']] #收件人地址   driver_info['Email']
    msg["Bcc"] = ["tonnyqoo@gmail.com", "misppool@gmail.com"]
    msg["from"]="teamkp.go@gmail.com"   #寄件人地址  
    msg["subject"]="[民眾順風車] ‘模糊匹配’ 媒合成功通知"                 #郵件主旨
    msg.add_alternative(content, subtype="html")  #將整個字串做製換
    
    # 【2.登入信箱憑證】驗證寄件人身分
    server=smtplib.SMTP_SSL("smtp.gmail.com",465) #465不用管他，固定的
    server.login("teamkp.go@gmail.com",EmailPassword)
    server.send_message(msg) 
    print(f'{driver}、{passengerList}，{msg["to"]}，寄件成功')
                         
server.quit()
server.close  #關閉連線
