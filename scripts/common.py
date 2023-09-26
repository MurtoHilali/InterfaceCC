import os
import argparse

####################################################################################################
## This script is used to remove files from two folders that don't have a shared basename. Shared ##
## basenames tell us that genes in question have both benign and pathogenic variants.             ##
####################################################################################################

def get_basenames_from_folder(folder_path):
    """Returns the set of basenames from all files in the folder."""
    return {os.path.splitext(filename)[0] for filename in os.listdir(folder_path)}

def remove_unshared_files(folder_path, shared_basenames):
    """Removes all files in the folder that don't have a basename in shared_basenames."""
    for filename in os.listdir(folder_path):
        basename = os.path.splitext(filename)[0]
        if basename not in shared_basenames:
            file_path = os.path.join(folder_path, filename)
            print(f"\rRemoving {file_path}", end="", flush=True)
            os.remove(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder1", help="path to the first folder")
    parser.add_argument("folder2", help="path to the second folder")
    args = parser.parse_args()

    # Get sets of basenames for each folder
    basenames1 = get_basenames_from_folder(args.folder1)
    basenames2 = get_basenames_from_folder(args.folder2)

    # Identify shared basenames
    shared_basenames = basenames1.intersection(basenames2)

    # Remove unshared files from each folder
    remove_unshared_files(args.folder1, shared_basenames)
    print("\n")
    remove_unshared_files(args.folder2, shared_basenames)
    print("\n")