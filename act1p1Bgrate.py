# %%

# INSTRUCTIONS
# Grating with frequency of 5 line pairs/cm
# line pair is a strip of black (0) and white (1) 

# importing libraries
import numpy as np
import matplotlib.pyplot as plt

# initiating values

# 2d grids
N = 400 # pixel count: 400x400 
x = np.linspace(-2, 2, num = N) # X ϵ [-2 cm, 2 cm]
y = x # square ; Y ϵ [-2 cm, 2 cm]
X, Y = np.meshgrid(x, y)

# grating w/ with frequency of 5 line pairs/cm
freq_sin = 5.0 # cycles per cm
sinu = np.sin(2 * np.pi * freq_sin * X) 
    # ω, angular freq = 2 π f
    # the sine wave is only a function of x
sinu_img = np.uint8(sinu + 1)
grating = np.where(sinu >= 0, 255, 0)
    # >= creates boolean mask (T/F), checks for crests
    # this T/F becomes an image array
    # T = outputs white (1) ; F = outputs black (0) 


# plot settings
plt.title('Grating (frequency: 5 cycles/cm)')
plt.imshow(grating, cmap = "gray", extent=[-2,2,-2,2])
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')

# display as image
plt.show()

# %%
