import pandas as pd
import matplotlib.pyplot as plt
import time
from scipy.signal import savgol_filter

start = time.time()
pd.set_option('display.max_columns', 100)
df = pd.read_csv('inp.csv', parse_dates=True, header=None)
df.columns = ['date', 'hour', 'value']
df = df.drop('hour', axis=1)
df['date'] = pd.to_datetime(df['date'], errors='ignore')
df = df.resample('d', on='date').mean()

Statistical_band = int(input("Write the Statistical Band (UCL - LCL) in % = ")) / 100
EV_threshold_percent = int(input("Write EV threshold in % of actual historical average (0 - 100%)= ")) / 100
EV_threshold = EV_threshold_percent * df['value'].mean()
mean_historical = df['value'].mean()

Moving_average = []
m1 = 1
m2 = 7
for q in df['value'][7:-7]:
    Moving_average.append(df['value'][m1:m2].quantile(q=0.5))
    m1 += 1
    m2 += 1

UCL = []
LCL = []
p2 = 0
p3 = 7
for i in df['value'][7:-10]:
    UCL.append(df['value'][p2:p3].quantile(q=0.5 + (Statistical_band / 2)))
    LCL.append(df['value'][p2:p3].quantile(q=0.5 - (Statistical_band / 2)))
    p2 += 1
    p3 += 1

EV = []
j = 0
o1 = 0
o2 = 7
for j in df['value'][7:-15]:
    if (UCL[o1] - df['value'][o2]) > 0:
        EV1 = 0
    else:
        EV1 = df['value'][o2] - UCL[o1]
    if (df['value'][o2] - LCL[o1]) > 0:
        EV2 = 0
    else:
        EV2 = df['value'][o2] - LCL[o1]

    if EV1 != 0:
        EV.append(EV1)
    else:
        EV.append(EV2)
    o1 += 1
    o2 += 1

EV_normalized = []
for i in EV:
    if abs(i) < EV_threshold:
        EV_normalized.append(0)
    else:
        EV_normalized.append(i)

Change_points = []
z = 1
for b in EV_normalized[1:]:
    if EV_normalized[z] * EV_normalized[z-1] <= 0 and EV_normalized[z] != EV_normalized[z-1] and EV_normalized[z-1] == 0:
        Change_points.append(Moving_average[z])
    else:
        Change_points.append(0)
    z += 1

total_change_points = 0
for i in Change_points:
    if i != 0:
        total_change_points += 1

value = []
for i in df['value'][:-15]:
    value.append(i)

Moving_average = savgol_filter(Moving_average, 51, 3)
fig = plt.figure()
ax = plt.axes()
plt.plot(EV, label='EV')
plt.plot(UCL, label='UCL')
plt.plot(LCL, label='LCL')
plt.plot(Moving_average, label='Moving Average')
plt.plot(Change_points, label='Change Point')
plt.plot(value, label='Value')
ax.set(xlabel='Day', ylabel='Value')
plt.title('Change Points Detection. (total Change Points = {})'.format(total_change_points))
ax.grid()
plt.legend()
plt.show()


