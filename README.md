# variCC
The shell script helps you find known variant missense residues (P/LP and B/LB) that occur at protein-protein interfaces for use as *in silico* controls. It currently accepts search output data from ClinVar as inputs and returns JSON information filtered out from PIONEER.

## Subscripts

All subscripts can be accessed independently and used from the command line as separate utilities:

```bash
python {script}.py <arg1> <arg2> ...
```
## Requirements
- Python 3.x
- Unipressed ([`pip install unipressed`](https://pypi.org/project/unipressed/))
- Human interactome data from [PIONEER](https://pioneer.yulab.org/downloads), as TSV. (You can use `data.sh` to download this for you.)

## Usage

To execute the script, open your terminal and navigate to the folder containing the script. Then run:

```bash
./run.sh \
-B [path/to/benign/variant/table] \
-P [path/to/pathogenic/variant/table] \
-O [output_folder_name]
```

For example, if you have benign variant data in a file named `benign_data.tsv`, pathogenic variant data in `pathogenic_data.tsv`, and you want to output to a folder named `results`, run:

```bash
./run.sh -B benign_data.tsv -P pathogenic_data.tsv -O results
```

### Command-line Options

The script accepts the following command-line options:

- `-B, --benign`: Specifies the path to the benign variant table from Clinvar. This is a required argument.

- `-P, --pathogenic`: Specifies the path to the pathogenic variant table from Clinvar. This is a required argument.

- `-O, --output`: Specifies the name of the output folder where the results will be saved. This is a required argument.

- `-h, --help`: Displays a help message detailing how to use the script and what each option does.

#### Examples

To run the script with specific benign and pathogenic variant tables and an output folder named `analysis_output`:

```bash
./run.sh -B benign_variants.tsv -P pathogenic_variants.tsv -O analysis_output
```

To display the help menu:

```bash
./run.sh -h
```

## Output
- Missense residues JSONs (for both TSVs).
- Missense residues appearing at interfaces for both JSONs.
- A combined JSON including data from both P/LP and B/LB interface residue JSONs.
- Directories containing TSVs subset from input tables, based on gene name.

All output files will be saved in the specified `output_folder`.

## Workflow Steps

1. `1_subset.py`: This script is used to subset a TSV file by the values in its second column, which is assumed to be a gene name. The output is a directory of TSV files, each corresponding to a gene name. 
2. `2_common.py`: This script is used to remove files from two folders that don't have a shared basename. Shared basenames tell us that genes in question have both benign and pathogenic variants.
3. `3_rois.py`: The residues of interest script is used to extract numbers from protein change codes in TSV files. The output is a JSON file containing a dictionary of lists, where each key is the basename of a TSV file and each value is a missense residue position. We'll search against these numbers to see if they appear in an interface.
4. `4_search.py`: Find residues in the interface of a protein-protein interaction that are also missense variants in a gene. The output is a JSON file containing a dictionary of dictionaries, where each key is a gene name and each value is a dictionary of dictionaries, where each key is a partner gene name and each value is a list of common residues.
5. `5_shared.py`: Finds the shared keys between two JSON files and write them to a new JSON file. For control purposes, it tells you which proteins have both P/LP & B/LP variant residues in their interfaces, and which proteins those interfaces are with.       

## TODO
- Implement more detailed error reporting and logging.
- Add support for variant data from gnomAD.

