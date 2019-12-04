import numpy as np
from scipy import stats
import math
import matplotlib.pyplot as plt

dx = np.arange(0, 200, 0.01)
#x = (dx-1500)/(np.sqrt(2)*100)
gamma = stats.gamma.cdf(dx, 100)

plt.figure(figsize=(6, 4))
plt.plot(dx, gamma, color='blue')
plt.xlabel('Vcal', fontsize=8)
plt.ylabel('Hit Occupancy', fontsize=8)
plt.grid(which="major")
plt.xticks([100], [ "threshold"])
plt.yticks([0, 0.5, 1], ["", "50%", "100%"])
plt.savefig("./figure/scurve.png")
plt.show()
