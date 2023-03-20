import argparse
import random

parser = argparse.ArgumentParser(description='Perform statistical analysis on 3 ls.ta files')
parser.add_argument('-a1', '--a1-file', type=argparse.FileType('r'), help='First method ls.ta file')
parser.add_argument('-a2', '--a2-file', type=argparse.FileType('r'), help='Second method ls.ta file')
parser.add_argument('-a3', '--a3-file', type=argparse.FileType('r'), help='Third method ls.ta file')
parser.add_argument('-o', '--output', type=str, required=True, help='The file path to output the results')
args = parser.parse_args()

# init
set_A1 = set()
set_A2 = set()
set_A3 = set()
a1_file = args.a1_file
a2_file = args.a2_file
a3_file = args.a3_file
output_file = args.output

# read dependencies of each method
for file in [a1_file, a2_file, a3_file]:
    for line in file:
        line = line.strip()
        if not line:
            continue
        parts = line.split(' ')

        if len(parts) != 3:
            continue
    
        type, from_file, to_file = parts
        key = f'{from_file} -> {to_file}'

        if type == 'cLinks':
            if file == args.a1_file:
                set_A1.add(key)
            elif file == args.a2_file:
                set_A2.add(key)
            elif file == args.a3_file:
                set_A3.add(key)

# set operations for quantitative/qualitative analyses
union = set_A1.union(set_A2, set_A3)
intersection = set_A1.intersection(set_A2, set_A3)
common = set_A1.intersection(set_A2).intersection(set_A3)
exclusive_A1 = set_A1.difference(set_A2, set_A3)
exclusive_A2 = set_A2.difference(set_A1, set_A3)
exclusive_A3 = set_A3.difference(set_A1, set_A2)
intersect_A1A2 = set_A1.intersection(set_A2)
intersect_A2A3 = set_A2.intersection(set_A3)
intersect_A1A3 = set_A1.intersection(set_A3)
# set partitions
size_A1 = len(set_A1)
size_A2 = len(set_A2)
size_A3 = len(set_A3)
size_common = len(common)
size_union = len(union)
size_exclusive_A1 = len(exclusive_A1)
size_exclusive_A2 = len(exclusive_A2)
size_exclusive_A3 = len(exclusive_A3)
size_intersect_A1A2 = len(intersect_A1A2)
size_intersect_A2A3 = len(intersect_A2A3)
size_intersect_A1A3 = len(intersect_A1A3)

# Performance analysis
population = union
# len(population) = 241570 as of 03-20-2023, for kernel

# https://www.surveysystem.com/sscalc.htm  
sample_size = 384

sample = random.choices(list(population), k=sample_size)
true_positives = len(common.intersection(sample))
false_positives = len(union.difference(common).intersection(sample))
false_negatives = len(common.difference(sample))
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f_measure = (2 * (precision * recall)) / (precision + recall)

# format output
output = []
output.append('---------------------Sets--------------------\n')
output.append(f'A1: {a1_file.name}\n')
output.append(f'A2: {a2_file.name}\n')
output.append(f'A3: {a3_file.name}\n')
output.append('-------------------Results-------------------\n')
output.append(f'Size of A1: {size_A1}\n')
output.append(f'Size of A2: {size_A2}\n')
output.append(f'Size of A3: {size_A3}\n')
output.append(f'{"-"*45}\n')
output.append(f'Size of common set: {size_common}\n')
output.append(f'Size of union set: {size_union}\n')
output.append(f'Size of exclusive A1: {size_exclusive_A1}\n')
output.append(f'Size of exclusive A2: {size_exclusive_A2}\n')
output.append(f'Size of exclusive A3: {size_exclusive_A3}\n')
output.append(f'Size of A1 intersect A2: {size_intersect_A1A2}\n')
output.append(f'Size of A2 intersect A3: {size_intersect_A2A3}\n')
output.append(f'Size of A1 intersect A3: {size_intersect_A1A3}\n')
output.append(f'{"-"*45}\n')
output.append('Common elements:\n')
output.append('\n'.join(common) + '\n')
output.append(f'{"-"*45}\n')
output.append('Elements exclusive to A1:\n')
output.append('\n'.join(exclusive_A1) + '\n')
output.append(f'{"-"*45}\n')
output.append('Elements exclusive to A2:\n')
output.append('\n'.join(exclusive_A2) + '\n')
output.append(f'{"-"*45}\n')
output.append('Elements exclusive to A3:\n')
output.append('\n'.join(exclusive_A3) + '\n')
output.append(f'{"-"*45}\n')
output.append(f'Precision: {precision:.2f}\n')
output.append(f'Recall: {recall:.2f}\n')
output.append(f'F-measure: {f_measure:.2f}\n')
output.append(f'{"-"*45}\n')


with open(output_file, 'w') as of:
    for line in output:
        of.write(line)