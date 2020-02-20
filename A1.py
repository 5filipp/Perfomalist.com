import pandas as pd
import matplotlib.pyplot as plt
import statistics as stat
import time

start = time.time()
pd.set_option('display.max_columns', 100)

df = pd.read_csv('inp.csv', index_col=0, parse_dates=True, header=None)
df.index = pd.to_datetime(df.index, errors='ignore')
df.index += pd.to_timedelta(df[1], unit='h')

i = 0
average_list = []
for i in range(168):
    average = df.resample('168H', base=i).asfreq().bfill().mean()
    average_list.append(average[2])
    i += 1

std_dev = stat.stdev(average_list)
UCL = [x + std_dev for x in average_list]
LCL = [x - std_dev for x in average_list]
value = [x for x in df[2][-168:]]
print(time.time()-start)

fig = plt.figure()
ax = plt.axes()
plt.plot(average_list, label='Average')
plt.plot(UCL, label='UCL')
plt.plot(LCL, label='LCL')
plt.plot(value, label='Value')
ax.set(xlabel='Week Hours', ylabel='Value', title='Weekly performance chart')
ax.grid()
plt.legend()
plt.show()

