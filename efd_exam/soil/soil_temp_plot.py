import matplotlib.pyplot as plt

def plot(times, matrix, observation_depths, filename):
    fig, ax = plt.subplots()
    plt.plot(times, matrix)
    plt.legend(observation_depths)
    fig.savefig(filename)
    plt.close(fig)

def contour_plot(times, depths, data, filename):
    fig, ax = plt.subplots()
    contour = plt.contour(times, depths, data)
    contour.clabel(fontsize=12, inline=1, fmt='%.1f')
    fig.savefig(filename)
    plt.close(fig)
