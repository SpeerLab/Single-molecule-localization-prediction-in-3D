import math
import pandas as pd
import os
import glob
import pickle
import random
import numpy as np

def make_data_per_image(img_df,clstr_pix_list_full_df,locs_dict_file_name,num_locs_directory,sema):
    # Read from the file and save it to a dictionary.
    print("Reading localizations dictionary from file ...\n")
    
    with open(locs_dict_file_name, 'rb') as filehandle:
        locs_storm = pickle.load(filehandle)

    # Iterate over all rows in dataframe for given image number.
    for idx in img_df.index:
        print('processing ' + str(idx) + 'th image')
        # Get the tile coordinates.
        tile_start_pix_y = math.floor(img_df.loc[idx, 'y(row)'])
        tile_start_pix_x = math.floor(img_df.loc[idx, 'x(column)'])
        tile_id = math.floor(img_df.loc[idx, 'Tile_ID'])            
        
        # Form a key from tile coordinates for given tile.
        key  =  "locs_"+str(tile_start_pix_y)+"_"+str(tile_start_pix_x)
        
        # From the localizations dictionary get list of localizations for given key.
        locs_storm_tile = locs_storm[key]
        z_pos = img_df.loc[idx, 'z(Num_image)']
        # From the full pix list, clean the background. 
        cur_pix_list = clstr_pix_list_full_df[clstr_pix_list_full_df["TileID"]==(idx+1)]
        cur_pix_list = cur_pix_list['row_col_tup'].tolist()
        
        fl_pt = 3
        z_pix_size = 70
        xy_pix_size = 15.5
        locs_storm_tile_3d = np.array([])

        for each_pos in locs_storm_tile:
            cur_tup = (np.floor(each_pos[0]-tile_start_pix_y),np.floor(each_pos[1]-tile_start_pix_x))
            if cur_tup in cur_pix_list:
        
                each_pos[0] = each_pos[0] * xy_pix_size
                each_pos[1] = each_pos[1] * xy_pix_size
                z_given = z_pix_size * random.randint((z_pos-1)*10**fl_pt,(z_pos)*10**fl_pt)/10**fl_pt
                locs_storm_tile_3d_cur = np.append(each_pos,z_given)
                cur_size = locs_storm_tile_3d.shape
                if cur_size[0] == 0:
                    locs_storm_tile_3d = locs_storm_tile_3d_cur
                else:
                    locs_storm_tile_3d = np.row_stack((locs_storm_tile_3d,locs_storm_tile_3d_cur))
        
        with open(num_locs_directory + str(tile_id) + '.data', 'wb') as filehandle:
            pickle.dump(locs_storm_tile_3d, filehandle)
        sema.release()   