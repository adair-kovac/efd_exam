import matplotlib.pyplot as plt

def plot(matrix, observation_depths):
    fig, ax = plt.subplots()
    plt.plot(matrix)
    plt.legend(observation_depths)
    fig.savefig("plot")