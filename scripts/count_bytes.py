#!/usr/bin/env python3
import sys

max_size = int(sys.argv[1])

size = 0
for line in sys.stdin:
    size += len(line.encode())
    if size < max_size:
        print(line, end='')
    elif size == max_size:
        print(line, end='')
        sys.exit(0)
    else:
        sys.exit(0)