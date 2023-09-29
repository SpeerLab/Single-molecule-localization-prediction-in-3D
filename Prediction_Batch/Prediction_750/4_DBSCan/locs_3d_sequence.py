"""
Script to create sequences of 3d localizations. The sequences of localizations are created from 
sequences of overlapping tiles previously found using tile_sequence.py     

Swapnil 1/22
"""

import glob
import pickle
import os
import sys

from tile_sequencer_class import TileSequencer

# Set path to data files.
# expfolder = "X:\\Chenghang\\04_4_Color\\Exp_Group\\1.4.2021_P2EB_B_V2\\"
expfolder = sys.argv[1]

storm_exp_name = "ML_Result_750"

storm_exp_directory = expfolder + storm_exp_name + "\\"

# Get 3d localizations directory.
locs_3d_directory = expfolder + "locs3d_predictions\\"
          
# tile_sequences_directory = storm_exp_directory + "tile_sequences\\"
tile_sequences_directory = expfolder + "tile_sequences\\"

# Create new directory for 3d localization sequence.
if not os.path.exists(expfolder + "locs3d_pred_sequences\\"):
    os.mkdir(expfolder + "locs3d_pred_sequences\\")

# Set localizations sequences directory.
locs_sequences_directory = expfolder + "locs3d_pred_sequences\\"     

# Remove previously present files. 
files = glob.glob(locs_sequences_directory + "*.data")
for f in files:
    os.remove(f)

# Get number of sequences present in tile_sequences_directory.
total_seqs = len(glob.glob(tile_sequences_directory + "*.data"))

for i in range(1, total_seqs+1):
    mol_list = False
    # Get the tile sequence filename.
    seq_file_name = tile_sequences_directory + "sequence_" + str(i) + ".data"


    locs_seq_file_name = locs_sequences_directory + "locs3d_pred_sequence_" + str(i) + ".data"    
        
    
    # Read from the file. 
    with open(seq_file_name, 'rb') as filehandle:
        tile_num_seq = pickle.load(filehandle)
                
    # locs_3d_seq = TileSequencer(tiles_df).locs3dSequence(tile_num_seq, locs_3d_directory)
    locs_3d_seq = TileSequencer().locs3dSequence(tile_num_seq, locs_3d_directory, mol_list)
    
    if (i%100 == 0):
        print("{}th locs_3d sequence is created." .format(i))       

    # Writing sequences to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
    with open(locs_seq_file_name, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(locs_3d_seq, filehandle)        
        
    

    










