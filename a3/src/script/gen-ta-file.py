import os
import re
import glob
import json
import argparse

# Parse args
parser = argparse.ArgumentParser(description='Generate the <containment-file-name>.contain file')
parser.add_argument('-ss', '--subsystems', type=str, required=True, help='The subsystems file')
parser.add_argument('-t', '--ta-file', type=str, required=True, help='The ta file name to generate')
parser.add_argument('-s', '--source', type=str, required=True, help='The path to the freebsd source code')
args = parser.parse_args()

subsystems_file = args.subsystems
ta_file = args.ta_file
src_path = args.source

# Create a containment file from Header includes, for the defined subsystems.
# Usage: python gen-containment.py -c <containment_file_name> -ss <subsystems-json-file> -s <src_path>

# Subsystems json file structure:
# {
#   "IPC.ss": { <- subsystem
#     "KQUEUE.ss": [ <- subsystem
#       ["exact", "sys/kern/kern_event.c"], <- leaf in form ["exact"|"glob", "pattern"], means the file matched by pattern is a component of parent
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


def file_exists_in_directory(directory, filename):
    """
    Verifies if a file exists in a directory.
    """
    file_path = os.path.join(directory, filename)
    return os.path.isfile(file_path)


def parse_file_dependencies(filename):
    """
    Parses a file and return a set of files it depends on.
    """
    dependencies = set()
    with open(filename) as f:
        for line in f:
            if line.startswith("#include"):
                include_file = line.split()[1].strip('"<>"')
                dependencies.add(include_file)
    return dependencies

# All dependencies
dependencies = {}
links = []
# toplevel = []
# lowlevel = []
instances = []
root = 'freebsd'

def print_subsystem(d, fn, parent=None):
    new_parent = parent or root
    for subsystem, value in d.items():
        # toplevel.append(f'contain {new_parent} {subsystem}\n')
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
                        fn(subsystem, f'{root}{sep}{match}')
                elif pattern_type == 'exact':
                    # match pattern exactly
                    if file_exists_in_directory(src_path, pattern):
                        fn(subsystem, f'{root}{sep}{pattern}')
                else:
                    raise ValueError(f'Invalid pattern type: {pattern_type}')

# Add file level contain
def add_file_dependencies(subsystem, file):
    if file.endswith(('.c', '.cpp', '.h')):
        # lowlevel.append(f'$INSTANCE {subsystem} cSubSystem\n')
        # From dependencies
        dependencies[file] = parse_file_dependencies(file)
        
        for dep in dependencies[file]:
            instances.append(f'$INSTANCE "{dep}" cFile\n')
            links.append(f'cLinks {file} {dep}\n')

# Recursively build subsystems
print_subsystem(subsystems, add_file_dependencies)

with open(ta_file, 'w') as tf:
    tf.write('FACT TUPLE :\n')
    # # Print top-level contains
    # for contain in toplevel:
    #     tf.write(contain)
    # tf.write("\n\n")

    # # Print file-level contains
    # for contain in lowlevel:
    #     tf.write(contain)

    # Print top-level contains
    for instance in instances:
        tf.write(instance)
    tf.write("\n\n")

    # Print file-level contains
    for link in links:
        tf.write(link)
    tf.close()