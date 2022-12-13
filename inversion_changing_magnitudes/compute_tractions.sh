#!/bin/bash


### STEP 1 . Compute the predicted 3 components of horizontal strain rates.

#use the python notebook
# python compute_predicted_strain_rates.py "Inversion_results_new_magnitudes\model_coef_Ridge_0.1519911082952933__0.95.out"

# sig_xx_pred.xyz
# tau_0_pred.xyz
# sig_xy_cosy_cosy_pred.xyz
# sig_xy_pred.xyz
# sig_xx_cosy_cosy_pred.xyz

### STEP 2. Take the gradients of the sigma_xx, tau_0, sigma_xy*cos(lat)^2, sigma_xy, sigma_xx*cos(lat)^2

I="-I120m" #120 m = 2 deg
R="-R-85/-15/45/85"

### STEP 2-1 sig xx
input="sig_xx_pred"
# xyx to grd format
gmt surface "$input".xyz -Graw.grd $I $R  
# gradient in x direction
gmt grdgradient raw.grd -A90 -Ggrad_x.grd
gmt grd2xyz grad_x.grd > grad_x.dat
# gradient in y direction
gmt grdgradient raw.grd -A0 -Ggrad_y.grd
gmt grd2xyz grad_y.grd > grad_y.dat
cp grad_x.dat grad_x_"$input".dat
cp grad_y.dat grad_y_"$input".dat
rm raw.grd grad_x.grd grad_x.dat grad_y.grd grad_y.dat


### STEP 2-2 tau 0
input="tau_0_pred"
# xyx to grd format
gmt surface "$input".xyz -Graw.grd $I $R
# gradient in x direction
gmt grdgradient raw.grd -A90 -Ggrad_x.grd
gmt grd2xyz grad_x.grd > grad_x.dat
# gradient in y direction
gmt grdgradient raw.grd -A0 -Ggrad_y.grd
gmt grd2xyz grad_y.grd > grad_y.dat
cp grad_x.dat grad_x_"$input".dat
cp grad_y.dat grad_y_"$input".dat
rm raw.grd grad_x.grd grad_x.dat grad_y.grd grad_y.dat


### STEP 2-3 sig xy * cos y * cos y
input="sig_xy_cosy_cosy_pred"
# xyx to grd format
gmt surface "$input".xyz -Graw.grd $I $R
# gradient in x direction
gmt grdgradient raw.grd -A90 -Ggrad_x.grd
gmt grd2xyz grad_x.grd > grad_x.dat
# gradient in y direction
gmt grdgradient raw.grd -A0 -Ggrad_y.grd
gmt grd2xyz grad_y.grd > grad_y.dat
cp grad_x.dat grad_x_"$input".dat
cp grad_y.dat grad_y_"$input".dat
rm raw.grd grad_x.grd grad_x.dat grad_y.grd grad_y.dat


### STEP 2-4 sig xy
input="sig_xy_pred"
# xyx to grd format
gmt surface "$input".xyz -Graw.grd $I $R
# gradient in x direction
gmt grdgradient raw.grd -A90 -Ggrad_x.grd
gmt grd2xyz grad_x.grd > grad_x.dat
# gradient in y direction
gmt grdgradient raw.grd -A0 -Ggrad_y.grd
gmt grd2xyz grad_y.grd > grad_y.dat
cp grad_x.dat grad_x_"$input".dat
cp grad_y.dat grad_y_"$input".dat
rm raw.grd grad_x.grd grad_x.dat grad_y.grd grad_y.dat


### STEP 2-5 sig xx * cos y * cos y
input="sig_xx_cosy_cosy_pred"
# xyx to grd format
gmt surface "$input".xyz -Graw.grd $I $R
# gradient in x direction
gmt grdgradient raw.grd -A90 -Ggrad_x.grd
gmt grd2xyz grad_x.grd > grad_x.dat
# gradient in y direction
gmt grdgradient raw.grd -A0 -Ggrad_y.grd
gmt grd2xyz grad_y.grd > grad_y.dat
cp grad_x.dat grad_x_"$input".dat
cp grad_y.dat grad_y_"$input".dat
rm raw.grd grad_x.grd grad_x.dat grad_y.grd grad_y.dat

### STEP 3. Compute tractions

#use notebook and make sure to run this
# python compute_Fx_Fy.py
