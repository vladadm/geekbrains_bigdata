#!/usr/local/opt/python@3.9/bin/python3.9

import sys, re

for line in sys.stdin:
    line = ''.join(re.findall('\d+', line))
    print(line)
