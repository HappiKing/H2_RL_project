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
        host='112.167.124.86',          # 데이터베이스 서버 주소
        user='root',      # 데이터베이스 사용자 이름
        password='password',  # 사용자 비밀번호
        database='Hydro_project'   # 접근할 데이터베이스 이름
    )

    if connection.is_connected():
                print('MySQL 데이터베이스에 성공적으로 연결되었습니다.')
                cursor = connection.cursor()

except Error as e:
        print(f"MySQL 데이터베이스 에러: {e}")

# 테이블 생성
cursor.execute(f"CREATE TABLE IF NOT EXISTS E_5 (일시 TIMESTAMP PRIMARY KEY, 전압 VARCHAR(255), 전류 VARCHAR(255), 출력_DC VARCHAR(255), 전압_RS VARCHAR(255),\
                                               전압_ST VARCHAR(255), 전압_TR VARCHAR(255), 전류_R VARCHAR(255), 전류_S VARCHAR(255), \
                                               전류_T VARCHAR(255), 출력_AC VARCHAR(255), 누적발전량 VARCHAR(255), 주파수 VARCHAR(255),\
                                               역률 VARCHAR(255), 경사 VARCHAR(255), 수평 VARCHAR(255), 모듈 VARCHAR(255), 외기 VARCHAR(255))")

print("데이터 수집 시작")

while True : 
    try :
        # 현재 시간 가져오기
        current_time = datetime.now()
        current_minute = current_time.minute
        current_sec = current_time.second
        
        nd = int(time.time()) * 1000

        # 5분 단위로 떨어지는지 확인
        if current_minute % 5 == 0 and current_sec <= 1:
            # 웹 페이지 URL
            date = datetime.today().strftime("%Y-%m-%d")
            url = f"http://10.21.91.183/_inc/report_list.asp?sdate={date}&edate={date}&sl_id=1&equip=IV&report_type=d&type_sd=d&inv_sel=1&data_form=5&inv_name=INV-1&wt_channel=4&cb_channel=0&equip_name=%EC%9D%B8%EB%B2%84%ED%84%B0&_search=false&nd=1716532572878&rows=10&page=1&sidx=dt&sord=desc"  # 실제 웹 페이지 URL로 교체해야 합니다.

            # 페이지로부터 HTML 가져오기
            response = requests.get(url)
            response.raise_for_status()  # 요청이 실패하면 예외를 발생시킵니다.

            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            json_str = str(soup)
            data = json.loads(json_str)

            a = dict(data['rows'][0])["cell"]

            try :
                query = "INSERT INTO E_5 (일시, 전압, 전류, 출력_DC, 전압_RS, 전압_ST, 전압_TR, 전류_R, 전류_S, 전류_T, 출력_AC, 누적발전량, 주파수, 역률, 경사, 수평, 모듈, 외기) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8],a[9], a[10], a[11], a[12], a[13], a[14], a[15], a[16], a[17])
                cursor.execute(query, values)
                print(current_time, "sucsess!!")
                connection.commit()
            except :
                print("이미 존재하는 데이터입니다.")

    except :
        print("Error 발생")