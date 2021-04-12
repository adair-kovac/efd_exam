import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

def plot(times, matrix, observation_depths, title):
    fig, ax = plt.subplots()
    plt.plot(times, matrix)
    plt.legend(observation_depths)
    plt.title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (C)")
    fig.savefig(title)
    plt.close(fig)

def contour_plot(times, depths, data, title):
    fig, ax = plt.subplots()
    contour = plt.contour(times, depths, data)
    contour.clabel(fontsize=12, inline=1, fmt='%.1f')
    ax.set_xlabel("Depth (m)")
    ax.set_ylabel("Time (s)")
    ax.yaxis.set_major_formatter(EngFormatter())
    plt.title(title)
    fig.savefig(title)
    plt.close(fig)
