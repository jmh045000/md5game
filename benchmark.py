#!/usr/bin/python -u

import commands
import itertools
import sys

TESTS = [
    '-falign-functions',
    '-falign-jumps',
    '-falign-labels',
    '-falign-loops',
    '-fauto-inc-dec',
    '-fbranch-target-load-optimize',
    '-fbranch-target-load-optimize2',
    '-fcaller-saves',
    '-fcprop-registers',
    '-fcrossjumping',
    '-fcse-follow-jumps',
    '-fcse-skip-blocks',
    '-fcx-limited-range',
    '-fdce',
    '-fdefer-pop',
    '-fdelayed-branch',
    '-fdelete-null-pointer-checks',
    '-fdse',
    '-fexpensive-optimizations',
    '-ffinite-math-only',
    '-fgcse',
    '-fgcse-after-reload',
    '-fgcse-lm',
    '-fguess-branch-probability',
    '-fif-conversion',
    '-fif-conversion2',
    '-findirect-inlining',
    '-finline-functions',
    '-finline-small-functions',
    '-fipa-cp-clone',
    '-fipa-pure-const',
    '-fipa-reference',
    '-floop-parallelize-all',
    '-fmath-errno',
    '-foptimize-sibling-calls',
    '-fpeephole2',
    '-fpredictive-commoning',
    '-fregmove',
    '-freorder-blocks',
    '-freorder-functions',
    '-frerun-cse-after-loop',
    '-frounding-math',
    '-fsched-interblock',
    '-fsched-spec',
    '-fschedule-insns',
    '-fschedule-insns2',
    '-fsignaling-nans',
    '-fsplit-wide-types',
    '-fstack-protector',
    '-fstrict-aliasing',
    '-fstrict-overflow',
    '-fthread-jumps',
    '-ftree-builtin-call-dce',
    '-ftree-ccp',
    '-ftree-ch',
    '-ftree-copyrename',
    '-ftree-dce',
    '-ftree-dominator-opts',
    '-ftree-dse',
    '-ftree-fre',
    '-ftree-pre',
    '-ftree-sra',
    '-ftree-switch-conversion',
    '-ftree-ter',
    '-ftree-vectorize',
    '-ftree-vrp',
    '-funit-at-a-time',
    '-funsafe-math-optimizations',
    '-funswitch-loops',
    '-fvect-cost-model',
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
    rc, out = commands.getstatusoutput('gcc ' + options + ' -Wall -o md5game -lpthread -DBENCHMARK md5game.c')
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
        else:
            sys.stderr.write('MD5 failed with options: ' + options + '\n')

for i in range(len(TESTS)):
    for options in itertools.combinations(TESTS, i):
        run_program(options)
        
sys.exit(0)

