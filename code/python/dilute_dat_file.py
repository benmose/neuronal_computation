import os
import sys
from utils import leave_only_given_locations_in_file
from config import dat_dir_path

if len(sys.argv) < 4:
    print(sys.argv[0], ": Wrong number of arguments!")
    print("Usage: ")
    print(sys.argv[0], " <filename> <x location> <y location> [unstable point number]")
    sys.exit(1)



filename = sys.argv[1]

x = int(sys.argv[2])
y = int(sys.argv[3])

loc = None

if len(sys.argv) > 4:
    loc = int(sys.argv[4])


leave_only_given_locations_in_file(filename, x, y, loc)
