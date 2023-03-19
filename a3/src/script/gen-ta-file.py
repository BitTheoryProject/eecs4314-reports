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
    if os.path.isfile(file_path):
        return file_path
    else:
        return None

def find_directories_with_headers(root_directory):
    """
    Recursively scan root_directory for directories that contain header files.
    Return a dictionary that maps each directory to the set of header files it contains.
    """
    header_dirs = {}
    for dirpath, dirnames, filenames in os.walk(root_directory):
        headers = set(f for f in filenames if f.endswith('.h') or f.endswith('.c'))
        if headers:
            header_dirs[dirpath] = headers
    return header_dirs

def parse_file_dependencies(file, header_dirs):
    """
    Parses a file and return a set of full paths of files it depends on.
    """
    dependencies = set()
    try:
        with open(file, encoding="utf-8", errors="ignore") as f:
            contents = f.read()
            # Limitation: might not find all include types
            includes = re.findall(r'^\s*#\s*include\s+[<"].*?([^\/>"]+)[>"]', contents, flags=re.MULTILINE)
            for include_file in includes:
                for header_dir, header_files in header_dirs.items():
                    if include_file in header_files:
                        # Limitation: This finds the first match, might not be the right header file
                        full_path = file_exists_in_directory(header_dir, include_file)
                        if full_path:
                            dependencies.add(full_path.replace(src_path, root, 1))
                            break
    except Exception:
        pass
    return dependencies

# All dependencies
dependencies = {}
links = []
instances = set()
print('Finding header locations...')
header_dirs = find_directories_with_headers(src_path)
print(f'Found {len(header_dirs)} header locations.')

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
                        fn(subsystem, match)
                elif pattern_type == 'exact':
                    # match pattern exactly
                    if file_exists_in_directory(src_path, pattern):
                        fn(subsystem, match)
                else:
                    raise ValueError(f'Invalid pattern type: {pattern_type}')

# Add include level dependencies
def add_file_dependencies(subsystem, file):
    if file.endswith(('.c', '.cpp', '.h')):
        file_clean = file.replace(src_path, root, 1)
        instances.add(f'$INSTANCE {file_clean} cFile\n')

        # From dependencies
        dependencies[file] = parse_file_dependencies(file, header_dirs)
        
        if dependencies[file]:
            for dep in dependencies[file]:
                links.append(f'cLinks {file_clean} {dep}\n')

print('Finding include dependencies...')
# Recursively build include dependencies
print_subsystem(subsystems, add_file_dependencies)

print(f'Creating {ta_file}...')
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