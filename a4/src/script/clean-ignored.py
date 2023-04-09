import re
import os
import argparse

ignored = set()
parser = argparse.ArgumentParser(description='Remove the paths in ignore file from the generated ls.ta file')
parser.add_argument('-t', '--ta', type=str, required=True, help='The ls.ta file generated by script/final-containment.sh')
parser.add_argument('-i', '--ignored', type=str, required=True, help='The ignored.txt file generated by script/final-containment.sh')
parser.add_argument('-r', '--res', type=str, required=True, help='The file to output the processed ls.ta file to')
parser.add_argument('-o', '--overwrite', action="store_true", required=False, help='True if rewrite original ls.ta file')
args = parser.parse_args()

ta_file = args.ta
ignored_file = args.ignored
res_file = args.res
overwrite = args.overwrite

with open(ignored_file) as file:
    for line in file:
        ignored.add(line.strip())

with open(ta_file) as file, open(res_file, 'w') as res:
    for line in file:
        append = True
        # match instance path and cLinks paths
        match = re.search(r"^(cLinks|\$INSTANCE)\s+(.*) (.*)\r?\n?$", line)
        if match:
            type, p1, p2 = match.groups()
            if p1 in ignored or p2 in ignored:
                append = False
        if append:
            res.write(line)

if overwrite:
    with open(res_file) as res, open(ta_file, 'w') as file:
        for line in res:
            file.write(line)   
        os.remove(res_file)
