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


def prompt_user_filters():
    filters = []
    add_filters = input("Do you want to apply filters? (y/n): ").strip().lower()
    if add_filters != 'y':
        return filters

    while True:
        key = input("Enter column/header name for filter application: ").strip()
        value_string = input("Enter allowed value(s) (comma-separated for multiple): ").strip()
        values = [v.strip() for v in value_string.split(",")]

        # Check for continuation prompt
        cont = input("Do you wish to add another filter? (y/n): ").strip().lower()
        if cont != 'y':
            break
    return filters


def filter_check(entry, filters):
    # Function applies filter to row entry
    # Check header exists in entry and allowed values align
    for key, allowed_values in filters:
        if key not in entry or entry[key] not in allowed_values:
            return False
    return True


def log_to_dict(input_file_path, filters):
    # Parse FortiGate logs entries into dicts and applies user filters

    pattern = re.compile(r'(\w+)=("[^"]*"|\S+)')

    rows = []

    all_keys = set()

    # Construct keys for column headers and row data
    with open(input_file_path, "r") as f:
        for line in f:
            entry = {}
            for match in pattern.finditer(line):
                key = match.group(1)
                val = match.group(2).strip('"')
                entry[key] = val
                all_keys.add(key)
            if filter_check(entry, filters):
                rows.append(entry)


def write_to_csv(rows, all_keys, output_file_path):
    fieldnames = sorted(all_keys)

    # Construct csv
    with open(output_file, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Event log converted to csv. File saved to: {output_file_path}")
    print(f"Total rows: {len(rows)}")


"""
# Sort keys
fieldnames = sorted(all_keys)

# Construct csv
with open(output_file, "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)


# print(f"Event log converted to csv. CSV file saved to: {output_file}")
"""

def main():
    "Run parse fnc. here"


if __name__ == "__main__":
    main()
