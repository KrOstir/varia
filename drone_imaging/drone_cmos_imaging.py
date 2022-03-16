# Analysis of drone CMOS imaging
#
# Read drone rotations during imaging and create pixel grid
#
# Kristof Ostir, 2017-02-01
# University of Ljubljana, Faculty of Civil and Geodetic Engineering
# (c) 2017

# Imports
import numpy as np
import matplotlib.pyplot as plt

# Data
# Sensor size
s_rows = 2000  # number of rows
s_cols = 3008  # number of columns
# Sensor parameters
focal_len = 32  # focal length in mm
pix_size = 0.0055  # pixel size in mm
# Plot sampling
pix_sample = 50
# Imagining
proj_cent = [1000, 1000, 280]  # projection centre in (m)
elevation = 200  # relief elevation
# Plot filename
fn_plot_img = "grid_image.png"
fn_plot_sen = "grid_sensor.png"

# Rotation matrix from angles
def rotation_matrix(angles):
    omega, fi, kappa = angles[0], angles[1], angles[2]
    R_o = np.matrix(
        [
            [1, 0, 0],
            [0, np.cos(omega), -np.sin(omega)],
            [0, np.sin(omega), np.cos(omega)],
        ]
    )
    R_f = np.matrix(
        [[np.cos(fi), 0, np.sin(fi)], [0, 1, 0], [-np.sin(fi), 0, np.cos(fi)]]
    )
    R_k = np.matrix(
        [
            [np.cos(kappa), -np.sin(kappa), 0],
            [np.sin(kappa), np.cos(kappa), 0],
            [0, 0, 1],
        ]
    )
    R = R_o * R_f * R_k
    return R


# Rotation matrix (x, y, z)
# for every line omega, fi, kappa
# TODO Read from file
omega_fi_kappa = np.random.rand(s_rows, 3)
omega_fi_kappa[:, 0] = 1 + omega_fi_kappa[:, 0] / 2
omega_fi_kappa[:, 1] = 1 - omega_fi_kappa[:, 1] / 2
omega_fi_kappa[:, 2] = 2 * omega_fi_kappa[:, 2]
omega_fi_kappa = np.radians(omega_fi_kappa)

# Focal length in pixels
focal_len_px = focal_len / pix_size

sample_rows = range(1, s_rows, pix_sample)
sample_cols = range(1, s_cols, pix_sample)

# img_x = img_y = np.zeros((len(sample_rows), len(sample_cols)))
img_x = []
img_y = []
sen_x = []
sen_y = []

for i, r in enumerate(sample_rows):
    rot = rotation_matrix(omega_fi_kappa[i, :])
    y = s_rows / 2 - r + 0.5  # image y coordinate
    for j, c in enumerate(sample_cols):
        x = c - s_cols / 2 + 0.5  # image x coordinate
        sen_x.append(c)
        sen_y.append(r)
        img_x.append(
            proj_cent[0]
            + (elevation - proj_cent[2])
            * (rot[0, :].dot([x, y, -focal_len_px]))
            / (rot[2, :].dot([x, y, -focal_len_px]))
        )
        img_y.append(
            proj_cent[1]
            + (elevation - proj_cent[2])
            * (rot[1, :].dot([x, y, -focal_len_px]))
            / (rot[2, :].dot([x, y, -focal_len_px]))
        )

fig_x = s_cols / 100
fig_y = s_rows / 100
plt.figure(figsize=(fig_x, fig_y))
plt.title("Image Grid")
plt.scatter(img_x, img_y, marker="P", c=sen_y, cmap="gist_ncar")
plt.savefig(fn_plot_img)

plt.figure(figsize=(fig_x, fig_y))
plt.title("Sensor Grid")
plt.scatter(sen_x, sen_y, marker="P", c=sen_y, cmap="gist_ncar")
plt.savefig(fn_plot_sen)
