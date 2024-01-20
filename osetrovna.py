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

DISEASES_AMOUNT = len(file_list)

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

def generate_disease(id):

    saved_file_path = os.path.join("./SAVED_RESULTS/", f"{id}.result")
    if os.path.exists(saved_file_path):
        with open(saved_file_path, 'r') as file:
                table = file.read()

    else:
        disease_id = int(id) % DISEASES_AMOUNT
        ILLNESS = list(DISEASES.items())[disease_id][0]
        # DEBUG:
        #pprint(ILLNESS)

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

        with open(saved_file_path, 'w') as result_file:
            result_file.write(table)

    # =================================

    # Get the terminal size
    import shutil
    terminal_size = shutil.get_terminal_size()
    terminal_width = terminal_size.columns

    # Calculate the left padding to center the table
    left_padding = (terminal_width - len(table.splitlines()[0])) // 2
    # Center each line of the table individually
    centered_table = "\n".join(line.center(terminal_width) for line in table.splitlines())

    # Print the centered table
    print(centered_table)

# =================================


while True:
    user_input = input("VLOŽTE ID VZORKU: ")

    # Check if the input is a positive integer
    if user_input.isdigit() and int(user_input) > 0:
        os.system('clear')
        print("Výsledky pro vzorek:", user_input)
        generate_disease(user_input)
    else:
        print("ERROR: Zadejte kladné celé číslo")
