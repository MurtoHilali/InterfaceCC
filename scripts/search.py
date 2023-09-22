import csv
import json
import time
from unipressed import IdMappingClient
import argparse
import re
####################################################################################################
## This script is used to find residues in the interface of a protein-protein interaction that    ##
## are also missense variants in a gene. The input is a TSV file containing protein-protein       ##
## interactions and a JSON file containing missense variants. The output is a JSON file           ##
## containing a dictionary of dictionaries, where each key is a gene name and each value is a     ##
## dictionary of dictionaries, where each key is a partner gene name and each value is a list of  ##
## common residues.                                                                               ##
####################################################################################################

def pc(protein_change):
    # Regular expression to capture number from protein change code
    number_match = re.search(r'\d+', protein_change)
    
    if number_match:
        return int(number_match.group(0))
    return None

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
                    common_residues = [x for x in interface_residues if x in gene_dict[gene_name]['positions']]

                    if common_residues:
                        print(f"\rCommon residues found for {gene_name}! Adding...", end="", flush=True)
                        key = f"{gene_name} ({uniprot_id})"
                        
                        # Create sub-dictionary for the key if it doesn't exist already
                        if key not in result:
                            result[key] = {
                                'protein_change': []
                            }
                        
                        # Determine the partner uniprot ID by swapping uniprot_column
                        partner_uniprot_id = row['uniprot2'] if uniprot_column == 'uniprot1' else row['uniprot1']
                        
                        if partner_uniprot_id not in result[key]:
                            result[key][partner_uniprot_id] = []
                                            
                        # Add common residues with partner_uniprot_id as key
                        result[key][partner_uniprot_id] += common_residues

                        # Add corresponding protein changes to the sub-dictionary
                        protein_changes = list(gene_dict[gene_name]['protein_change'])
                        
                        common_set = set(common_residues)
                        result[key]['protein_change'] = list({change for change in protein_changes if pc(change) in common_set})

                        print(f"Done! {len(common_set)} common residues found for {gene_name}.")


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

    save_results_as_json(result, args.json_output_file)
