# Analysis of drone CMOS imaging
#
# Read drone rotations during imaging and create pixel grid
#
# Kristof Ostir, 2017-02-01
# University of Ljubljana, Faculty of Civil and Geodetic Engineering
# (c) 2017

# Imports
import numpy as np

# function
# mreza_objKrd()
#
# Data
# Sensor size
s_rows = 2000 # number of rows
s_cols = 3008 # number of columns
focal_len = 32 # focal length in mm
pix_sample = 100 # pixel sampling
pix_size = 0.0055 # pixel size in mm
proj_cent = [1000, 1000, 280] # projection centre in (m)
elevation = 200 # relief elevation

# Rotation matrix (x, y, z)
# for every line omega, fi, kappa
# TODO Read from file
omega_fi_kappa = np.random.rand(s_rows, 3)
omega_fi_kappa[:,0] = 1 + omega_fi_kappa[:,0] / 2
omega_fi_kappa[:,1] = 1 - omega_fi_kappa[:,1] / 2
omega_fi_kappa[:,2] = 2 * omega_fi_kappa[:,2]
omega_fi_kappa = np.radians(omega_fi_kappa)

# Focal length in pixels
focal_len_px = focal_len / pix_size

# vv = 1:n: v;
# sv = 1:n: s;
#
# for i = 1:length(vv)
# R = rotacijska_matrika(omega_fi_kappa(vv(i),:));
# y = v / 2 - vv(i) + 0.5; % slikovna
# koordinata
# y
# for j= 1:length(sv)
# x = sv(j) - s / 2 + 0.5; % slikovna
# koordinata
# x
# X(i, j) = X0(1) + (Z - X0(3)) * (R(1,:)*[x;
# y;
# -c]) / (R(3,:)*[x;
# y;
# -c]);
# Y(i, j) = X0(2) + (Z - X0(3)) * (R(2,:)*[x;
# y;
# -c]) / (R(3,:)*[x;
# y;
# -c]);
# end
# end
#
# figure(1), cla, hold
# on
# for i=1:size(X, 1)
# plot(X(i,:), Y(i,:), 'r')
# for j=1:size(X, 2)
# plot(X(i, j), Y(i, j), '.')
# end
# end
# axis
# equal,
# hold
# off
#
# % %
# function
# R = rotacijska_matrika(omega_fi_kappa)
# % funkcija
# izracuna
# 3
# D
# rotacijsko
# matriko
#
# Ro = [1, 0, 0; % rotacija
# okoli
# x
# za
# kot
# omega
# 0, cos(omega_fi_kappa(1)), -sin(omega_fi_kappa(1));
# 0, sin(omega_fi_kappa(1)), cos(omega_fi_kappa(1))];
#
# Rfi = [cos(omega_fi_kappa(2)), 0, sin(omega_fi_kappa(2)); % rotacija
# okoli
# y
# za
# kot
# fi
# 0, 1, 0;
# -sin(omega_fi_kappa(2)), 0, cos(omega_fi_kappa(2))];
#
# Rk = [cos(omega_fi_kappa(3)), -sin(omega_fi_kappa(3)), 0; % rotacija
# okoli
# z
# za
# kot
# kapa
# sin(omega_fi_kappa(3)), cos(omega_fi_kappa(3)), 0;
# 0, 0, 1];
#
# R = Ro * Rfi * Rk;
#
#
#
