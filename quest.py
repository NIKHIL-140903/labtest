


import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

np.random.seed(0)  
traffic_data = np.random.randint(50, 150, size=1440) 
noise = np.random.normal(0, 10, 1440) 
traffic_data_noisy = traffic_data + noise 


b, a = signal.butter(3, 0.05) 
traffic_data_smooth = signal.filtfilt(b, a, traffic_data_noisy)


hourly_traffic_averages = np.mean(traffic_data_smooth.reshape(24, 60), axis=1)


plt.figure(figsize=(10, 6))
minutes = np.arange(1440)

plt.plot(minutes, traffic_data_noisy, label='Noisy Traffic Data', alpha=0.5)
plt.plot(minutes, traffic_data_smooth, label='Smoothed Traffic Data', color='red')
plt.scatter(np.arange(0, 1440, 60), hourly_traffic_averages, label='Hourly Averages', color='green', zorder=5)

plt.title('Traffic Data: Noisy, Smoothed, and Hourly Averages')
plt.xlabel('Time (Minutes)')
plt.ylabel('Number of Vehicles')
plt.legend()
plt.grid(True)


threshold = 100
exceed_indices = np.where(traffic_data_smooth > threshold)[0]

consecutive_limit = 20
exceed_periods = []


current_period = [exceed_indices[0]]
for i in range(1, len(exceed_indices)):
    if exceed_indices[i] == exceed_indices[i - 1] + 1:
        current_period.append(exceed_indices[i])
    else:
        if len(current_period) >= consecutive_limit:
            exceed_periods.append(current_period)
        current_period = [exceed_indices[i]]

if len(current_period) >= consecutive_limit:
    exceed_periods.append(current_period)


for period in exceed_periods:
    plt.axvspan(period[0], period[-1], color='yellow', alpha=0.3)

plt.show()


for period in exceed_periods:
    print(f"Traffic exceeded {threshold} vehicles/min from minute {period[0]} to {period[-1]}")



