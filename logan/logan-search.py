import json
import re
import os
import argparse

conf_path = '~/.logan/logan_conf.json'


def fullpath(path):
    return os.path.abspath(os.path.expanduser(path))


def read_file(path, patterns):
    output = '\n{' + fullpath(path) + '}\n\n'

    try:
        with open(fullpath(path)) as file:
            lines = file.readlines()
            line_num = 1

            for line in lines:
                match = False
                for pattern in patterns:
                    if pattern.search(line) is not None:
                        match = True
                        break
                if match:
                    output += '[' + str(line_num) + '] ' + line

                line_num += 1
    except FileNotFoundError:
        output += 'File not found\n'

    return output


def listdir_r(directory):
    directory = os.path.abspath(directory)
    dirlist = []
    for path in os.listdir(directory):
        full_path = os.path.join(directory, path)
        dirlist.append(full_path)
        if os.path.isdir(full_path):
            dirlist += listdir_r(full_path)

    return dirlist


def main():
    parser = argparse.ArgumentParser(description='Monitors log files and directories for specified patterns')
    parser.add_argument('-C', metavar='conf', type=str, help='custom configuration path, overrides other arguments')
    parser.add_argument('-f', metavar='file', type=str, nargs='*', help='files to monitor')
    parser.add_argument('-d', metavar='dir', type=str, nargs='*', help='directories to monitor')
    parser.add_argument('-r', metavar='regex', type=str, nargs='+', help='patterns to find')
    parser.add_argument('-o', metavar='out', type=str, help='output file')
    args = parser.parse_args()

    conf = {}

    try:
        if args.C is None:
            with open(fullpath(conf_path)) as conf_file:
                conf = json.load(conf_file)

            if args.f is not None:
                conf['files'] = args.f
            if args.d is not None:
                conf['directories'] = args.d
            if args.r is not None:
                conf['patterns'] = args.r
            if args.o is not None:
                conf['output'] = args.o

        else:
            with open(fullpath(args.C)) as conf_file:
                conf = json.load(conf_file)

        output = ""
        patterns = []

        for pattern in conf['patterns']:
            patterns.append(re.compile(pattern))

        paths = []
        paths += conf['files']

        for directory in conf['directories']:
            directory = fullpath(directory)
            for path in listdir_r(directory):
                if os.path.isfile(os.path.join(directory, path)):
                    paths.append(os.path.join(directory, path))

        for path in paths:
            output += read_file(path, patterns)

        output_filename = fullpath(conf['output'])
        if not os.path.exists(os.path.dirname(output_filename)):
            os.makedirs(os.path.dirname(output_filename))

        with open(output_filename, 'w') as output_file:
            output_file.write(output)
    except FileNotFoundError:
        print("Configuration file not found")


if __name__ == "__main__":
    main()
