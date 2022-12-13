#!/usr/bin/env python
# coding: utf-8

# Import modules
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')


# How Many grid cells
HowManyBasisFunctions=np.loadtxt("geometry_info.txt", skiprows=1)
HowManyCell=int(HowManyBasisFunctions[1])

# Output files
outputFILE_G_matrix="G_matrix.out" 


input_sample = "./FILES_basis_functions/vel_horizontal_basis_functions_1_1.gmt"
sample = np.loadtxt(input_sample)
data_length=len(sample)*2

# Make a blank G matrix part related to Boundary Condition on data points
df_G = pd.DataFrame(index = range(data_length)) 
names = ['lon','lat','ve','vn','se','sn','corr']

for i in range(1,HowManyCell+1): 
    
    inputfile_exx = "./FILES_basis_functions/vel_horizontal_basis_functions_"+str(i)+"_1"+".gmt" 
    #exx horizontal
    inputfile_eyy = "./FILES_basis_functions/vel_horizontal_basis_functions_"+str(i)+"_2"+".gmt" 
    #eyy horizontal
    inputfile_exy = "./FILES_basis_functions/vel_horizontal_basis_functions_"+str(i)+"_3"+".gmt" 
    #exy horizontal 


    df_exx=pd.read_csv(inputfile_exx, header=None, sep=r'(?:,|\s+)', 
                           comment='#', engine='python')
    df_eyy=pd.read_csv(inputfile_eyy, header=None, sep=r'(?:,|\s+)', 
                           comment='#', engine='python')
    df_exy=pd.read_csv(inputfile_exy, header=None, sep=r'(?:,|\s+)', 
                           comment='#', engine='python')   

# CHANGE the column names 

    df_exx.columns = names
    df_eyy.columns = names
    df_exy.columns = names

    
    
    
# BUILD a column vector Gexx (i)

    df_exx_x = df_exx.iloc[:,[0,1,2]]  # saved vx basis function on the data points
    df_exx_y = df_exx.iloc[:,[0,1,3]]  # saved vn basis function on the data points

    df_exx_x=df_exx_x.rename(columns ={'ve': 'velo'}) #column name change
    df_exx_y=df_exx_y.rename(columns ={'vn': 'velo'}) #column name change
    
    # !! SORT VALUES !! # lat (ascending) first, and then lon (ascending).
    df_exx_x=df_exx_x.sort_values(['lat', 'lon'], ascending=[True, True])
    df_exx_y=df_exx_y.sort_values(['lat', 'lon'], ascending=[True, True])
    
    # MERGE two columns (n*1) into a new column (2n*1)
    # > ignore_index = True : 
    # >   have one continuous index numbers,
    # >     ignorning each of the two dfs original indices   
    frames_Gexx=[df_exx_x,df_exx_y]
    df_Gexx=pd.concat(frames_Gexx,ignore_index=True) # merge the two dataFrames into one

    
    
    
# BUILD a column vector Geyy (i)

    df_eyy_x = df_eyy.iloc[:,[0,1,2]]  # saved vx basis function on the data points
    df_eyy_y = df_eyy.iloc[:,[0,1,3]]  # saved vn basis function on the data points

    df_eyy_x=df_eyy_x.rename(columns ={'ve': 'velo'}) #column name change
    df_eyy_y=df_eyy_y.rename(columns ={'vn': 'velo'}) #column name change

    # !! SORT VALUES !! # lat (ascending) first, and then lon (ascending).
    df_eyy_x=df_eyy_x.sort_values(['lat', 'lon'], ascending=[True, True])
    df_eyy_y=df_eyy_y.sort_values(['lat', 'lon'], ascending=[True, True])
    
    # MERGE two columns (n*1) into a new column (2n*1)
    # > ignore_index = True : 
    # >   have one continuous index numbers,
    # >     ignorning each of the two dfs original indices
    frames_Geyy=[df_eyy_x,df_eyy_y]
    df_Geyy=pd.concat(frames_Geyy,ignore_index=True) # merge the two dataFrames into one
    
    
    
    
# BUILD a column vector Gexy (i)

    df_exy_x = df_exy.iloc[:,[0,1,2]]  # saved vx basis function on the data points
    df_exy_y = df_exy.iloc[:,[0,1,3]]  # saved vn basis function on the data points

    df_exy_x=df_exy_x.rename(columns ={'ve': 'velo'}) #column name change
    df_exy_y=df_exy_y.rename(columns ={'vn': 'velo'}) #column name change

   
    # !! SORT VALUES !! # lat (ascending) first, and then lon (ascending).
    df_exy_x=df_exy_x.sort_values(['lat', 'lon'], ascending=[True, True])
    df_exy_y=df_exy_y.sort_values(['lat', 'lon'], ascending=[True, True])
    
    # MERGE two columns (n*1) into a new column (2n*1)
    # > ignore_index = True : 
    # >   have one continuous index numbers,
    # >     ignorning each of the two dfs original indices
    frames_Gexy=[df_exy_x,df_exy_y]
    df_Gexy=pd.concat(frames_Gexy,ignore_index=True) # merge the two dataFrames into one



# SAVE a part of G-matrix (as in two different structures and then they will be merged later)

    # 1st structure = [Gexx(1) Geyy(1) Gexy(1) ... Gexx(HowManyCell) Geyy(HowManyCell) Gexy(HowManyCell)]   
    df_G["G_exx"+str(i)] = df_Gexx.loc[:,['velo']]
    df_G["G_eyy"+str(i)] = df_Geyy.loc[:,['velo']]
    df_G["G_exy"+str(i)] = df_Gexy.loc[:,['velo']]


print("DONE")


df_data = pd.read_csv("vel_obs_m_per_hr.gmt", header=None, sep=r'(?:,|\s+)', 
                           comment='#', engine='python')


if len(df_data)*2!=df_G.shape[0]:
    print("WARNING: Something went wrong!")
if HowManyCell*3!=df_G.shape[1]:
    print("WARNING: Something went wrong!")


# SAVE G-matrix for the inversion
df_G.to_csv(outputFILE_G_matrix, index=None, float_format='%g')


df_G

