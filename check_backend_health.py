#!/usr/bin/python3

import subprocess
import argparse

UNKNOWN = -1
OK = 0
WARNING = 1
CRITIAL = 2

parser = argparse.ArgumentParser(prog="check_varnish_health", description='Check the health of each Varnish backend')

# Add the arguments
parser.add_argument('Path', metavar='path', type=str, help='the path to list')
parser.add_argument('Args', metavar='args', type=str, help='list backend parameter')

# Execute the parse_args() method
args = parser.parse_args()

varnishadm_path = args.Path
varnishadm_args = args.Args

#print(f"Path: {varnishadm_path}\nArgs: {varnishadm_args}")

command = subprocess.run([varnishadm_path, varnishadm_args], capture_output=True, text=True).stdout

b = command.split("\n")

b_healthy, b_sick, b_unknown = [], [], []
for l in b:
    if l.startswith("reload") or l.startswith("boot"):
        if "healthy" in l:
            b_healthy.append(l.split(" ")[1])
            print('healthy')
        if "sick" in l:
            b_sick.append(l.split(" ")[1])
        else:
            b_unknown.append(l.split(" ")[1])


if b_healthy:
    print ("All %s backends are healthy" % (len(b_healthy)))
