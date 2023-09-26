import json
import os
import argparse

#####################################################################################################
## This script is used to find the shared keys between two JSON files and write them to a new JSON ##
## file. For control purposes, it tells you which proteins have both P/LP & B/LP variant residues  ##
## in their interfaces, and which proteins those interfaces are with.                              ##
#####################################################################################################

def read_json(json_file_path):
    """Reads a JSON file and returns its content as a Python dictionary."""
    with open(json_file_path, 'r') as f:
        return json.load(f)

def write_json(data, json_file_path):
    """Writes a Python dictionary to a JSON file."""
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_basename_without_extension(file_path):
    """Returns the basename of a file without its extension."""
    return os.path.splitext(os.path.basename(file_path))[0]

def main(json_file1_path, json_file2_path, output_file_path):
    # Read the content of each JSON file into a Python dictionary
    json_data1 = read_json(json_file1_path)
    json_data2 = read_json(json_file2_path)

    # Get the basename without extension for each JSON file
    basename1 = get_basename_without_extension(json_file1_path)
    basename2 = get_basename_without_extension(json_file2_path)

    # Find the keys shared between the two JSON files
    shared_keys = set(json_data1.keys()).intersection(set(json_data2.keys()))

    # Create a new dictionary to store the shared keys and their corresponding values
    shared_data = {}
    if len(shared_keys) == 0:
        print("No shared keys :(")
        exit()

    for key in shared_keys:
        shared_data[key] = {
            basename1: json_data1[key],
            basename2: json_data2[key]
        }

    # Write the shared data to the output JSON file
    write_json(shared_data, output_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file1_path", help="path to the first input JSON file")
    parser.add_argument("json_file2_path", help="path to the second input JSON file")
    parser.add_argument("output_file_path", help="path to the output JSON file")
    args = parser.parse_args()

    main(args.json_file1_path, args.json_file2_path, args.output_file_path)
