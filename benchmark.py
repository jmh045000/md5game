#!/usr/bin/python -u

import commands
import itertools
import sys

TESTS = [
    '-fbranch-target-load-optimize2',
    '-fcx-limited-range',
    '-ffinite-math-only',
    '-fipa-reference',
    '-floop-parallelize-all',
    '-f-no-math-errno',
    '-foptimize-sibling-calls',
    '-frounding-math',
    '-fschedule-insns',
    '-fschedule-insns2',
    '-fsignaling-nans',
    '-f-no-stack-protector',
    '-fthread-jumps',
    '-funsafe-math-optimizations',
    '-fwhole-program',
]

max = 0

def test_generator():
    list = []
    for t in TESTS:
        list.append(t)
    return list

def run_program(optimizations):
    global max
    options = ' '.join(optimizations)
    rc, out = commands.getstatusoutput('gcc -O3 ' + options + ' -Wall -o md5game -lpthread -DBENCHMARK md5game.c')
    if rc == 0:
        sys.stderr.write('Running with options: ' + options + '\n')
        rc, out = commands.getstatusoutput('./md5game')
        if rc == 0:
            count = 0
            total = 0
            for line in out.splitlines():
                total = total + int(line)
                count = count + 1
            total = total / count
            if max < total:
                print 'Best options so far:', options, '\nWith average of', total
                max = total
        else:
            sys.stderr.write('MD5 failed with options: ' + options + '\n')

for i in range(len(TESTS)):
    for options in itertools.combinations(TESTS, i):
        run_program(options)
        
sys.exit(0)

