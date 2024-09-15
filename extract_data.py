import os
import sys
import subprocess
import numpy as np
import glob
import json
import pandas as pd

'''
This script creates a folder "Extracted_data" inside which it extracts all the wav files in the directories date-wise
Modified to work on Windows systems
'''

coswara_data_dir = os.path.abspath('.')  # Local Path of iiscleap/Coswara-Data Repo
extracted_data_dir = os.path.join(coswara_data_dir, 'Extracted_data')  

if not os.path.exists(coswara_data_dir):
    raise Exception("Check the Coswara dataset directory!")

if not os.path.exists(extracted_data_dir):
    os.makedirs(extracted_data_dir)  # Creates the Extracted_data folder if it doesn't exist

dirs_extracted = set(map(os.path.basename, glob.glob(os.path.join(extracted_data_dir, '202*'))))
dirs_all = set(map(os.path.basename, glob.glob(os.path.join(coswara_data_dir, '202*'))))

dirs_to_extract = list(set(dirs_all) - dirs_extracted)

for d in dirs_to_extract:
    source_dir = os.path.join(coswara_data_dir, d)
    tar_files = glob.glob(os.path.join(source_dir, '*.tar.gz*'))
    
    if tar_files:
        # Combine split tar files if necessary
        if len(tar_files) > 1:
            combined_tar = os.path.join(source_dir, 'combined.tar.gz')
            with open(combined_tar, 'wb') as outfile:
                for tar_file in sorted(tar_files):
                    with open(tar_file, 'rb') as infile:
                        outfile.write(infile.read())
        else:
            combined_tar = tar_files[0]
        
        # Extract using Python's tarfile module
        import tarfile
        with tarfile.open(combined_tar, 'r:gz') as tar:
            tar.extractall(path=extracted_data_dir)
        
        # Clean up combined tar if created
        if len(tar_files) > 1:
            os.remove(combined_tar)

print("Extraction process complete!")