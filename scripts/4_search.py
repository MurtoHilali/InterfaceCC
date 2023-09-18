import csv
import json
import time
from unipressed import IdMappingClient
import argparse

####################################################################################################
## This script is used to find residues in the interface of a protein-protein interaction that    ##
## are also missense variants in a gene. The input is a TSV file containing protein-protein       ##
## interactions and a JSON file containing missense variants. The output is a JSON file           ##
## containing a dictionary of dictionaries, where each key is a gene name and each value is a     ##
## dictionary of dictionaries, where each key is a partner gene name and each value is a list of  ##
## common residues.                                                                               ##
####################################################################################################

def read_json_and_map_ids(json_file):
    with open(json_file, 'r') as f:
        gene_dict = json.load(f)

    id_to_gene_map = {}
    request = IdMappingClient.submit(
        source="GeneCards",
        dest="UniProtKB",
        ids=set(gene_dict.keys())
    )

    time.sleep(1.0)
    results = list(request.each_result())
    for result in results:
        if result:
            uniprot_id = result['to']
            gene_name = result['from']
            id_to_gene_map[uniprot_id] = gene_name

    return gene_dict, id_to_gene_map


def process_tsv(tsv_file, gene_dict, id_to_gene_map):
    result = {}

    with open(tsv_file, 'r', newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')

        for row in reader:
            for uniprot_column, interface_column in [('uniprot1', 'interface_residues1'), ('uniprot2', 'interface_residues2')]:
                uniprot_id = row[uniprot_column]
                interface_residues = json.loads(row[interface_column].replace("'", '"'))

                if uniprot_id in id_to_gene_map:
                    gene_name = id_to_gene_map[uniprot_id]
                    common_residues = [x for x in interface_residues if x in gene_dict[gene_name]]

                    if common_residues:
                        print(f"\rCommon residues found for {gene_name}! Adding...", end="", flush=True)
                        key = f"{gene_name} ({uniprot_id})"
                        
                        # Create sub-dictionary with 'interactions' key if it doesn't exist already
                        if key not in result:
                            result[key] = {}

                        # Determine the partner uniprot ID by swapping uniprot_column
                        partner_uniprot_id = row['uniprot2'] if uniprot_column == 'uniprot1' else row['uniprot1']
                        
                        # Add common residues with partner_uniprot_id as key
                        result[key][partner_uniprot_id] = common_residues

    return result

def save_results_as_json(result, json_file):
    with open(json_file, 'w') as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_input_file", help="path to the input JSON file")
    parser.add_argument("tsv_input_file", help="path to the input TSV file")
    parser.add_argument("json_output_file", help="path to the output JSON file")
    args = parser.parse_args()

    gene_dict, id_to_gene_map = read_json_and_map_ids(args.json_input_file)
    result = process_tsv(args.tsv_input_file, gene_dict, id_to_gene_map)
    print("\n")
    save_results_as_json(result, args.json_output_file)
