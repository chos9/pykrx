## KRX 전종목 시세 데이터 크롤링
import requests
import pandas as pd
from io import StringIO ## for Python 3
import io
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import exchange_calendars as ecals


XKRX = ecals.get_calendar("XKRX")
dates = []
for i in pd.date_range('1/1/2017', '12/1/2022', freq='MS'):
    temp = i
    while XKRX.is_session(temp.strftime('%Y-%m-%d')) == False:
        temp = temp + timedelta(days=1)
    dates.append(temp)


gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
referer = {'referer' : gen_otp_url}

df = pd.DataFrame(columns=['거래일자','종목코드','종목명','시장구분','소속부','종가','대비','등락률','시가','고가','저가','거래량','거래대금','시가총액','상장주식수'])

for i in dates:
    gen_otp_data = {
        'locale' : 'ko_KR',
        'mktId' : 'ALL',
        'trdDd' : i.strftime('%Y%m%d'),
        'share' : '1',
        'money' : '1',
        'csvxls_isNo' : 'false',
        'name' : 'fileDown',
        'url' : 'dbms/MDC/STAT/standard/MDCSTAT01501',
    }
    otp = requests.post(gen_otp_url, params = gen_otp_data)
    otp = BeautifulSoup(otp.content, "html.parser").text
    otp_key = {"code" : otp}
    down = requests.post(down_url, data= otp_key, headers = referer).content.decode('EUC-KR')
    down = StringIO(down)
    df_temp = pd.read_csv(down, sep = ',')

    df_temp['거래일자'] = i.strftime('%Y%m%d')
    df = pd.concat([df, df_temp])

file_dir = "./"
file_name = "data.csv"
df.to_csv(file_dir + file_name,index=False, index_label=None)
# print('Job Finished')
# print(file_dir + file_name + ' Saved')

