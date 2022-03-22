#!/usr/local/opt/python@3.9/bin/python3.9

import sys
import random

batch = []
count = 0
size = random.randint(1, 6)

for line in sys.stdin:
    count += 1
    batch.append(line.strip())
    if count == size:
        print(','.join(batch))
        count = 0
        size = random.randint(1, 6)
        batch = []


