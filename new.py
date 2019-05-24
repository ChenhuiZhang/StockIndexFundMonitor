# coding=utf-8
import io
import datetime
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties
chinese_font = FontProperties(fname='/usr/share/fonts/program/yahei_mono.ttf')

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    req = requests.get(url, headers=headers)

    if req.status_code == 200:
        return req.text
    return None

def save_csv(code, duration):
    now = datetime.date.today()
    begin = now - datetime.timedelta(days=duration)
    fields = "TCLOSE;TOPEN;LCLOSE;CHG;PCHG"

    csv = "%s_%s_%d.csv" % (code, begin.strftime("%Y%m%d"), duration)
    url = 'http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&fields=%s' \
            % (code, begin.strftime("%Y%m%d"), now.strftime("%Y%m%d"), fields)
    print url

    html = get_data(url)

    with io.open(csv, 'w', encoding="gb2312") as f:
        f.write(html)

    return csv

def plot_SMA(df):
    mas = [30, 60, 90, 180]
    colors = dict(zip(mas, ['r', 'm', 'c', 'g']))

    total = len(df.index)

    for days in filter(lambda x: x < total, mas):
        avg = df.tail(days).mean()
        start = 1 - float(days)/total
        plt.axhline(y=avg, xmin=start, xmax=0.97, color=colors[days], label=str(days) + u'日均线')

def plot_csv(csv):
    df = pd.read_csv(csv, header=0, encoding='gb2312')

    df = df[::-1]
    df = df.reset_index(drop=True)
    print df.head(5)

    ax = df.plot(x=u'日期', y=[u'收盘价'])
    ax.set_xticks(df.index)
    ax.set_xticklabels(df[u'日期'], rotation=60)

    plot_SMA(df[u'收盘价'])

    plt.legend()

    plt.show()

def xxxx(name, csv):
    url = "http://hq.sinajs.cn/list=%s" % name

    html = get_data(url)

    print html

    pattern = re.compile(r'\d+\.\d+')

    match = re.findall(pattern, html)

    today = match[0]
    diff = match[1]
    percentage = match[2]

    print today, diff, percentage

    if percentage < -0.04:
        print "Do"
    elif percentage < -0.02:
        print "Do and check"
    else:
        print "Nothing"

    df = pd.read_csv(csv, header=0, encoding='gb2312')
    print len(df.index)
    print df[u'收盘价'].head(30).mean()
    print df[u'收盘价'].head(60).mean()
    print df[u'收盘价'].head(180).mean()

if __name__ == '__main__':
    #csv_file = save_csv("0000016", 180)
    #plot_csv(csv_file)

    csv_file = save_csv("0000300", 360)
    #plot_csv(csv_file)
    #plot_csv("0000300_20181110_180.csv")

    xxxx("s_sh000300", csv_file)
