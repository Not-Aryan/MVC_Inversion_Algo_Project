#!/usr/bin/env python
# coding: utf-8

# # Compute tractions using the results from the Greenland traction inversion: 
# ## <font color=blue>"compute_Fx_Fy.ipynb"</font>
# #### Jul 25, 2022  <font color=red>(v. testing)</font>
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# 
# 1. Using the equations (1) and (2) in Finzel et al. (2015, GRL), this code computes Basal Tractions

# In[34]:


########Import modules
import numpy as np
import pandas as pd


# In[35]:


input_x1="grad_x_sig_xx_pred.dat"
input_x2="grad_y_sig_xy_cosy_cosy_pred.dat"
input_x3="grad_x_tau_0_pred.dat"

input_y1="grad_x_sig_xy_pred.dat"
input_y2="grad_y_sig_xx_cosy_cosy_pred.dat"
input_y3="grad_y_tau_0_pred.dat"


sample = np.loadtxt(input_x1)
lon=sample[:,0]
lat=sample[:,1]
grad_x_sig_xx = sample[:,2]


sample = np.loadtxt(input_x2)
grad_y_sig_xy_cosy_cosy = sample[:,2]


sample = np.loadtxt(input_x3)
grad_x_tau_0 = sample[:,2]




sample = np.loadtxt(input_y1)
grad_x_sig_xy = sample[:,2]


sample = np.loadtxt(input_y2)
grad_y_sig_xx_cosy_cosy = sample[:,2]


sample = np.loadtxt(input_y3)
grad_y_tau_0 = sample[:,2]


# In[39]:


cosTheta = np.cos(lat*np.pi/180)
cosTheta_sq = np.cos(lat*np.pi/180)**2


# In[46]:


Fx = (-1/cosTheta*grad_x_sig_xx -1/cosTheta_sq*grad_y_sig_xy_cosy_cosy -1/cosTheta*grad_x_tau_0) * -1
Fy = (-1/cosTheta*grad_x_sig_xy +1/cosTheta_sq*grad_y_sig_xx_cosy_cosy - grad_y_tau_0) * -1

pascal_coef = 1/3.15 * 10**(-3) * 8.76

Fx = pascal_coef * Fx
Fy = pascal_coef * Fy


# In[50]:


zero_vector = np.zeros((len(lon),))


# In[9]:


### dictionary for gmt file
dict_tractions_pred = {'lon': lon, 'lat': lat, 'Fx': Fx, 'Fy': Fy, 'stdFx': zero_vector, 'stdFy': zero_vector, 'corr_xy': zero_vector}


### dict to df 
df_tractions_pred = pd.DataFrame(dict_tractions_pred)


### save df
df_tractions_pred.to_csv("Traction.gmt", header=None, index=None, sep=' ')


# In[ ]:




