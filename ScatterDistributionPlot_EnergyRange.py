#!/usr/bin/env python3

from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import pandas as pd

filename = input(f'Please type your filename: ')
energy_keyword = 'E'

df = pd.read_csv(filename, sep='\t').mul(2625.5) # convert Hartree to kJ/mol

energy_ranges = [
        (-1530*2625.5, -1520*2625.5),#20
        (-1460*2625.5, -1450*2625.5),#19
        (-1380*2625.5, -1370*2625.5),#18
        (-1305*2625.5, -1295*2625.5),#17
        (-1230*2625.5, -1220*2625.5),#16
        (-1150*2625.5, -1140*2625.5),#15
        (-1075*2625.5, -1065*2625.5),#14
        (-1000*2625.5, -990*2625.5),#13
        (-920*2625.5, -910*2625.5),#12
        (-845*2625.5, -835*2625.5),#11
        (-770*2625.5, -760*2625.5),#10
        (-690*2625.5, -680*2625.5),#9
        (-615*2625.5, -605*2625.5),#8
        (-540*2625.5, -530*2625.5),#7
        (-465*2625.5, -455*2625.5),#6
        (-385*2625.5, -375*2625.5),#5
        (-310*2625.5, -300*2625.5),#4-body
        (-235*2625.5, -225*2625.5),#3-body
        (-155*2625.5, -145*2625.5),#2-body
        (-80*2625.5, -70*2625.5)#1-bosy
        ]

def scatter_hist(x, y, ax, ax_histx, ax_histy, mae):
    diff = abs(max(x) - max(y)) + abs(min(x) - min(y))
    if diff < 100:
        v = x.tolist() + y.tolist()
        vx_max = vy_max = max(v)
        vx_min = vy_min = min(v)
        vx_diff = vy_diff = (vx_max - vx_min)/10
    else:
        vx_max = max(x)
        vy_max = max(y)
        vx_min = min(x)
        vy_min = min(y)
        vx_diff = (vx_max - vx_min)/20
        vy_diff = (vy_max - vy_min)/20
    ax_histx.tick_params(axis='x', labelbottom=False)
    ax_histx.set(ylabel='Counts')
    ax_histy.tick_params(axis='y', labelleft=False)
    ax_histy.set(xlabel='Counts')
    ax.plot([0, 1], [0, 1], transform=ax.transAxes, color='black', linewidth=0.5)
    ax.set_xlabel('Actual E (kJ/mol)')
    ax.set_ylabel('Predicted E (kJ/mol)')
    ax.set_xlim(0, vx_max-vx_min)
    ax.set_ylim(0, vy_max-vy_min)
    ax.text(0, vy_max-vy_min, f'E MAE={"%.2f" % (mae)} kJ/mol', fontsize=18)
    ax.ticklabel_format(useOffset=False)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.scatter(x-vx_min, y-vy_min, s=1)
    #xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    #lim = (int(xymax/binwidth) + 1) * binwidth
#    if vx_diff < 0.0001:
#        binwidth = 0.0000025
#    elif 0.0001 <= vx_diff < 0.001:
#        binwidth = 0.000025
#    elif 0.001 <= vx_diff < 0.01:
#        binwidth = 0.00025
#    elif 0.01 <= vx_diff < 0.1:
#        binwidth = 0.0025
#    else:
#        binwidth = 0.025
    binwidth = 100
    xbins = np.arange(vx_min, vx_max, binwidth) #100
    ybins = np.arange(vy_min, vy_max, binwidth)
    ax_histx.hist(x, bins=xbins)
    ax_histy.hist(y, bins=ybins, orientation='horizontal')

def scatter_hist_inset_axes(x, y):
    fig = plt.figure(layout='constrained')
    ax = fig.add_gridspec(top=0.75, right=0.75).subplots()
    #ax.set(aspect=1)
    ax_histx = ax.inset_axes([0, 1.05, 1, 0.25], sharex=ax)
    ax_histy = ax.inset_axes([1.05, 0, 0.25, 1], sharey=ax)
    scatter_hist(x, y, ax, ax_histx, ax_histy)
    fig.savefig(f'{filename.split(".")[0]}_{energy_keyword}_{start}_{end}.png')
    plt.close()

def scatter_hist_gridspec(x, y, mae):
    fig = plt.figure(figsize=(6, 6))
    gs = fig.add_gridspec(2, 2,  width_ratios=(4, 1), height_ratios=(1, 4),
         left=0.15, right=0.95, bottom=0.15, top=0.95,
         wspace=0.1, hspace=0.1)
    ax = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
    scatter_hist(x, y, ax, ax_histx, ax_histy, mae)
    fig.savefig(f'{filename.split(".")[0]}_{energy_keyword}_{start}_{end}.png', dpi=300)
    plt.close()

for i, (start, end) in enumerate(energy_ranges):
    df_i = df[(df['#actual_energy_value'] >= start) & (df['#actual_energy_value'] < end)]
    x = df_i['#actual_energy_value']
    y = df_i['predicted_energy_value']
    mae = abs(df_i['#actual_energy_value'] - df_i['predicted_energy_value']).mean()
    #scatter_hist_inset_axes(x, y)
    scatter_hist_gridspec(x, y, mae)

#fig1 = plt.figure()
#gs1 = GridSpec(4, 4)
#
#fig2 = plt.figure()
#gs2 = GridSpec(4, 4)
#
#scatter1 = fig1.add_subplot(gs2[1:4, 0:3])
#scatter1_hist_y = fig1.add_subplot(gs1[0,0:3])
#scatter1_hist_x = fig1.add_subplot(gs1[1:4, 3])
#
#scatter1.set_xlabel('Actual E (Ha)')
#scatter1.set_ylabel('Predict E (Ha)')
#scatter1.scatter(df['#actual_energy_value'], df['predicted_energy_value'])
#scatter1_hist_x.hist(df['#actual_energy_value'], orientation = 'horizontal', bins=100)
#scatter1_hist_y.hist(df['predicted_energy_value'], orientation = 'vertical', bins=100)
#fig1.savefig('pred_e_train.png', dpi=300)
#
#scatter2 = fig2.add_subplot(gs2[1:4, 0:3])
#scatter2_hist_x = fig2.add_subplot(gs2[1:4, 3])
#scatter2_hist_y = fig2.add_subplot(gs2[0,0:3])
#
#scatter2.set_xlabel('Actual F (Ha/Angstrom)')
#scatter2.set_ylabel('Predict F (Ha/Angstrom)')
#scatter2.scatter(df['actual_force_value'], df['predicted_force_value'])
#scatter2_hist_x.hist(df['actual_force_value'], orientation = 'horizontal', bins=100)
#scatter2_hist_y.hist(df['predicted_force_value'], orientation = 'vertical', bins=100)
#fig2.savefig('pred_f_train.png', dpi=300)
