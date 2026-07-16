# %%

# INSTRUCTIONS
# physical images dont have neg value
# range of intensities of your sinusoid is between 0 and 255? 

# # importing libraries
import numpy as np
import matplotlib.pyplot as plt

# initiating values

# 2d grids
N = 400 # pixel count: 400x400 
x = np.linspace(-2, 2, num = N) # X ϵ [-2 cm, 2 cm]
y = x # square ; Y ϵ [-2 cm, 2 cm]
X, Y = np.meshgrid(x, y)

# sinusoidal pattern along x direction, with frequency of 4 cycles/cm
freq_sin = 4.0 # cycles per cm
sinu = np.sin(2 * np.pi * freq_sin * X) 
    # ω, angular freq = 2 π f
    # the sine wave is only a function of x

# scale sinusoid from [-1, 1] to [0, 255]
sinu_img = np.uint8(127.5 * (sinu + 1))
    # uint8 = unsigned 8-bit integer, stores data from 0 to 255, dont store negative value
    # 255 / 2 = 127.5
    # sinu + 1 = shifts by 1 so it oscillates from [0,2] instead of [1,1]


# plot settings
plt.title('Sinusoid along x-direction (frequency: 4 cycles/cm)')
plt.imshow(sinu_img, cmap = "gray")
plt.xlim(0, 250) # x values
plt.ylim(0, 250) # y values
plt.colorbar() # color bar to show gradient

# display as image
plt.show()


# %%