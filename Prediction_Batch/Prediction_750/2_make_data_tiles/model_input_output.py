"""
This function collects tiles from makeTiles() and number of localizations per pixel from locsFromTiles() functions.

Swapnil 12/21
"""

from make_tiles import makeTiles


def modelInputOutput(expfolder, tile_size, tiles_df):
    
    tile_input = []
        
    # Read images of teach tile and save them as .data files 
    total_tiles = makeTiles(expfolder, tile_size, tiles_df, tile_input)
    
        
    return total_tiles   
            
            
            
            
            
            
        
        
        

    

