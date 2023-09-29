import pickle

inpath = "X:\\Chenghang\\4_Color\\Raw\\12.21.2020_P8EA_B_V2\\model_predictions\\"
infile = inpath + "tile_pred_num_locs_tile_1.data"
with open(infile,'rb') as filehandle:
    locs_data = pickle.load(filehandle)
