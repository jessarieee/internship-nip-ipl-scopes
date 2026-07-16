# %%

# importing libraries
import numpy as np 
import matplotlib.pyplot as plt 
import math

# initiating values

# 2d grids
N = 500 # pixel
x = np.linspace(-10, 10, num = N) # [-10,10]
y = x # square
X,Y = np.meshgrid(x,y)

# colors
Rd, Gn, Bl = np.zeros((N,N)), np.zeros((N,N)), np.zeros((N,N))
    # N x N = dimensions
 
# draw colored circles 
Rt, Rc, deg = 3, 4, 30
    # Rt = upper circle from the origin
    # Rc = radius of each circle
    # deg = angle used to position the upper circles
xt, yt = Rt*np.cos(deg*np.pi/180), Rt*np.sin(deg*np.pi/180)
    # angle is converted from deg to rad: π/180 * rad
 
R = np.sqrt((X)**2 + (Y+Rt)**2)
    # distance formula: sqrt((X-Xcenter)**2 + (Y-Ycenter)**2)
    # center = (0, -Rt)
    # red circle coordinates: (0, -3)
Rd[np.where(R < Rc)] = 1.0
    # every point that is (R < Rc) is inside the circle and the pixel is set to 1

R = np.sqrt((X-xt)**2 + (Y-yt)**2)
    # distance formula: sqrt((X-Xcenter)**2 + (Y-Ycenter)**2)
    # center = (xt, yt) = (Rt*np.cos(deg*np.pi/180), Rt*np.sin(deg*np.pi/180)) =  (3cos(30 deg), 3sin(30 deg))
    # green circle coordinates: (2.59, 1.5)
Gn[np.where(R < Rc)] = 1.0
    # every point that is (R < Rc) is inside the circle and the pixel is set to 1
 
R = np.sqrt((X+xt)**2 + (Y-yt)**2)
    # distance formula: sqrt((X-Xcenter)**2 + (Y-Ycenter)**2)
    # center = (-xt, yt) = (-Rt*np.cos(deg*np.pi/180), Rt*np.sin(deg*np.pi/180)) =  (-3cos(30 deg), 3sin(30 deg))
    # green circle coordinates: (-2.59, 1.5)
Bl[np.where(R < Rc)] = 1.0
    # every point that is (R < Rc) is inside the circle and the pixel is set to 1
 
I = np.zeros((N, N, 3))
    # N x N pixels
    # 3 colors

I[...,0] = Rd # red
I[...,1] = Gn # green
I[...,2] = Bl # blue
# similar to [:, :, 0]
 
fig = plt.figure()

plt.imshow(I)

# %%