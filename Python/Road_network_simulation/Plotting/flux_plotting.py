""" 
This file is used to plot the flux data for ingoing and outgoing cars from a predefined road network.
The data has been taken from an Excel file after the simulation was run 10 times for each injection probability.
The resulting plot displays the averaage flux of ingoing and outgoing cars and also plots the standard deviation as error bars.
"""

import matplotlib.pyplot as plt
import numpy as np

# Defining the variables
injection_prob = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

input_flux = [0.0000, 0.8222, 0.9674, 1.0119, 1.0352, 1.0500, 1.0458, 1.0485, 1.0510, 1.0523, 1.0504]
input_error = [0.0000, 0.0118, 0.0080, 0.0074, 0.0091, 0.0066, 0.0103, 0.0107, 0.0102, 0.0105, 0.0112]

output_flux = [0.0000, 0.3852, 0.4594, 0.4819, 0.4923, 0.5120, 0.4979, 0.4960, 0.4991, 0.4965, 0.4934]
output_error = [0.0000, 0.0076, 0.0094, 0.0070, 0.0110, 0.0291, 0.0125, 0.0112, 0.0058, 0.0075, 0.0131]

# Plotting the curves simultaneously 
fig, ax = plt.subplots()
ax.errorbar(injection_prob, input_flux, yerr = input_error, color = 'g', label = 'Input Flux')
ax.errorbar(injection_prob, output_flux, yerr = output_error, color = 'b', label = 'Output Flux')
ax.set_xlabel("Injection Probability")
ax.set_ylabel("Flux of Cars (num_cars/sim_steps)")
ax.set_title("Flux of Ingoing and Outgoing Cars")
ax.legend(loc ='best')

plt.show()
