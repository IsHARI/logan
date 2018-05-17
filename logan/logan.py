import json
import os
import argparse
import subprocess
import time
import getpass

conf_path = './logan_conf.json'

parser = argparse.ArgumentParser(description='Monitors log files and directories for specified patterns')
parser.add_argument('-C', metavar='conf', type=str, help='custom configuration path, overrides other arguments')
parser.add_argument('-f', metavar='file', type=str, nargs='+', help='files to monitor')
parser.add_argument('-d', metavar='dir', type=str, nargs='+', help='directories to monitor')
parser.add_argument('-r', metavar='regex', type=str, nargs='+', help='patterns to find')
parser.add_argument('-o', metavar='out', type=str, help='output file')
parser.add_argument('-t', metavar='T', type=int, help='interval of time between log searches')
parser.add_argument('-R', metavar='id', type=str, help='stop the logan job with the given ID')

args = parser.parse_args()

interval = 0

if args.C is not None:
    with open(os.path.expanduser(args.C)) as conf_file:
        conf = json.load(conf_file)
        interval = conf['interval']

elif args.t is not None:
    interval = args.t

else:
    with open(os.path.expanduser(conf_path)) as conf_file:
        conf = json.load(conf_file)
        interval = conf['interval']


with open('/var/spool/cron/crontabs' + getpass.getuser(), 'w') as crontab:
    crontab.write()
