import mysql.connector
from mysql.connector import Error

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

import time

# 데이터베이스 연결 설정
try :
    connection = mysql.connector.connect(
        host='localhost',          # 데이터베이스 서버 주소
        user='root',      # 데이터베이스 사용자 이름
        password='password',  # 사용자 비밀번호
        database='Hydro_project'   # 접근할 데이터베이스 이름
    )

    if connection.is_connected():
        print('MySQL 데이터베이스에 성공적으로 연결되었습니다.')
        cursor = connection.cursor()

except Error as e:
    print(f"MySQL 데이터베이스 에러: {e}")

print("Start!")

while True :
    try :
        # 웹 페이지 URL
        current_time = datetime.now()
        current_minute = current_time.minute
        current_sec = current_time.second

        if current_minute % 5 == 0 and current_sec <= 1 :
            nd = int(time.time()) * 1000
            
            date = datetime.today().strftime("%Y-%m-%d")
            
            url = f"http://10.21.10.97/_inc/report_list.asp?sdate={date}&edate={date}&sl_id=1&equip=IV&report_type=d&type_sd=d&inv_sel=21&data_form=5&inv_name=그린에너지연구관&wt_channel=4&cb_channel=0&equip_name=인버터&_search=false&nd={nd}&rows=10&page=1&sidx=dt&sord=desc"


            # 페이지로부터 HTML 가져오기
            response = requests.get(url)
            response.raise_for_status()  # 요청이 실패하면 예외를 발생시킵니다.

            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            json_str = str(soup)
            data = json.loads(json_str)

       
            a = dict(data['rows'][0])["cell"]
        
       
            query = "INSERT INTO E_GR (일시, 전압, 전류, 출력_DC, 전압_RS, 전압_ST, 전압_TR, 전류_R, 전류_S, 전류_T, 출력_AC, 누적발전량, 주파수, 역률, 경사, 수평, 모듈, 외기) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            values = (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14], a[15], a[16], a[17])

            cursor.execute(query, values)
            connection.commit()
            print(date, current_time, "sucsess!")

    except :
        pass
