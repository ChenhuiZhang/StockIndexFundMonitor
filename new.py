# coding=utf-8
import io
import datetime
import requests
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

def plot_csv(csv):
    df = pd.read_csv(csv, header=0, encoding='gb2312')

    df = df[::-1]
    df = df.reset_index(drop=True)
    print df.head(5)

    print len(df.index)
    rows = len(df.index)

    print df.tail(30)
    print df.tail(30)[u'收盘价']
    print df.tail(60)[u'收盘价'].mean()
    avg30 = df.tail(90)[u'收盘价'].mean()
    #print df.ix[-30:, u'收盘价']
    #print df.ix[-30:, u'收盘价'].mean()
    #avg30 = df.ix[-30:, u'收盘价'].mean()

    ax = df.plot(x=u'日期', y=[u'收盘价'])
    ax.set_xticks(df.index)
    ax.set_xticklabels(df[u'日期'], rotation=60)
    #df.plot.line(x=u'日期', avg30)

    s = float(30)/rows
    print s
    if rows > 30:
        avg30 = df.tail(30)[u'收盘价'].mean()
        start = 1 - float(30)/rows
        plt.axhline(y=avg30, xmin=start, xmax=1, color='r', linestyle='-', label=u'30日均线')
    if rows > 60:
        avg60 = df.tail(60)[u'收盘价'].mean()
        start = 1 - float(60)/rows
        plt.axhline(y=avg60, xmin=start, xmax=1, color='m', linestyle='-', label=u'60日均线')
    if rows > 90:
        avg90 = df.tail(90)[u'收盘价'].mean()
        start = 1 - float(90)/rows
        plt.axhline(y=avg90, xmin=start, xmax=1, color='c', linestyle='-', label=u'90日均线')
    if rows > 180:
        avg180 = df.tail(180)[u'收盘价'].mean()
        start = 1 - float(180)/rows
        plt.axhline(y=avg180, xmin=start, xmax=1, color='g', linestyle='-', label=u'180日均线')

    plt.legend()

    plt.show()

if __name__ == '__main__':
    #csv_file = save_csv("0000016", 180)
    #plot_csv(csv_file)

    csv_file = save_csv("0000300", 300)
    plot_csv(csv_file)
    #plot_csv("0000300_20181110_180.csv")

