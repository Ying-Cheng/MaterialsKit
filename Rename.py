import os
import csv

mapping = {}
with open('Name.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if len(row) == 2:
            current_name, new_name = row
            mapping[current_name] = new_name

directory = "./out"

for filename in os.listdir(directory):
    name_before_extension, file_extension = os.path.splitext(filename)
    if name_before_extension in mapping:
        new_filename = mapping[name_before_extension] + file_extension
        current_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(current_path, new_path)
        print(f'Renamed file: {filename} -> {new_filename}')
