# coding=utf-8
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
import io
import matplotlib
import datetime
import sys

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Yahei Mono']

from matplotlib.font_manager import FontProperties
chinese_font = FontProperties(fname='/usr/share/fonts/program/yahei_mono.ttf')

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    req = requests.get(url, headers=headers)

    if req.status_code == 200:
        return req.text
    return None

def save_csv(code, duration):
    now = datetime.date.today()
    begin = now - datetime.timedelta(days=duration)

    csv = "%s_%s.csv" % (code, begin.strftime("%Y%m%d"))
    url = 'http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&fields=TCLOSE;TOPEN;LCLOSE;CHG;PCHG' % (code, begin.strftime("%Y%m%d"), now.strftime("%Y%m%d"))
    print url

    html = get_data(url)

    with io.open(csv, 'w', encoding="gb2312") as file:
        file.write(html)

    return csv

def plot_csv(csv):
    df = pd.read_csv(csv, header=0, encoding='gb2312')

    df = df[::-1]
    df = df.reset_index(drop=True)
    print df.head(5)

    ax = df.plot(x=u'日期', y=[u'收盘价'])
    ax.set_xticks(df.index)
    ax.set_xticklabels(df[u'日期'], rotation=60)
    plt.show()

if __name__ == '__main__':
    csv_file = save_csv("0000300", 180)

    plot_csv(csv_file)
    
