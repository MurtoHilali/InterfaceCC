import csv
import os
from collections import defaultdict
import argparse

####################################################################################################
## This script is used to subset a TSV file by the values in its second column, which is assumed ##
## to be a gene name. The output is a directory of TSV files, each corresponding to a gene name. ##
####################################################################################################

# Function to read TSV and subset it
def subset_tsv(input_tsv_path):
    # Dictionary to hold rows by second column values
    subsets = defaultdict(list)

    # Reading the TSV file
    with open(input_tsv_path, 'r', newline='') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        
        # Read the header row
        header = next(reader)
        
        # Read each row and add it to the corresponding subset
        for row in reader:
            key = row[1]
            subsets[key].append(row)

    return header, subsets

# Function to write the subset TSVs
def write_subsets(header, subsets, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for key, rows in subsets.items():
        # Creating a safe filename
        safe_key = "".join([c if c.isalnum() else "_" for c in key])
        
        # Naming the new TSV according to the key
        output_tsv_path = os.path.join(output_directory, f"{safe_key}.tsv")
        
        # Writing the subset TSV
        with open(output_tsv_path, 'w', newline='') as tsv_file:
            writer = csv.writer(tsv_file, delimiter='\t')
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)

# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_tsv_path", help="path to input TSV file")
    parser.add_argument("output_directory", help="directory where subset TSVs will be saved")
    args = parser.parse_args()

    header, subsets = subset_tsv(args.input_tsv_path)
    write_subsets(header, subsets, args.output_directory)
