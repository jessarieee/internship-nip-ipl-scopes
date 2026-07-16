# Build the Shape of a Planet Shape from Power Spectra

import matplotlib.pyplot as plt
import numpy as np
import pyshtools as pysh
from cartopy import crs as ccrs

# we wish to create the spherical harmonic representation for the topography
# Rapp (1989): for spherical harmonic degrees up to

# Set maximum spherical harmonic degree, in this case l=719, following Wieczorek (2007)
lmax = 719
# Create array containing spherical harmonic degrees
degrees = np.arange(lmax+1, dtype=float)
# Set value for power law exponent, following Rapp (1989) for actual topography
beta = -2.13
# Set reference radius for the planet in kilometers (here we use the value for Earth)
r=6371
# Set value for A, following Rapp (1989) for actual topography
at = 155.4*2*np.pi*r
# Set degree 0 term to infinity to avoid the resulting singularity
degrees[0] = np.inf
# Create an array for the power spectrum using degrees
power = at*degrees**(beta)

# From the form of the power spectrum that was just defined, a random realization of a set of spherical harmonic coefficients representing the topography can be generated using `.from_random()`:
hlm = pysh.SHCoeffs.from_random(power, seed=12345)

# The seed value for the random number generator can be changed.
fig1, ax1 = hlm.plot_spectrum(show=False)
    # show=False is used to avoid a warning when plotting in inline mode

# The spherical harmonic representation of the topography can now be evaluated at points within a grid using `.expand()`:
grid = hlm.expand()

fig2, ax2 = grid.plot(projection = ccrs.Mollweide(central_longitude=0.0),
                    colorbar='bottom',
                    cb_label='Elevation [m]',
                    cb_triangles='both',
                    cmap='Spectral_r',
                    grid=True,
                    tick_interval=[60,30],
                    show=False)
ax2.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# You may choose to set a different central longitude for the projection.
clon = 180.0
fig2, ax2 = grid.plot(projection = ccrs.Mollweide(central_longitude=clon),
                    colorbar='bottom',
                    cb_label='Elevation [m]',
                    cmap='Spectral_r',
                    show=False)
ax2.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

#The coordinate representation may also be rotated with the Euler angles `alpha`, `beta`, and `gamma` using `.rotate()`:
rlat = 30.
rlon = 180.

alpha = 0.
beta = -(90.-rlat)
gamma = -rlon

hlm_rotated = hlm.rotate(alpha, beta,gamma, degrees=True)
grid_rotated = hlm_rotated.expand()

# results are plotted
clon = 0.0
fig3, ax3 = grid_rotated.plot(projection = ccrs.Mollweide(central_longitude=clon),
                    colorbar='bottom',
                    cb_label='Elevation [m]',
                    cmap='Spectral_r',
                    show=False)
ax3.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
