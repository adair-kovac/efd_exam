import math
import numpy as np
from matplotlib import pyplot as plt

deep_temp = 17 # degree C, estimate
A = 16 - deep_temp # constant, no idea what to guess this as, need to plug surface temp into eq to find it
one_day = 24 * 60 * 60 # seconds, the period of the diurnal cycle
omega = 2 * math.pi/one_day
thermal_diffusivity = 0.4
damping_depth = math.sqrt(2*thermal_diffusivity/omega) / 100 # m to cm


def soil_temp_function(time, depth):
    return deep_temp + A * math.exp(-depth/damping_depth) * math.cos(omega*time - depth/damping_depth)


times = range(0, one_day + 1)
depths = [0, 1.6, 3.9, 5.8, 8.5, 10.4, 15, 25] # actually these are cm, not m

fig, ax = plt.subplots()
for depth in depths:
    ax.plot(times, [soil_temp_function(time, depth) for time in times], label=str(depth))

ax.legend()
fig.savefig("model_fig")

