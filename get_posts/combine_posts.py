#!/usr/bin/python3

import os
import sys
from datetime import datetime

def main():
    if len(sys.argv) != 2:
        raise Exception('Usage: python get_combined_posts.py <username>')
    username = sys.argv[1].lower()

    bases = ['m2k2', 'sda']

    # Read posts
    lines = {}
    for base in bases:
        with open('posts_raw/%s/%s.txt' % (base,username)) as r:
            lines[base] = r.readlines()
    num_lines_total = sum([len(x) for x in lines.values()])

    # Get timestamps
    timestamps = {}
    for base in bases:
        timestamps[base] = [None] * len(lines[base])
        for i, line in enumerate(lines[base]):
            time_str = ' '.join(line.split()[:3])[:-1].lower()
            timestamp = datetime.strptime(time_str, '%Y-%m-%d %I:%M:%S %p')
            timestamps[base][i] = timestamp

    lines['combined'] = []
    indices = {base: 0 for base in bases}
    while sum(indices.values()) < num_lines_total:
        ts_current = {x: timestamps[x][indices[x]] for x in bases if
                      indices[x] < len(lines[x])}
        base = [x for x in ts_current.keys() if
                ts_current[x] == min(ts_current.values())][0]
        lines['combined'].append(lines[base][indices[base]])
        indices[base] += 1

    # Create directory for combined posts
    combined_dir = 'posts_raw/combined'
    if not os.path.exists(combined_dir): os.makedirs(combined_dir)

    # Write combined posts to file
    w = open('%s/%s.txt' % (combined_dir, username), 'w')
    for line in lines['combined']: w.write(line)
    w.close()

if __name__ == '__main__': main()
