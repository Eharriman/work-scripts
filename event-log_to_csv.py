"""
Script Name: event-log_to_csv.py
Author: Ethan Harriman
Date: 2025-08-14
Description: This script converts a FortiGate log export (.log txt) to a csv. Event log column headers
             are extracted from the .log file as keys. Row data is listed. The script is invariant
             to the type of event log, spcecific filters applied to the export, or specific columns
             used.
"""

import csv
import re

# File paths
input_file = r'[Input location]'
output_file = r'[Output location]]'

# Regex to extract column headers passed on ""= pattern
pattern = re.compile(r'(\w+)=("[^"]*"|\S+)')

rows = []

all_keys = set()

# Construct keys for column headers and row data
with open(input_file, "r") as f:
    for line in f:
        entry = {}
        for match in pattern.finditer(line):
            key = match.group(1)
            val = match.group(2).strip('"')
            entry[key] = val
            all_keys.add(key)
        rows.append(entry)

# Sort keys
fieldnames = sorted(all_keys)

# Construct csv
with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"Event log converted to csv. CSV file saved to: {output_file}")
