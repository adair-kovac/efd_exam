"""
Finite-difference numerical solution of the heat equation, without assuming equal intervals of initial/boundary
condition points.

Equation: dT/dt = alpha * d^2T/dz^2

Letting time (t) be indexed by i and depth (z) be indexed by j, the finite difference approximation is:

T_(i+1) = alpha * (t_(i+1) - t_i) * approximate(d^2T/dz^2) + T_i

where approximate(d^2T/dz^2) is:

(approx(dT_(i,j+1/2)/dz) - approx(dT_(i, j-1/2)/dz)) / ((z_j+1 + z_j-1)/2)

and

approx(dT_(i,j+1/2)/dz) = (T_(i,j+1) - T_(i,j))/(z_j+1 - z_j)
approx(dT_(i,j-1/2)/dz) = (T_(i,j) - T_(i,j-1))/(z_j - z_j-1)

We can't make common textbook simplifications since delta_z is not always the same.
"""


def temp_at_next_time(matrix, times, depths, i, j, alpha, temp_i):
    new_temp = alpha * (times[i + 1] - times[i]) * second_spatial_deriv(matrix, depths, i, j) + temp_i
    return new_temp


def second_spatial_deriv(matrix, depths, i, j):
    dT1 = first_spatial_deriv(matrix, depths, i, j-1)
    dT2 = first_spatial_deriv(matrix, depths, i, j)
    z_1 = depths[j - 1]
    z_2 = depths[j + 1]

    central_difference = (dT2 - dT1) / ((z_2 + z_1) / 2)
    return central_difference


def first_spatial_deriv(matrix, depths, i, lower_j):
    T_1 = matrix[i][lower_j]
    T_2 = matrix[i][lower_j + 1]
    z_1 = depths[lower_j]
    z_2 = depths[lower_j + 1]
    difference = (T_2 - T_1) / (z_2 - z_1)
    return difference
