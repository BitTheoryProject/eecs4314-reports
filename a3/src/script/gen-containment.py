import os
import re
import glob
import json
import argparse

# Parse args
parser = argparse.ArgumentParser(description='Generate the <containment-file-name>.contain file')
parser.add_argument('-t', '--ta-raw', type=str, required=True, help='The raw.ta file')
parser.add_argument('-ss', '--subsystems', type=str, required=True, help='The raw.ta file')
parser.add_argument('-c', '--contain', type=str, required=True, help='The containment file name')
parser.add_argument('-s', '--source', type=str, required=True, help='The path to the freebsd source code')
args = parser.parse_args()

ta_file = args.ta_raw
subsystems_file = args.subsystems
contain_file = args.contain
src_path = args.source

# Create a containment file from generated TA and source
# Usage: python gen-containment.py -t <raw_ta_dependency_file> -c <containment_file_name> -ss <subsystems-json-file> -s <src_path>

# Subsystems json file structure:
# {
#   "IPC.ss": { <- subsystem
#     "KQUEUE.ss": [ <- subsystem
#       ["exact", "sys/kern/kern_event.c"], <- leaf in form ["exact"|"glob"|"regex", "pattern"], means the file matched by pattern is a component of parent
#       ["exact", "sys/kern/kern_kqueue.c"]
#     ],
#     "PTY.ss": [
#       ["exact", "sys/kern/tty_*.c"],
#     ]
#   }
# }
# Pattern types:
# exact -> exact match pattern
# glob -> glob match pattern
# regex -> regex match pattern

sep = os.sep

# Read subsystems JSON
with open(subsystems_file) as f:
    subsystems = json.load(f)

# Read ta_dependency_file dependencies
dependencies = []
with open(ta_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        type, from_file, _ = line.split()
        # We only care about the concrete files
        if type == "$INSTANCE":
            dependencies.append(from_file)

dependencies_hash = {d: 1 for d in dependencies}
toplevel = []
lowlevel = []
root = 'freebsd'

def print_subsystem(d, fn, parent=None):
    new_parent = parent or root
    for subsystem, value in d.items():
        toplevel.append(f'contain {new_parent} {subsystem}\n')
        if isinstance(value, dict):
            print_subsystem(value, fn, subsystem)
        elif isinstance(value, list):
            for entry in value:
                pattern_type, pattern = entry
                if pattern_type == 'glob':
                    # match pattern using glob
                    matches = glob.glob(f'{src_path}{sep}{pattern}', recursive=True)
                    for match in matches:
                        match = match.replace(f'{src_path}{sep}', "")
                        # make sure file is a raw.ta instance
                        if dependencies_hash.get(f'{root}{sep}{match}'):
                            fn(subsystem, f'{root}{sep}{match}')
                        else:
                            print(f'{root}{sep}{match}')
                elif pattern_type == 'regex':
                    # match pattern using regex
                    match = next((s for s in dependencies if re.search(pattern, s)), None)
                    if match:
                        fn(subsystem, match)
                elif pattern_type == 'exact':
                    # match pattern exactly
                    if f'{root}{sep}{pattern}' in dependencies:
                        fn(subsystem, f'{root}{sep}{pattern}')
                else:
                    raise ValueError(f'Invalid pattern type: {pattern_type}')

# Add file level contain
def add_file_to_subsystem(subsystem, file):
    if file.endswith(('.c', '.cpp', '.h')):
        lowlevel.append(f'contain {subsystem} {file}\n')

# Recursively build subsystems
print_subsystem(subsystems, add_file_to_subsystem)

with open(contain_file, 'w') as cf:
    #Print top-level contains
    for contain in toplevel:
        cf.write(contain)
    cf.write("\n\n")

    #Print file-level contains
    for contain in lowlevel:
        cf.write(contain)
    cf.close()
