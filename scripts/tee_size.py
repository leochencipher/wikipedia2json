#!/usr/bin/env python3
#
# Reads a file line by line only once and copies it to others with arbitrary
# sizes. It works similarly to 'tee', but writes to the file until the given
# length.
#
# Let's say we have a compressed json file and we want to generate the 4G.json
# file with the first 4G of data, 8G.json with the first 8GB and also 16G.json.
# This can be accomplished by the following pipes:
#
# pbzcat all-50G.json.bz2 | ./tee_size 16G 16G.json quit | \
# ./tee_size 8G 8G.json | ./tee_size 4G 4G.json
#
# Please, notice 2 important requirements for the pipes to work correctly:
#   - Descending size order
#   - A 3rd argument in the first ./tee_size (otherwise, the files will be
#     correctly generated, but all the pipe will be consumed and it will take
#     longer to finish.
#
import sys

max_size = sys.argv[1]
f = open(sys.argv[2], 'w')
should_quit = len(sys.argv) > 3

if max_size[-1] == 'G':
    max_size = int(max_size[:-1]) * 1024 * 1024 * 1024
elif max_size[-1] == 'M':
    max_size = int(max_size[:-1]) * 1024 * 1024
elif max_size[-1] == 'K':
    max_size = int(max_size[:-1]) * 1024
else:
    max_size = int(max_size)

size = 0
done = False
for line in sys.stdin:
    if not done:
        size += len(line.encode())
        if size <= max_size:
            f.write(line)
            print(line, end='')
        elif should_quit:
            f.close()
            break
        else:
            f.close()
            done = True