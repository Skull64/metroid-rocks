#!/usr/bin/python3

import math
from datetime import datetime
from datetime import timedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def import_date(date):
    return datetime.strptime(date, '%Y-%m-%d')

class Run():
    def __init__(self, game, cat, name, date, l1, l2):
        self.game = game  # 1, 2, 3
        self.cat  = cat   # 1, 2, 3, 4
        self.name = name
        self.date = import_date(date)
        self.l1   = l1
        self.l2   = l2

def get_runs():
    runs = []
    with open('input.txt', 'r') as reader: lines = reader.readlines()
    for line in lines:
        tokens = line.split()
        game = int(tokens[0])
        cat = int(tokens[1])
        name = tokens[2]
        date = tokens[3]
        l1 = int(tokens[4])
        l2 = int(tokens[5])
        runs.append(Run(game, cat, name, date, l1, l2))
    return runs

def main():
    runs = get_runs()

    plot_data = [ [ [ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ] ],
                  [ [ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ] ],
                  [ [ [], [] ], [ [], [] ], [ [], [] ], [ [], [] ] ] ]

    for game in range(3):
        for cat in range(4):
            plot_data[game][cat][0].append(Run(0, 0, '', '2010-01-01', 1, 1))
            plot_data[game][cat][1].append(0)
            plot_data[game][cat][1].append(0)

    for run in runs:
        if plot_data[run.game-1][run.cat-1][1] == []: i = 0
        else: i = plot_data[run.game-1][run.cat-1][1][-1] + 1
        plot_data[run.game-1][run.cat-1][0].append(run)
        plot_data[run.game-1][run.cat-1][0].append(run)
        plot_data[run.game-1][run.cat-1][1].append(i)
        plot_data[run.game-1][run.cat-1][1].append(i)

    for game in range(3):
        for cat in range(4):
            plot_data[game][cat][0].append(Run(0, 0, '', datetime.today().strftime('%Y-%m-%d'), 1, 1))

    current_year = datetime.now().year
    xmax = import_date('%u-01-01' % (current_year + 1))
    xto_const = 0.008
    yto_const = 0.02

    plot_titles = ['Metroid Prime Low% Completions',
                   'Metroid Prime 2: Echoes Low% Completions',
                   'Metroid Prime 3: Corruption Low% Completions']
    xmins = [2010, 2012, 2015]
    spacings = [2, 2, 1]
    for game in range(3):
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111)

        # X-axis stuff
        xmin_year = xmins[game]
        xmin = import_date('%u-01-01' % xmin_year)
        xtextoff = timedelta(seconds=xto_const * (xmax - xmin).total_seconds())

        # Y-axis stuff
        spacing = spacings[game]
        ymax = 1
        for cat in range(4): ymax = max(max(plot_data[game][cat][1]), ymax)
        ymax = int((math.ceil(ymax / spacing) + 1) * spacing)
        ytextoff = yto_const * ymax

        # Plot the points
        for cat in range(4):
            dates = [run.date for run in plot_data[game][cat][0]]
            ax.plot(dates, plot_data[game][cat][1],
                     'o-', markersize=4, markevery=2)
            for i, run in enumerate(plot_data[game][cat][0]):
                if i%2 == 1: continue
                xy = (run.date, i/2)
                if run.l1 == 0:
                    ha = 'right'
                    xytext=(xy[0] - xtextoff, xy[1] + ytextoff)
                elif run.l1 == 1:
                    ha = 'center'
                    xytext=(xy[0], xy[1] + ytextoff)
                elif run.l1 == 2:
                    ha = 'left'
                    xytext=(xy[0] + xtextoff, xy[1] + ytextoff)
                ax.annotate(run.name, xy=xy, ha=ha, va='center', xytext=xytext)

        ax.legend(['Done', 'Hard', 'SS', 'Hard SS'], loc=2)
        ax.set_xlim([xmin, xmax])
        ax.xaxis.set_ticks([import_date('%u-01-01' % (year)) for year in range(xmin_year, current_year + 2)])
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.set_ylim([0, ymax])
        ax.set_yticks(range(0, ymax + spacing, spacing))
        ax.set_xlabel('Date of first completion')
        ax.set_ylabel('Completion index')
        ax.set_title(plot_titles[game])
        ax.grid()
        fname = 'prime%u.png' % (game + 1)
        print(fname)
        plt.savefig(fname)
        plt.close()

    plot_titles = ['Metroid Prime Series Low% Completions',
                   'Metroid Prime Series Hard Low% Completions',
                   'Metroid Prime Series Low% SS Completions',
                   'Metroid Prime Series Hard Low% SS Completions']
    xmins = [2010, 2010, 2014, 2015]
    spacings = [2, 2, 1, 1]
    for cat in range(4):
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111)

        # X-axis stuff
        xmin_year = xmins[cat]
        xmin = import_date('%u-01-01' % xmin_year)
        xtextoff = timedelta(seconds=xto_const * (xmax - xmin).total_seconds())

        # Y-axis stuff
        spacing = spacings[cat]
        ymax = 1
        for game in range(3): ymax = max(max(plot_data[game][cat][1]), ymax)
        ymax = int((math.ceil(ymax / spacing) + 1) * spacing)
        ytextoff = yto_const * ymax

        # Plot the points
        for game in range(3):
            dates = [run.date for run in plot_data[game][cat][0]]
            ax.plot(dates, plot_data[game][cat][1],
                     'o-', markersize=4, markevery=2)
            for i, run in enumerate(plot_data[game][cat][0]):
                if i%2 == 1: continue
                xy = (run.date, i/2)
                if run.l2 == 0:
                    ha = 'right'
                    xytext=(xy[0] - xtextoff, xy[1] + ytextoff)
                elif run.l2 == 1:
                    ha = 'center'
                    xytext=(xy[0], xy[1] + ytextoff)
                elif run.l2 == 2:
                    ha = 'left'
                    xytext=(xy[0] + xtextoff, xy[1] + ytextoff)
                ax.annotate(run.name, xy=xy, ha=ha, va='center', xytext=xytext)

        ax.legend(['Prime', 'Echoes', 'Corruption'], loc=2)
        ax.set_xlim([xmin, xmax])
        ax.xaxis.set_ticks([import_date('%u-01-01' % (year)) for year in range(xmin_year, current_year + 2)])
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.set_ylim([0, ymax])
        ax.yaxis.set_ticks(range(0, ymax + spacing, spacing))
        ax.set_xlabel('Date of first completion')
        ax.set_ylabel('Completion index')
        ax.set_title(plot_titles[cat])
        ax.grid()
        fname = 'cat%u.png' % (cat + 1)
        print(fname)
        plt.savefig(fname)
        plt.close()

if __name__ == '__main__':
    main()
