#!/bin/bash

# Function to display help message
show_help() {
  echo "Usage: ./script.sh [OPTIONS]"
  echo
  echo "Options:"
  echo "  -B, --benign       Path to benign variant table from Clinvar."
  echo "  -P, --pathogenic   Path to pathogenic variant table from Clinvar."
  echo "  -O, --output       Name of the output folder."
  echo "  -h, --help         Display this help message."
  echo
}

# Initialize variables
benign=""
pathogenic=""
output=""

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -B|--benign)
      benign="$2"
      shift 2
      ;;
    -P|--pathogenic)
      pathogenic="$2"
      shift 2
      ;;
    -O|--output)
      output="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Validate input
if [[ -z "$benign" || -z "$pathogenic" || -z "$output" ]]; then
  echo "Error: Missing required arguments."
  show_help
  exit 1
fi

# Create folder for run results
mkdir "$output"
cd "$output"

# Subset data into separate directories
python ../scripts/1_subset.py "../$benign" genes_P
python ../scripts/1_subset.py "../$pathogenic" genes_B

# Keep only genes with P/LP and B/LB variants
python ../scripts/2_common.py genes_P genes_B

# Extract missense residues from both sets of variants
python ../scripts/3_rois.py missense_residues_B.json genes_B
python ../scripts/3_rois.py missense_residues_P.json genes_P

# Search for missense residues in interface using PIONEER database
python ../scripts/4_search.py missense_residues_B.json ../data/human.tsv missense_interface_resides_B.json
python ../scripts/4_search.py missense_residues_P.json ../data/human.tsv missense_interface_resides_P.json

# Compile results into final JSON file
python ../scripts/5_shared.py missense_interface_resides_B.json missense_interface_resides_P.json final_proteins.json
