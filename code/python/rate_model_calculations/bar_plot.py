import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 0.25
#fig = plt.subplots(figsize =(12, 8))
fig = plt.subplots()

# set height of bar
rate = [1, 2, 3, 0]
cb = [2, 3, 3, 0]

# Set position of bar on X axis
br1 = np.arange(len(rate))
br2 = [x + barWidth for x in br1]

# Make the plot
plt.bar(br1, rate, color ='r', width = barWidth,
		edgecolor ='grey', label ='Rate Model')
plt.bar(br2, cb, color ='g', width = barWidth,
		edgecolor ='grey', label ='CB Model')

plt.title('Conductance Based Model vs Rate Model')
# Adding Xticks
plt.xlabel('Iapp', fontweight ='bold', fontsize = 15)
plt.ylabel('Burst Frequency Hz', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(rate))],
		['1', '2', '3', '4'])

plt.legend()
plt.show()
