import os
import re
import glob
import json
import argparse

# Parse args
parser = argparse.ArgumentParser(description='Generate the <containment-file-name>.contain file')
parser.add_argument('-t', '--ta-file', type=str, required=True, help='The ta file name to generate')
parser.add_argument('-ss', '--subsystems', type=str, required=True, help='The subsystems file')
parser.add_argument('-s', '--source', type=str, required=True, help='The path to the freebsd source code (make sure root is "freebsd")')
args = parser.parse_args()

subsystems_file = args.subsystems
ta_file = args.ta_file
src_path = args.source
root = 'freebsd'

# Create a raw.ta file from header includes, for the defined subsystems.
# Usage: python gen-ta-file.py -t <raw_ta_dependency_filename> -ss <subsystems-json-file> -s <src_path>

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
    Parses a file and return a set of full paths of files it depends on.
    """
    dependencies = set()
    try:
        with open(filename, encoding="utf-8", errors="ignore") as f:
            try:
                for line in f:
                    if line.startswith("#include"):
                        include_file = line.split()[1].strip('"<>"')
                        # Get the full path of the include file : potential bug, todo
                        # include_file_path = os.path.abspath(os.path.join(os.path.dirname(filename), include_file))
                        # print(include_file_path)
                        # dependencies.add(include_file_path.replace(src_path, root))
                        dependencies.add(include_file)
            except Exception as err:
                # print(filename, err)
                pass
    except Exception as err:
        # print(f'{filename}\n')
        pass
    return dependencies

# All dependencies
dependencies = {}
links = []
instances = []

def print_subsystem(d, fn, parent=None):
    for subsystem, value in d.items():
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
        # From dependencies
        dependencies[file] = parse_file_dependencies(file.replace('freebsd', src_path, 1))
        
        if dependencies[file]:
            for dep in dependencies[file]:
                instances.append(f'$INSTANCE {dep} cFile\n')
                links.append(f'cLinks {file} {dep}\n')

# Recursively build subsystems
print_subsystem(subsystems, add_file_dependencies)

with open(ta_file, 'w') as tf:
    tf.write('FACT TUPLE :\n')

    # Print top-level contains
    for instance in instances:
        tf.write(instance)
    tf.write("\n\n")

    # Print file-level contains
    for link in links:
        tf.write(link)
    tf.close()