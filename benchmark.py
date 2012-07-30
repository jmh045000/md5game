#!/usr/bin/python -u

import commands
import itertools
import sys

TESTS = [
    '-finline-functions',
    '-funswitch-loops',
    '-fpredictive-commoning',
    '-fgcse-after-reload',
    '-ftree-vectorize',
    '-fvect-cost-model',
    '-ftree-partial-pre',
    '-fipa-cp-clone',
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
    rc, out = commands.getstatusoutput('gcc -O2 -ffast-math -fwhole-program ' + options + ' -Wall -o md5game -lpthread -DBENCHMARK md5game.c')
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

