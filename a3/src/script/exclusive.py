import argparse
import random

# Meant to return the exclusive dependencies between two extraction files

parser = argparse.ArgumentParser(
    description="Perform statistical analysis on 3 ls.ta files"
)
parser.add_argument(
    "-a1", "--a1-file", type=argparse.FileType("r"), help="First method ls.ta file"
)
parser.add_argument(
    "-a2", "--a2-file", type=argparse.FileType("r"), help="Second method ls.ta file"
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    required=True,
    help="The file path to output the results",
)
args = parser.parse_args()

# init
set_A1 = set()
set_A2 = set()
a1_file = args.a1_file
a2_file = args.a2_file
output_file = args.output

# read dependencies of each method
for file in [a1_file, a2_file]:
    for line in file:
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ")

        if len(parts) != 3:
            continue

        type, from_file, to_file = parts
        key = f"{from_file} -> {to_file}"

        if type == "cLinks":
            if file == args.a1_file:
                set_A1.add(key)
            elif file == args.a2_file:
                set_A2.add(key)
            elif file == args.a3_file:
                set_A3.add(key)

# set operations
union = set_A1.union(set_A2)
exclusive_A1 = set_A1 - set_A2
exclusive_A2 = set_A2 - set_A1

# format output
output = []
output.append("---------------------Exclusive to A1--------------------\n")
while len(exclusive_A1) > 0:
    output.append(exclusive_A1.pop())
    output.append("\n")

output.append("---------------------Exclusive to A1--------------------\n")
while len(exclusive_A2) > 0:
    output.append(exclusive_A2.pop())
    output.append("\n")

# write to files
with open(output_file, "w") as of:
    for line in output:
        of.write(line)
