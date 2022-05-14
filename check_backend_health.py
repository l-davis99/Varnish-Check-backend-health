#!/usr/bin/python3

import subprocess
import argparse

UNKNOWN = -1
OK = 0
WARNING = 1
CRITIAL = 2

parser = argparse.ArgumentParser(prog="check_varnish_health", description='Check the health of each Varnish backend')

# Add the arguments
parser.add_argument('--verbose', metavar='verbose', type=bool, default=False, help='Enable verbose output')
parser.add_argument('path', metavar='path', type=str, help='the path to list')
parser.add_argument('args', metavar='args', type=str, help='list backend parameter')

# Execute the parse_args() method
args = parser.parse_args()

verbose = args.verbose
varnishadm_path = args.path
varnishadm_args = args.args

command = subprocess.run([varnishadm_path, varnishadm_args], capture_output=True, text=True).stdout

cmd = command.split("\n")

b_healthy, b_sick, b_unknown = [], [], []
for l in cmd:
    if l.startswith("reload") or l.startswith("boot"):
        if "healthy" in l:
            p = l.partition('.')[2]
            b_healthy.append(p.split(" ")[0])
        if "sick" in l:
            p = l.partition('.')[2]
            b_sick.append(p.split(" ")[0])

if verbose: print(f"Healthy Backends: {b_healthy}")
if verbose: print(f"Sick Backends: {b_sick}")

if b_sick:
    print("%s backends are sick! %s" %  (len(b_sick), " ".join(b_sick)))

if b_healthy:
    print ("All %s backends are healthy" % (len(b_healthy)))


