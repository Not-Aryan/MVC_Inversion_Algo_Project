#!/usr/bin/env python
# coding: utf-8

# # Compute tractions using the results from the Greenland traction inversion: 
# ## <font color=blue>"compute_predicted_strain_rates.ipynb"</font>
# #### Jul 25, 2022  <font color=red>(v. testing)</font>
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# 
# 1. A G-matrix will be built using "strain" basis functions. 
# 2. And then the model coefficients will be multiplied to the G-matrix to obtain **${e}_{ij}^{obs}$**.
# 3. Using the **${e}_{ij}^{obs}$** and the equations in Finzel et al. (2015, GRL), this code computes sigma xx, sigma xy, tau_0. #greek

# In[2]:


########Import modules
import numpy as np
import pandas as pd
import sys

import warnings
warnings.filterwarnings('ignore')


# In[3]:


inversion_results = sys.argv[1]
inversion_results = str(inversion_results)


#inversion_results = "model_coef_Ridge_1.0481131341546852.out"


# In[4]:


np_model_coefs = np.loadtxt(inversion_results)

######## How Many Basis Functions 
HowManyBasisFunctions=np.loadtxt("geometry_info.txt", skiprows=1)
HowManyCell=int(HowManyBasisFunctions[1])

# Output files
exx_pred = "exx_pred.xyz"
eyy_pred = "eyy_pred.xyz"
exy_pred = "exy_pred.xyz"

pred1 = "sig_xx_pred.xyz"
pred2 = "tau_0_pred.xyz"
pred3 = "sig_xy_cosy_cosy_pred.xyz"
pred4 = "sig_xy_pred.xyz"
pred5 = "sig_xx_cosy_cosy_pred.xyz"


# # `STEP 1:` **BUILD G-Matrix (strain rates), $\bar{\bar{G}}$**

# In[5]:


input_sample = "./FILES_basis_functions/average_strain_RECTANGULAR_1_1.out"
sample = np.loadtxt(input_sample)
data_length=len(sample)


# In[6]:


lon=sample[:,2]
lat=sample[:,1]


# In[7]:


df_G_exx_resp = pd.DataFrame(index = range(data_length))
df_G_eyy_resp = pd.DataFrame(index = range(data_length)) 
df_G_exy_resp = pd.DataFrame(index = range(data_length)) 


names = ['cell_num','lat','lon','exx_resp','eyy_resp','exy_resp','std_exx_resp','std_eyy_resp','std_exy_resp']
# Make a blank G matrix part related to Boundary Condition on data points

for i in range(1,HowManyCell+1): 
    
    inputfile_exx = "./FILES_basis_functions/average_strain_RECTANGULAR_"+str(i)+"_1"+".out" 
    #exx responses
    inputfile_eyy = "./FILES_basis_functions/average_strain_RECTANGULAR_"+str(i)+"_2"+".out" 
    #eyy responses
    inputfile_exy = "./FILES_basis_functions/average_strain_RECTANGULAR_"+str(i)+"_3"+".out" 
    #exy responses 


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


       
    df_G_exx_resp["G_exx_resp_from_exx_"+str(i)] = df_exx.loc[:,['exx_resp']]
    df_G_exx_resp["G_exx_resp_from_eyy_"+str(i)] = df_eyy.loc[:,['exx_resp']]
    df_G_exx_resp["G_exx_resp_from_exy_"+str(i)] = df_exy.loc[:,['exx_resp']]
    
    df_G_eyy_resp["G_eyy_resp_from_exx_"+str(i)] = df_exx.loc[:,['eyy_resp']]
    df_G_eyy_resp["G_eyy_resp_from_eyy_"+str(i)] = df_eyy.loc[:,['eyy_resp']]
    df_G_eyy_resp["G_eyy_resp_from_exy_"+str(i)] = df_exy.loc[:,['eyy_resp']]
    
    df_G_exy_resp["G_exy_resp_from_exx_"+str(i)] = df_exx.loc[:,['exy_resp']]
    df_G_exy_resp["G_exy_resp_from_eyy_"+str(i)] = df_eyy.loc[:,['exy_resp']]
    df_G_exy_resp["G_exy_resp_from_exy_"+str(i)] = df_exy.loc[:,['exy_resp']]


# In[8]:




# <div class="alert alert-success">
#     <b> These are strain rate basis functions ! </b>
# </div>
# 
# <div class="alert alert-success">
#     <b> strain rate basis functions @ model coefficients = predicted strain </b>
# </div>

# In[9]:


### df G to np G
np_G_exx_resp=df_G_exx_resp.to_numpy()
np_G_eyy_resp=df_G_eyy_resp.to_numpy()
np_G_exy_resp=df_G_exy_resp.to_numpy()

### G*m (prediction for strain)
np_exx_pred = np_G_exx_resp @ np_model_coefs
np_eyy_pred = np_G_eyy_resp @ np_model_coefs
np_exy_pred = np_G_exy_resp @ np_model_coefs

np_sig_xy = np_exy_pred
np_sig_xx = 1/2*(np_exx_pred - np_eyy_pred)
np_tau_0 = 3/2*(np_exx_pred + np_eyy_pred)


np_sig_xy_cosycosy = np_sig_xy*(np.cos(lat*np.pi/180)**2)
np_sig_xx_cosycosy = np_sig_xx*(np.cos(lat*np.pi/180)**2)

### dictionary for  xyz files
dict_exx_pred = {'lon': lon, 'lat': lat, 'exx': np_exx_pred}
dict_eyy_pred = {'lon': lon, 'lat': lat, 'eyy': np_eyy_pred}
dict_exy_pred = {'lon': lon, 'lat': lat, 'exy': np_exy_pred}


dict_sig_xx_pred = {'lon': lon, 'lat': lat, 'sigxx': np_sig_xx}
dict_tau_0_pred = {'lon': lon, 'lat': lat, 'tau0': np_tau_0}
dict_sig_xy_cosycosy_pred = {'lon': lon, 'lat': lat, 'sigxy_cosy_cosy': np_sig_xy_cosycosy}
dict_sig_xy_pred = {'lon': lon, 'lat': lat, 'sigxy': np_sig_xy}
dict_sig_xx_cosycosy_pred = {'lon': lon, 'lat': lat, 'sigxx_cosy_cosy': np_sig_xx_cosycosy}


### dict to df 
df_exx_pred = pd.DataFrame(dict_exx_pred)
df_eyy_pred = pd.DataFrame(dict_eyy_pred)
df_exy_pred = pd.DataFrame(dict_exy_pred)


df_sig_xx_pred = pd.DataFrame(dict_sig_xx_pred)
df_tau_0_pred = pd.DataFrame(dict_tau_0_pred)
df_sig_xy_cosycosy_pred = pd.DataFrame(dict_sig_xy_cosycosy_pred)
df_sig_xy_pred = pd.DataFrame(dict_sig_xy_pred)
df_sig_xx_cosycosy_pred = pd.DataFrame(dict_sig_xx_cosycosy_pred)



### save df

df_exx_pred.to_csv(exx_pred,header=None, index=None, sep=' ')
df_eyy_pred.to_csv(eyy_pred,header=None, index=None, sep=' ')
df_exy_pred.to_csv(exy_pred,header=None, index=None, sep=' ')


df_sig_xx_pred.to_csv(pred1,header=None, index=None, sep=' ')
df_tau_0_pred.to_csv(pred2,header=None, index=None, sep=' ')
df_sig_xy_cosycosy_pred.to_csv(pred3,header=None, index=None, sep=' ')
df_sig_xy_pred.to_csv(pred4,header=None, index=None, sep=' ')
df_sig_xx_cosycosy_pred.to_csv(pred5,header=None, index=None, sep=' ')


# In[ ]:




