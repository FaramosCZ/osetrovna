#! /usr/bin/env python3

import os
import csv
from pprint import pprint
from tabulate import tabulate

# =================================

# Load the REFERENCE VALUES
csv_file_path = 'REFERENCE_VALUES.csv'
REFERENCE_VALUES = {}

with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        column1, column2, column3, column4 = row
        REFERENCE_VALUES[column1.strip()] = [column2.strip(), column3.strip(), column4.strip()]

#pprint(REFERENCE_VALUES)
#pprint(REFERENCE_VALUES["Amoniak"])

# =================================

# Load the DISEASES
diseases_dir_path = './DISEASES/'
DISEASES = {}

file_list = [f for f in os.listdir(diseases_dir_path) if os.path.isfile(os.path.join(diseases_dir_path, f))]
for file in file_list:

    DISEASES[file[:-4]] = {}

    with open(os.path.join(diseases_dir_path, file), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            column1, column2 = row
            DISEASES[file[:-4]][column1.strip()] = column2.strip()

#pprint(DISEASES)
#pprint(DISEASES["Cukrovka"])

# =================================

# Generate results

ILLNESS = "Cukrovka"

headers = ["ENZYM", "HODNOTA"]
data = []

for enzym in DISEASES[ILLNESS]:

    symbol = DISEASES[ILLNESS][enzym]
    if symbol == "-":
        lower_limit = 0
        upper_limit = REFERENCE_VALUES[enzym][1]
    elif symbol == "+":
        lower_limit = REFERENCE_VALUES[enzym][2]
        upper_limit = float(REFERENCE_VALUES[enzym][2]) + 500
    else:
        lower_limit = REFERENCE_VALUES[enzym][1]
        upper_limit = REFERENCE_VALUES[enzym][2]

    import random
    random_float = random.uniform(float(lower_limit), float(upper_limit))
    random_float_rounded = round(random_float, 2)

    data.append([enzym, f"{random_float_rounded} {REFERENCE_VALUES[enzym][0]}"])

# =================================

table = tabulate(data, headers, tablefmt="pretty",  colalign=("left", "left"))
print(table)



