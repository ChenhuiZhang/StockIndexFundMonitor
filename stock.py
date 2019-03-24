import tushare as ts
import matplotlib.pyplot as plt
import datetime

id = 'hs300'

#df = ts.get_realtime_quotes(id)

#print(df[['code', 'name', 'price', 'pre_close']])

#print(df)

now = datetime.date.today()
begin = now - datetime.timedelta(days=60)

print(now, begin)

df = ts.get_hist_data('hs300', begin.isoformat(), now.isoformat())
#df = ts.get_hist_data('hs300',start='2018-01-01',end='2019-03-01')

new = df.sort_values(by="date" , ascending=True)
print(new.head(30))

df = new.head(30)

price = [q for q in df["close"]]
date = [q for q in df.index]

print(date)
print(price)

plt.plot(date, price)
plt.show()
