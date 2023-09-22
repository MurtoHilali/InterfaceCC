import os
import csv
import json
import re
import argparse

####################################################################################################
## This script is used to extract numbers from protein change codes in TSV files. The output is a ##
## JSON file containing a dictionary of lists, where each key is the basename of a TSV file and   ##
## each value is a missense residue position. We'll search against these numbers to see if they    ##
## appear in an interface.                                                                        ##
####################################################################################################


def extract_number_from_protein_change(protein_change):
    # Regular expression to capture number from protein change code
    number_match = re.search(r'\d+', protein_change)
    
    if number_match:
        return int(number_match.group(0))
    return None

def process_tsv_files(directory, output_json):
    output_dict = {}
    
    # Loop through each TSV file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.tsv'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', newline='') as tsv_file:
                reader = csv.reader(tsv_file, delimiter='\t')
                
                # Skip header
                next(reader)
                
                # Lists to hold values from column 3
                numbers_list = []
                protein_change_list = []

                # Read rows and collect numbers
                for row in reader:
                    protein_changes = row[2].split(', ')
                    for change in protein_changes:
                        protein_change_list.append(change)
                        number = extract_number_from_protein_change(change)
                        if number is not None:
                            numbers_list.append(number)
                        
                
                # Add to the output dictionary
                basename = os.path.splitext(filename)[0]
                numbers_list = sorted(list(set(numbers_list)))
                output_dict[basename] = {
                    'protein_change': protein_change_list, 
                    'positions': numbers_list
                }
    
    # Output the dictionary as a JSON file
    with open(output_json, 'w') as json_file:
        json.dump(output_dict, json_file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_json", help="name of the output JSON file")
    parser.add_argument("input_directory", help="path to the input directory")
    args = parser.parse_args()

    process_tsv_files(args.input_directory, args.output_json)
