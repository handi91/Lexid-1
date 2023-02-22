import re
import os
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

match = 0
locations = []
list_folder = ['data/bn', 'data/lain-lain', 'data/ln', 'data/perda']
for folder in list_folder:
    for (root, dirs, files) in os.walk(folder, topdown=True):
        for arr in files:
            if root[-1:] != "\\":
                locations.append("{}\{}".format(root, arr))
            else:
                locations.append("{}{}".format(root, arr))
print(len(locations))

for turtle_file in locations:
    with open(turtle_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if re.search(r'"Pasal (\d+) : Pasal \1"', line):
                match += 1
            if re.search(r'"Pasal (\d+[A-Z]) : Pasal \1"', line):
                match += 1
            if re.search(r'"Pasal (\d+) : Pasal  \1"', line):
                match += 1
            if re.search(r'"ayat (\d+) : \(\1\)"', line):
                match += 1
            if re.search(r'"Pasal  (\d+)"', line):
                match += 1
            if re.search(r'"Pasal (\d+) ([A-Z])"', line):
                match += 1
            if re.search(r'"Pasal ([A-Z]) : Pasal (\d+) \1"', line):
                match += 1

    # with open(turtle_file, 'w') as f:
    #     for line in lines:
    #         if re.search(r'"Pasal (\d+) : Pasal \1"', line):
    #             line = re.sub(r'"Pasal (\d+) : Pasal \1"',
    #                           r'"Pasal \1"', line)
    #         if re.search(r'"Pasal (\d+[A-Z]) : Pasal \1"', line):
    #             line = re.sub(r'"Pasal (\d+) : Pasal  \1"',
    #                           r'"Pasal \1"', line)
    #         if re.search(r'"Pasal (\d+) : Pasal  \1"', line):
    #             line = re.sub(r'"Pasal (\d+) : Pasal  \1"',
    #                           r'"Pasal \1"', line)
    #         if re.search(r'"ayat (\d+) : \(\1\)"', line):
    #             line = re.sub(r'"ayat (\d+) : \(\1\)"',
    #                           r'"ayat \1"', line)
    #         if re.search(r'"Pasal  (\d+)"', line):
    #             line = re.sub(r'"Pasal  (\d+)"',
    #                           r'"Pasal \1"', line)
    #         if re.search(r'"Pasal (\d+) ([A-Z])"', line):
    #             line = re.sub(r'"Pasal (\d+) ([A-Z])"',
    #                           r'"Pasal \1\2"', line)
    #         if re.search(r'"Pasal ([A-Z]) : Pasal (\d+) \1"', line):
    #             line = re.sub(r'"Pasal ([A-Z]) : Pasal (\d+) \1"',
    #                           r'"Pasal \2\1"', line)
    #         f.write(line)

print(match)