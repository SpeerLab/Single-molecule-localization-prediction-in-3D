import os
import glob
import pandas as pd

size_filter = 1
outpath = 'X:\\Chenghang\\4_Color\\Raw\\1.11.2021_B2P8C_B_V2\\'
pathname = outpath + 'cluster_stats_sequences_eps_20_min_smpl_8\\'

print('Num_of_sub')
Num_of_sub = pd.DataFrame()
dir_list = glob.glob(pathname + '*.csv')
Cur_num_of_sub = []
for file in dir_list:
    df = pd.read_csv(file)
    df = df[(df['size']>size_filter)]
    Cur_num_of_sub.append(df.shape[0])
Curnum_series = pd.Series(Cur_num_of_sub)
Curnum_series.name = 'Num_of_sub'
Num_of_sub = pd.concat([Num_of_sub,Curnum_series],axis=1)
Num_of_sub.to_csv(outpath+'Pred_Num_of_sub.csv',index = False)

print('Sub_Size')
Sub_Size = pd.DataFrame()
dir_list = glob.glob(pathname + '*.csv')
Cur_size = pd.DataFrame()
for file in dir_list:
    df = pd.read_csv(file)
    df = df[df['size']>size_filter]
    Cur_size = pd.concat([Cur_size,df['size']],axis=0)
Cur_size = Cur_size.reset_index(drop=True)
Sub_Size = pd.concat([Sub_Size,Cur_size],axis=1)
Sub_Size.to_csv(outpath+'Pred_Sub_size.csv',index = False)

print('Sub_volume')
Sub_volume = pd.DataFrame()
dir_list = glob.glob(pathname + '*.csv')
Cur_volume = pd.DataFrame()
for file in dir_list:
    df = pd.read_csv(file)
    df = df[df['size']>size_filter]
    Cur_volume = pd.concat([Cur_volume,df['volume']],axis=0)
Cur_volume = Cur_volume.reset_index(drop=True)
Sub_volume = pd.concat([Sub_volume,Cur_volume],axis=1)
Sub_volume.to_csv(outpath+'Pred_Sub_volume.csv',index = False)

print('Sub_ClusterID')
Cluster_ID = pd.DataFrame()
dir_list = glob.glob(pathname + '*.csv')
Cur_Cluster_ID = pd.DataFrame()
count = 0
for file in dir_list:
    df = pd.read_csv(file)
    df = df[df['size']>size_filter]
    Cur_Cluster_ID = pd.concat([Cur_Cluster_ID,pd.DataFrame(df.shape[0]*[count])],axis=0)
    count = count + 1
Cur_Cluster_ID = Cur_Cluster_ID.reset_index(drop=True)
Cluster_ID = pd.concat([Cluster_ID,Cur_Cluster_ID],axis=1)
Cluster_ID.to_csv(outpath+'Pred_Cluster_ID.csv',index = False)

print('Sub_X')
Sub_X = pd.DataFrame()
dir_list = glob.glob(pathname + '*.csv')
Cur_X = pd.DataFrame()
for file in dir_list:
    df = pd.read_csv(file)
    df = df[df['size']>size_filter]
    Cur_X = pd.concat([Cur_X,df['center x']],axis=0)
Cur_X = Cur_X.reset_index(drop=True)
Sub_X = pd.concat([Sub_X,Cur_X],axis=1)
Sub_X.to_csv(outpath+'Pred_Sub_X.csv',index = False)

print('Sub_Y')
Sub_Y = pd.DataFrame()
dir_list = glob.glob(pathname + '*.csv')
Cur_Y = pd.DataFrame()
for file in dir_list:
    df = pd.read_csv(file)
    df = df[df['size']>size_filter]
    Cur_Y = pd.concat([Cur_Y,df['center y']],axis=0)
Cur_Y = Cur_Y.reset_index(drop=True)
Sub_Y = pd.concat([Sub_Y,Cur_Y],axis=1)
Sub_Y.to_csv(outpath+'Pred_Sub_Y.csv',index = False)

print('Sub_Z')
Sub_Z = pd.DataFrame()
dir_list = glob.glob(pathname + '*.csv')
Cur_Z = pd.DataFrame()
for file in dir_list:
    df = pd.read_csv(file)
    df = df[df['size']>size_filter]
    Cur_Z = pd.concat([Cur_Z,df['center z']],axis=0)
Cur_Z = Cur_Z.reset_index(drop=True)
Sub_Z = pd.concat([Sub_Z,Cur_Z],axis=1)
Sub_Z.to_csv(outpath+'Pred_Sub_Z.csv',index = False)

