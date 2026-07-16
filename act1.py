# %%

# # importing libraries
import numpy as np
import matplotlib.pyplot as plt

# initiating values

# 2d grids
N = 200 # higher number = finer 
x = np.linspace(-1, 1, num = N)
y = x # square
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
A = np.zeros(np.shape(R))
A[np.where(R < 0.5)] = 1.0

rgb = np.random.rand(200, 200, 3)

# display as image
plt.imshow(A, cmap = "gray")
plt.show()

# display as a 3D surface in cartesian coor system
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()

projection = '3d'
ax = fig.add_subplot(1,1,1, projection='3d')  # 1 row, 1 col, 1st plot

ax.plot_surface(X, Y, A, cmap = "pink")
plt.show()

rgbim = rgb*255.0 # scaling it to 0-255 range
img = rgbim.astype(np.uint8) # convert to uint8
plt.imsave("act1y.jpg",img) 
plt.imsave("act1y.bmp",img) 
plt.imsave("act1y.png",img) 
plt.imsave("act1y.tiff",img) 


# %%
