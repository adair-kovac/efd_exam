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
alpha = .4

def main():
    matrix, observation_depths, observation_times = initialize_data()
    deriv_matrix = initialize_deriv_matrix(matrix, observation_times, observation_depths)
    print(deriv_matrix)


def initialize_deriv_matrix(matrix, observation_times, observation_depths):
    deriv_matrix = np.zeros_like(matrix)
    i = 0
    for j in range(1, matrix.shape[1]-1):
        deriv_matrix[i, j] = first_deriv_temp_time(i, j, matrix, observation_times)
    j = 0
    for i in range(1, matrix.shape[0]-1):
        deriv_matrix[i, j] = alpha*calc_second_deriv_temp_with_depth(i, j, matrix, observation_depths)
    return deriv_matrix





def initialize_data():
    observation_depths_str = ["1.6", "3.9", "5.8", "8.5", "10.4", "15", "25"]
    observation_depths = [float(x) for x in observation_depths_str]
    surface_boundary_temperatures_by_time = []
    data = data_loader.load_data()
    observation_times = []
    for i, row in data.iterrows():
        observation_times.append(get_time(int(row["Day"]), int(row["Hour (UTC)"]), int(row["Min"])))
        surface_boundary_temperatures_by_time.append(float(row["T-1.6"]))
    deep_temperature = np.average(data["T-25"])
    initial_temperatures_by_depth = [data.iloc()[0]["T-" + depth] for depth in observation_depths_str]

    num_columns = len(observation_times)
    num_rows = len(initial_temperatures_by_depth) + 1
    observation_depths.append(35) # Adding a final row for the temperature at depth BC

    matrix = np.zeros((num_rows, num_columns))
    matrix[0] = surface_boundary_temperatures_by_time
    matrix[-1] = deep_temperature
    matrix[:-1, 0] = initial_temperatures_by_depth
    return matrix, observation_depths, observation_times


def first_deriv_temp_depth(i_1, i_2, j, matrix, observation_depths):
    return (matrix[i_1, j] - matrix[i_2, j])/(observation_depths[i_1] - observation_depths[i_2])


def calc_second_deriv_temp_with_depth(i, j, matrix, observation_depths):
    dif_1 = first_deriv_temp_depth(i-1, i, j, matrix, observation_depths)
    dif_2 = first_deriv_temp_depth(i, i+1, j, matrix, observation_depths)
    del_z = observation_depths[i+1] = observation_depths[i-1]
    return (dif_2 - dif_1)/del_z


def first_deriv_temp_time(i, j, matrix, observation_times):
    del_temp = matrix[i, j+1] - matrix[i, j-1]
    del_t = observation_times[j+1] - observation_times[j-1]
    return del_temp/del_t


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