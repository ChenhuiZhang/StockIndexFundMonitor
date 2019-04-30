# coding=utf-8
import time
import requests
import pandas as pd
import io

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    req = requests.get(url, headers=headers)

    if req.status_code == 200:
        return req.text
    return None

if __name__ == '__main__':
    url = 'http://quotes.money.163.com/service/chddata.html?code=0000300&start=20190201&end=20190429&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'
    html = get_data(url)

    with io.open("my.csv", 'w', encoding="gb2312") as file:
        file.write(html)

    #print(html)
    #df = pd.read_csv(url, header=0, encoding='gb2312')
    df = pd.read_csv("my.csv", header=0, encoding='gb2312')
    print df.head(5)

    df.plot(x='日期', y=['收盘价'])
    
