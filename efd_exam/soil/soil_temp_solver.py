'''

We solve the heat equation:

dT/dt = alpha * d^2 T/dz^2

using Euler's method.

Our conditions are:

I.C. - T(t=0, z)
B.C. - T(z -> infinity) [this is the same for all t]
B.C. - T(t, z = 1.5)

'''

import numpy as np
from soil import soil_data_loader as data_loader
from soil import finite_difference
from soil import soil_temp_plot
alpha = .4 / 100 # Converting to cm
observation_depths_str = ["1.6", "3.9", "5.8", "8.5", "10.4", "15", "25"]

def main():
    matrix, observation_depths, observation_times = initialize_data()
    for j in range(1, len(observation_depths_str)):
        for i in range(1, len(observation_times)):
            matrix[i][j] = finite_difference.temp_at_next_time(matrix, observation_times,
                                                               observation_depths, i-1, j,
                                                               alpha, matrix[i-1][j])
    soil_temp_plot.plot(matrix, observation_depths_str)


def initialize_data():
    observation_depths = [float(x) for x in observation_depths_str]
    surface_boundary_temperatures_by_time = []
    data = data_loader.load_data()
    observation_times = []
    for i, row in data.iterrows():
        observation_times.append(get_time(int(row["Day"]), int(row["Hour (UTC)"]), int(row["Min"])))
        surface_boundary_temperatures_by_time.append(float(row["T-1.6"]))
    deep_temperature = np.average(data["T-25"])
    initial_temperatures_by_depth = [data.iloc()[0]["T-" + depth] for depth in observation_depths_str]

    num_rows = len(observation_times)
    num_columns = len(initial_temperatures_by_depth) + 1
    observation_depths.append(30) # Adding a final row for the temperature at depth BC

    matrix = np.zeros((num_rows, num_columns))
    matrix[:, 0] = surface_boundary_temperatures_by_time
    initial_temperatures_by_depth.append(deep_temperature)
    matrix[0] = initial_temperatures_by_depth
    return matrix, observation_depths, observation_times


def get_time(day, hour, min):
    initial_day = 17
    initial_hour = 0
    initial_min = 5
    return one_day() * (day - initial_day) + one_hour() * (hour - initial_hour) + one_min() * (min - initial_min)


def one_day():
    return 24*60*60


def one_hour():
    return 60*60


def one_min():
    return 60


if __name__=="__main__":
    main()