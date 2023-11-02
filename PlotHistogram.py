#!/usr/bin/env python3

from decimal import Decimal, ROUND_HALF_UP
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from scipy.stats import norm

def RoundOff(num, decimal):
    # print(num)
    str_deci = 1
    for _ in range(decimal):
        str_deci = str_deci / 10
    str_deci = str(str_deci)
    result = Decimal(str(num)).quantize(Decimal(str_deci), rounding=ROUND_HALF_UP)
    result = float(result)
    # print(result)
    return result

def linear_fit(x, y):
    # Fit a linear regression line (y = mx + b)
    coefficients = np.polyfit(x, y, 1)
    m, b = coefficients
    # Create the fitted line using the calculated coefficients
    fitted_line = m * x + b
    return fitted_line

def CreateHistogram(data, output_filename):
    bin_width = 0.02
    x_min = 0
    x_max = 2.0
    x_interval = 0.2
    y_min = 0
    y_max = 20
    y_interval = 2
    font_size = 20

    num_bins = int(RoundOff((max(data) - min(data)) / bin_width, 0))
    hist, bins, _ = plt.hist(data, bins=num_bins, edgecolor='black')

    plt.xlabel('RMSD (Angstrom)', fontsize=font_size)
    plt.ylabel('Number of data', fontsize=font_size)

    plt.xticks(np.arange(x_min, x_max, x_interval), fontsize=font_size)
    plt.yticks(np.arange(y_min, y_max, y_interval), fontsize=font_size)

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.text(x_min + x_interval, y_max - y_interval, f'Bin width = {bin_width}', fontsize=font_size, ha='left')

    # mean, std = norm.fit(data)
    # x = np.linspace(x_min, x_max, 100)
    # fitted_pdf = norm.pdf(x, mean, std)

    # plt.plot(x, fitted_pdf * len(data) * bin_width, 'r--', linewidth=2)

    sns.kdeplot(data, color='red', linestyle='--', linewidth=2) #, label='Fitted PDF')

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close()

current_directory = os.getcwd()
input_files = [filename for filename in os.listdir(current_directory) if filename.endswith(".csv")]

for csv_file in input_files:
    csv_filename = os.path.splitext(csv_file)[0]
    raw_data = np.genfromtxt(csv_file, delimiter=',', dtype=None, encoding=None)
    # print(f'raw_data: {raw_data}')
    data = raw_data[1:, 1].astype(float)
    # print(f'data: {data}')
    CreateHistogram(data, f'{csv_filename}.png')
