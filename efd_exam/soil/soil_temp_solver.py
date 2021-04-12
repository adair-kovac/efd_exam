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
alpha = .4e-6
observation_depths_str = ["1.6", "3.9", "5.8", "8.5", "10.4", "15", "25"]


def main():
    matrix, observation_depths, observation_times, original_data = initialize_data()
    for j in range(1, len(observation_depths_str)):
        for i in range(1, len(observation_times)):
            matrix[i][j] = finite_difference.temp_at_next_time(matrix, observation_times,
                                                               observation_depths, i-1, j,
                                                               alpha, matrix[i-1][j])
    observation_depths_str_model = observation_depths_str + ["30"]
    time_column = original_data["seconds_since"]
    soil_temp_plot.plot(time_column, matrix, observation_depths_str_model, "Finite Difference Numerical Solution")
    columns = ["T-" + depth for depth in observation_depths_str]
    soil_temp_plot.plot(time_column, original_data[columns], observation_depths_str, "Actual Data")
    model_data_dim = matrix[:, :-1]
    soil_temp_plot.plot(time_column, original_data[columns] - model_data_dim, observation_depths_str,
                        "Actual Minus Modelled")
    soil_temp_plot.contour_plot(observation_depths[:-1], time_column, original_data[columns],
                                "Actual Temperature by Depth and Time")


def initialize_data():
    observation_depths = [float(x)/100 for x in observation_depths_str] # convert cm to m
    surface_boundary_temperatures_by_time = []
    data = data_loader.load_data()
    observation_times = data["seconds_since"]
    for i, row in data.iterrows():
        surface_boundary_temperatures_by_time.append(float(row["T-1.6"]))
    deep_temperature = np.average(data["T-25"])
    initial_temperatures_by_depth = [data.iloc()[0]["T-" + depth] for depth in observation_depths_str]

    num_rows = len(observation_times)
    num_columns = len(initial_temperatures_by_depth) + 1
    observation_depths.append(.3) # Adding a final row for the temperature at depth BC

    matrix = np.zeros((num_rows, num_columns))
    matrix[:, 0] = surface_boundary_temperatures_by_time
    initial_temperatures_by_depth.append(deep_temperature)
    matrix[0] = initial_temperatures_by_depth
    matrix[:, -1] = deep_temperature
    return matrix, observation_depths, observation_times, data



if __name__=="__main__":
    main()