import pandas as pd
import pickle
import numpy as np
import os
import sys


#expfolder = "X:\\Chenghang\\04_4_Color\\Exp_Group\\1.2.2021_P2EA_B_V2\\"
expfolder = sys.argv[1]
storm_exp_name = "ML_result_647"
tile_list_file = expfolder + storm_exp_name + "\\ROIs.csv"
if not os.path.exists(expfolder + "tile_sequences\\"):
    os.mkdir(expfolder + "tile_sequences\\")
tile_sequences_directory = expfolder + "tile_sequences\\"


tile_size = 72

df = pd.read_csv(tile_list_file)
cluster_id_frame = df['Cluster_ID']
cluster_id_max = cluster_id_frame.max()
for i in range(0,cluster_id_max):
    df_temp = df[df['Cluster_ID'] == (i+1)]
    tile_seq = df_temp['Tile_ID'].tolist()
    
    seq_file_name = tile_sequences_directory + "sequence_" + str(i+1) + ".data"
    with open(seq_file_name,'wb') as filehandle:
        pickle.dump(tile_seq,filehandle)
    if ((i+1)%100 == 0):
        print("{}th tile sequence is created." .format(i+1))
