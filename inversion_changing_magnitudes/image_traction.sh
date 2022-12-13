#!/bin/bash


## GMT setup  (no worries about these)
gmt set FORMAT_GEO_MAP ddd.x
gmt set MAP_FRAME_TYPE plain


## params
##multiply by ice viscosity

# ice_thickness
T="-T0/3000/500" # mVal/MVal/Interval
input="T_ice.dat" # Input file 
CPT="ice.cpt" #the name of your cpt file
color_type="jet" # cpt name
#
# S="-Se0.1/0/0"
S="-Se0.01/0/0"
M="greenland_traction.ps" # output map figure name
R="-R-80/-10/55/85" # boundary of your map (mlon/Mlon/mlat/Mlat)
J="-Jm0.18" # map projection (m: a type of a projection; # is the size)
B="-BNesW -Ba10f5" # map boundary ticks and location of labels
ocean_color="slategray3" #R/G/B [0-255]

vel_input="traction_parsed.gmt" 

#psuedo 
#traction related to the friction
#
#f(theta) = - 


## plot data
gmt psbasemap $R $J $B -P -V -Y2.0i -K > $M
## color scale
gmt makecpt -C$color_type $T -Z -Do > $CPT

gmt blockmean $input $R -I6m -V > plot.dat
gmt surface plot.dat -Ggm0.grd -I6m $R -T0.2
gmt grdgradient gm0.grd -Ggm0.shd  -Nt1 -A20

# with a shade
#gmt grdimage gm0.grd -C$CPT -Igm0.shd  $R $J -O -V -K >> $M

# PLOT THE INPUT VALUES without a shade
gmt grdimage gm0.grd -C$CPT $R $J -V -K -O >> $M

# coastline
gmt pscoast $J $R $B -Df -S$ocean_color -W0.1 -V -N1 -N2 -K -O >> $M

gmt psxy $R $J -O -K -Gwhite -Wthicker -V -A >> $M <<END
-70 59
-52 59
-52 57
-70 57
END


gmt psvelo $R -W0.1,black -Gblack $S  -L $J -A0.01/0.1/0.025 -O -K<<EOT>>$M
-68 58  5  0 0   0 0 0
EOT

gmt pstext  $R $J -P -O -K -V  <<EOT>> $M
-59 58   12   0.0   0       6     5 MPa
EOT




gmt psvelo $vel_input $R -W0.4,200/0/0 -Gred $S -L $J -A0.03/0.1/0.05 -O >>$M



gmt psconvert $M -Tf -A
