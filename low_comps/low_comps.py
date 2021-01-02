#!/usr/bin/python3

import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams['font.family'     ] = 'serif'
plt.rcParams['mathtext.default'] = 'regular'

class Run():
    def __init__(self, game, cat, name, date, l1, l2):
        self.game = game  # 1, 2, 3
        self.cat  = cat   # 1, 2, 3, 4
        self.name = name
        self.date = import_date(date)
        self.l1   = l1
        self.l2   = l2

def import_date(date): return datetime.strptime(date, '%Y-%m-%d')

def main():
    runs = get_runs()
    for game in [1, 2, 3   ]: plot_runs_by_game(runs, game)
    for cat  in [1, 2, 3, 4]: plot_runs_by_cat (runs, cat )

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

def plot_runs_by_game(runs_all, game):
    game_names = ['Metroid Prime', 'Metroid Prime 2: Echoes',
                  'Metroid Prime 3: Corruption']
    cat_names = ['Done', 'Hard', 'SS', 'Hard SS']

    xmin_list = [2010, 2012, 2015]
    yspace_list = [2, 2, 1]

    # X-axis stuff
    xmin_year = xmin_list[game - 1]
    xmax_year = datetime.now().year + 1
    xmin = import_date('%u-01-01' % (xmin_year))
    xmax = import_date('%u-01-01' % (xmax_year))
    xto_const = 0.008
    xtextoff = timedelta(seconds=xto_const * (xmax - xmin).total_seconds())
    xlabels = [import_date('%u-01-01' % (x)) for x in
               range(xmin_year, xmax_year + 1)]

    # Y-axis stuff
    yspace = yspace_list[game - 1]
    ymax = 0
    for cat in [1, 2, 3, 4]:
        runs = [x for x in runs_all if x.game == game and x.cat == cat]
        ymax = max(ymax, len(runs))
    ymax = int((np.ceil(ymax / yspace)) * yspace)
    yticks = list(range(0, ymax + 2 * yspace, yspace))
    yto_const = 0.02
    ytextoff = yto_const * ymax

    # Make plot
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(12.0, 9.0)
    for cat in [1, 2, 3, 4]:
        runs = [x for x in runs_all if x.game == game and x.cat == cat]
        dates = [xmin] + [x.date for x in runs] + [datetime.today()]
        yvals = list(range(len(runs) + 1)) + [len(runs)]
        ax.step(dates, yvals, 'o-', where='post', markersize=4,
                markevery=range(len(runs) + 1), label=cat_names[cat - 1])
        for i, run in enumerate(runs):
            xy = (run.date, i + 1)
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
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(0, ymax + yspace)
    ax.set_yticks(yticks)
    ax.xaxis.set_ticks(xlabels)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_xlabel('Date of first completion')
    ax.set_ylabel('Completion index')
    ax.set_title('%s Low%% Completions' % (game_names[game - 1]))
    ax.grid()
    ax.legend(loc='upper left')
    fname = 'prime%u.png' % (game)
    print(fname)
    plt.savefig(fname)
    plt.close()

def plot_runs_by_cat(runs_all, cat):
    game_names = ['Prime', 'Echoes', 'Corruption']
    cat_names = ['Low%', 'Hard Low%', 'Low% SS', 'Hard Low% SS']

    xmin_list = [2010, 2010, 2014, 2015]
    yspace_list = [2, 2, 1, 1]

    # X-axis stuff
    xmin_year = xmin_list[cat - 1]
    xmax_year = datetime.now().year + 1
    xmin = import_date('%u-01-01' % (xmin_year))
    xmax = import_date('%u-01-01' % (xmax_year))
    xto_const = 0.008
    xtextoff = timedelta(seconds=xto_const * (xmax - xmin).total_seconds())
    xlabels = [import_date('%u-01-01' % (x)) for x in
               range(xmin_year, xmax_year + 1)]

    # Y-axis stuff
    yspace = yspace_list[cat - 1]
    ymax = 0
    for game in [1, 2, 3]:
        runs = [x for x in runs_all if x.game == game and x.cat == cat]
        ymax = max(ymax, len(runs))
    ymax = int((np.ceil(ymax / yspace)) * yspace)
    yticks = list(range(0, ymax + 2 * yspace, yspace))
    yto_const = 0.02
    ytextoff = yto_const * ymax

    # Make plot
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(12.0, 9.0)
    for game in [1, 2, 3]:
        runs = [x for x in runs_all if x.game == game and x.cat == cat]
        dates = [xmin] + [x.date for x in runs] + [datetime.today()]
        yvals = list(range(len(runs) + 1)) + [len(runs)]
        ax.step(dates, yvals, 'o-', where='post', markersize=4,
                markevery=range(len(runs) + 1), label=game_names[game - 1])
        for i, run in enumerate(runs):
            xy = (run.date, i + 1)
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
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(0, ymax + yspace)
    ax.set_yticks(yticks)
    ax.xaxis.set_ticks(xlabels)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_xlabel('Date of first completion')
    ax.set_ylabel('Completion index')
    ax.set_title('Metroid Prime Series %s Completions' % (cat_names[cat - 1]))
    ax.grid()
    ax.legend(loc='upper left')
    fname = 'cat%u.png' % (cat)
    print(fname)
    plt.savefig(fname)
    plt.close()

if __name__ == '__main__': main()
