"""
Script to get properties clusters predicted by dbscan algorithm on 3d(x,y,z) sequences of localizations.

2/22

Modified to get all subcluster information and subcluster number within each cluster as csv files. 
9/23
"""

import glob
import pickle
import os
import csv

from cluster_properties_class import ClusterProperties

expfolder = "X:\\Chenghang\\04_4_Color\\Exp_Group\\1.2.2021_P2EA_B_V2\\"
storm_exp_name = "ML_result_750"


# Get dbscan parameters.
eps = 20
min_samples = 6

# Set directory for dbscan output of 3d localization sequences.
dbscan_seq_directory = expfolder + "dbscan_output_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\" 

cl_stats_directory = expfolder + "cluster_stats_sequences_eps_" + str(eps) + "_min_smpl_" + str(min_samples) + "\\"
if not os.path.exists(cl_stats_directory):
    os.mkdir(cl_stats_directory)


# Remove previously present files in the folder.
files = glob.glob(cl_stats_directory + "*.data") 
for file in files:
    os.remove(file)


locs_sequences_directory = expfolder + "locs3d_pred_sequences\\"

# Get number of 3d localization sequences present in locs_sequences_directory.
total_seqs = len(glob.glob(locs_sequences_directory + "*.data"))

files = glob.glob(locs_sequences_directory + "*.data")        

# Initialize cluster property value.
clust_sz = 0
clust_ar = 0
clust_vl = 0    

# Initialize cluster property counter.
clust_count = 0 
sub_cluster_count = 0   

fields = ['ID','cluster_id','center_x','center_y','center_z','num_locs','volume','surf_area']
csv_name_handle = expfolder.split('\\')
csv_filename = expfolder + csv_name_handle[-2] + '_subcluster.csv'
with open(filename,'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)

# Iterate over sequences.
    for file in files:
        
        # Get the 3d localization sequence filename.            
        locs_seq_file_name = file

        # Get the sequence number present in the filename.
        seq = int(locs_seq_file_name.split("_")[-1][:-5])             
        
        # Set the DBSCAN result filename for given 3d localization sequence.
        db_out_file_name = dbscan_seq_directory + "dbscan_out_sequence_" + str(seq) + ".data"   

        # Set the filename for cluster stats from given 3d localization sequence.
        cl_stats_file_name = cl_stats_directory + "cluster_stats_sequence_" + str(seq) + ".data"           
        
        # Read from the file. 
        with open(locs_seq_file_name, 'rb') as filehandle:
            locs3d_seq_arr = pickle.load(filehandle)

        # DBSCAN expects first column of array to be x and second column to be y, so swap the two columns of locs3d_seq_arr. 
        if len(locs3d_seq_arr.shape) > 1:
        
            # DBSCAN expects first column of array to be x and second column to be y, so swap the two columns of locs3d_seq_arr. 
            locs3d_seq_arr[:,[0,1]] = locs3d_seq_arr[:,[1,0]]
       
        # Read dbscan output from the file. 
        with open(db_out_file_name, 'rb') as filehandle:
            db = pickle.load(filehandle)

        # Create an empty list for cluster stats.
        sub_cl_num = []

        # Get the cluster properties from dbscan output and add them to cluster stat list.
        # Get the number of clusters predicted.
        num_cl = ClusterProperties(db).numOfClusters()
        sub_cl_num.append(num_cl)
        
        # Get the number of noise points predicted.
        #num_ns = ClusterProperties(db).numOfNoise()
        #cl_stats.append(num_ns)         

        # Get tupple of dictionaries (with unique cluster labels as key) for different cluster stats.
        dicts = ClusterProperties(db).clusterStats(locs3d_seq_arr)

        # Writting the cluster stats list to files for future use (See https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/ for pickle method)
        with open(cl_stats_file_name, 'wb') as filehandle:
            # store the data as binary data stream.
            pickle.dump(cl_stats, filehandle)         
        
        # Get dictionary for cluster centers.
        cl_cntr_dict = dicts[0]  

        # Get dictionary for cluster sizes.
        cl_sz_dict = dicts[1]

        # Get dictionary for cluster areas.
        cl_ar_dict = dicts[2] 

        # Get dictionary for cluster volumes.
        cl_vl_dict = dicts[3]

        for key in cl_sz_dict.keys():
            
            cur_cetr_post = cl_cntr_dict[key]
            cur_csv_row = [str(sub_cluster_count),str(cluster_count),str(cur_cetr_post[0]),str(cur_cetr_post[1]),str(cur_cetr_post[2]),str(cl_sz_dict[key]),str(cl_vl_dict[key]),str(cl_ar_dict[key])]
            csvwriter.writerow(cur_csv_row)
            
            clust_sz += cl_sz_dict[key]
            clust_ar += cl_ar_dict[key]
            clust_vl += cl_vl_dict[key]            
            sub_clust_count += 1
            
        if (seq%100 == 0):
            print("{}th sequence is analyzed." .format(seq))               
            
    clust_sz_avg = clust_sz/sub_clust_count
    clust_ar_avg = clust_ar/sub_clust_count       
    clust_vl_avg = clust_vl/sub_clust_count
    
    cluster_count += 1

    print("average cluster size: {}, average cluster area: {}, average cluster volume: {}" .format(clust_sz_avg, clust_ar_avg, clust_vl_avg))

    



        
        

