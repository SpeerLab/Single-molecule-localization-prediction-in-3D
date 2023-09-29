"""
This function collects tiles from makeTiles() and number of localizations per pixel from locsFromTiles() functions.

Swapnil 12/21
"""

from locs_from_tiles import locsFromTiles

def modelInputOutput(expfolder, tile_size, max_processes, tiles_df, locsPerTile2, clust_pix_list_full_file):
    
    num_locs_output = []      
    
    # Make localization files for individual tiles.             
    total_loc_files = locsFromTiles(expfolder, tile_size, num_locs_output, max_processes, tiles_df, locsPerTile2, clust_pix_list_full_file)                   
        
    return total_loc_files
    # return total_tiles        
    
            
            
            
            
            
            
        
        
        

    

