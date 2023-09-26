#!/bin/bash

# Function to display help message
show_help() {
  echo "Usage: ./vicc.sh [OPTIONS]"
  echo
  echo "Options:"
  echo "  -B, --benign       Path to benign variant table from Clinvar."
  echo "  -P, --pathogenic   Path to pathogenic variant table from Clinvar."
  echo "  -O, --output       Name of the output folder."
  echo "  -s, --stringent    Run stringent sections of the script."
  echo "  -h, --help         Display this help message."
  echo
}

# Initialize variables
benign=""
pathogenic=""
output=""
stringent=false

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
    -s|--stringent)
      stringent=true
      shift
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
python ../scripts/subset.py "../$pathogenic" genes_P
python ../scripts/subset.py "../$benign" genes_B

# If stringent flag is set, run the following sections
if $stringent; then
  # Keep only genes with P/LP and B/LB variants
  python ../scripts/common.py genes_P genes_B
fi

# Extract missense residues from both sets of variants
python ../scripts/rois.py missense_residues_B.json genes_B
python ../scripts/rois.py missense_residues_P.json genes_P

# Search for missense residues in interface using PIONEER database
python ../scripts/search.py missense_residues_B.json ../scripts/data/human-high.tsv missense_interface_residues_B.json
python ../scripts/search.py missense_residues_P.json ../scripts/data/human-high.tsv missense_interface_residues_P.json

# If stringent flag is set, run the following sections
if $stringent; then
  # Compile results into final JSON file
  python ../scripts/shared.py missense_interface_residues_B.json missense_interface_residues_P.json final_proteins.json
fi

mv ../$benign ../$pathogenic .
