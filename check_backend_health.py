#!/usr/bin/python3
#
# Author: Luke Davis (luked@positive-internet.com)
# Date: 2022-05-14
# Description: Script to check varnish backends
#

import subprocess
import argparse

# define nrpe agent exit status
UNKNOWN = -1
OK = 0
WARNING = 1
CRITIAL = 2

# handle cli-based parameters
parser = argparse.ArgumentParser(prog="check_varnish_health", description='Check the health of each Varnish backend')
parser.add_argument('--verbose', type=bool, default=False, help='Enable verbose output')
parser.add_argument('path', metavar='path', type=str, help='the path to list')
parser.add_argument('args', metavar='args', type=str, help='list backend parameter')

# Execute the parse_args() method
args = parser.parse_args()

# assign arguments to variables
verbose = args.verbose
varnishadm_path = args.path
varnishadm_args = args.args

# run varnishadm command based on above variables and parameters
command = subprocess.run([varnishadm_path, varnishadm_args], capture_output=True, text=True).stdout

# split output of varnishadm command 
cmd = command.split("\n")

# define arrays for backend names depending on status of for loop
b_healthy, b_sick, b_unknown = [], [], []

# loop over each line from varnishadm output
for l in cmd:

    # only get the lines we're interested in.
    if l.startswith("reload") or l.startswith("boot"):

        # depending on what the line contains, place it in the correct array
        if "healthy" in l:
            p = l.partition('.')[2]
            b_healthy.append(p.split(" ")[0])
        if "sick" in l:
            p = l.partition('.')[2]
            b_sick.append(p.split(" ")[0])

# verbose ouput to see what the script is detectign
if verbose: print(f"Healthy Backends: {b_healthy}")
if verbose: print(f"Sick Backends: {b_sick}\n")

if b_sick:
    print("CRITICAL: %s backends are sick! %s" %  (len(b_sick), " ".join(b_sick)))
    exit(CRITICAL)

if not b_sick and not b_healthy:
    print("UNKNOWN: No backends found (check verbose output)")
    exit(UNKNOWN)

if b_healthy:
    print ("OK: All %s backends are healthy" % (len(b_healthy)))
    exit(OK)
