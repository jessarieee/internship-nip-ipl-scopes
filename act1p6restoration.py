# %%

# instructions

# Apply all three white balancing algorithms to your image
    # contrast stretching
    # gray world algorithm
    # white patch algorithm

# importing libraries
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# open the faded color pic
filename = 'act1p6restoration.jpeg'

img = mpimg.imread(filename)
    # shape and color channels (N, N, 3)
if img.dtype == np.uint8:
    img = img.astype(np.float32) / 255.0
    # jpeg is uint8 and we have to convert it to float
    # and the value is divided by 255 so the colors are just from 0 to 1

# verify that the img is in RGB (or 3 color channels)
if img.ndim != 3 or img.shape[2] != 3:
    # grayscale dimensions: (N, N)
    # rgb dimensions: (N, N, 3)
    # rgb third shape ^ (0th, 1st, 2nd) --> if 2nd shape should be 3
    raise ValueError('Input image must be a color image with 3 channels.')
        # stops the program is the pic is not RGB

# contrast stretching per channel

def contrast_stretch_channel(channel, low_percentile=0.02, high_percentile=0.98):
    values = channel.flatten()
        # channel (rgb) is flattened to a 1D array
    hist, bin_edges = np.histogram(values, bins=256, range=(0.0, 1.0))
        # hist contains the number of pixels
        # bin_edges stores the bin edges (but not needed in this script)
        # computes histogram
        # each bin has 1/255
    pdf = hist / hist.sum()
        # computes pdf 
    cdf = np.cumsum(pdf)
        # computes cdf

    Imin = np.searchsorted(cdf, low_percentile)
    Imax = np.searchsorted(cdf, high_percentile)
        # finds lower and upper percentiles
    
    Imin = Imin / 255.0
    Imax = Imax / 255.0
        # scales it converting it to intensities

    if Imax <= Imin: #to make sure the denominator isnt 0
        return channel
    stretched = np.clip((channel - Imin) / (Imax - Imin), 0.0, 1.0)
    return stretched
        # returns the enhanced color channel

R = img[:, :, 0] # contains all red intensities
G = img[:, :, 1] # contains all green intensities
B = img[:, :, 2] # contains all blue intensities

# applying constrast stretch to each RGB
R_st = contrast_stretch_channel(R)
G_st = contrast_stretch_channel(G)
B_st = contrast_stretch_channel(B)

# restacking each color layer into one image
img_stretch = np.stack((R_st, G_st, B_st), axis=2)

# gray world algorithm
means = np.mean(img.reshape(-1, 3), axis=0)
    # img.reshape(-1, 3): -1 determines the number of rows
        # (400, 400, 3) -> (160000, 3) ; one dimensional
    # np.mean: get the average of each channel in RGB
world_scale = np.mean(means) / means
    # np.mean(means) compute the overall average
    # each element is divided individually to scale
img_grayworld = np.clip(img * world_scale, 0.0, 1.0)
    # important to clip because after correction, some values exceed 1 or become negative values

# white patch algorithm
    # a white pixel has R = G = B

luminance = np.dot(img, [0.299, 0.587, 0.114])
    # luminance is the perceived brightness of pixel
    # computing luminance = 0.299R + 0.587G + 0.114B
    # RGB (3) -> brightness (1)
white_mask = luminance >= np.percentile(luminance, 99.5)
    # np.percentile(luminance, 99.5) computes pixel according to the 99.5th percentile
    # inequality considers a threshold value where if its beyond the percentile, it is TRUE
if white_mask.sum() < 10:
    # check if enough pixels exist
    img_whitepatch = None
        # if theres not enough, white patch algorithm wont happen
        # because theres not enough bright pixels for it to occur
else:
    Rw, Gw, Bw = np.mean(img[white_mask], axis=0)
        # compute the average white pixel color
        # img[white_mask] only selects the bright pixels that are above the threshold set
        # np.mean computes the average of each channel
    if Rw == 0 or Gw == 0 or Bw == 0:
        # check if there is 0
        img_whitepatch = None
            # if there is, a division by 0 will occur (error!)
            # if there is none, the correction is not gonna happen
    else:
        patch_scale = np.array([Rw, Gw, Bw], dtype=np.float32)
            # scaling factors
        img_whitepatch = img / patch_scale
            # correct the image for every pixel
        img_whitepatch = img_whitepatch / np.max(img_whitepatch)
            # np.max(img_whitepatch) finds the largest value so it rescales the values
            # so the value wont exceed 1
        img_whitepatch = np.clip(img_whitepatch, 0.0, 1.0)
            # values are clipped from 0 to 1

# displaying the results in a single resulting picture
fig, axes = plt.subplots(2, 2, figsize=(7, 5))

axes[0,0].imshow(img)
axes[0,0].set_title('Original')
axes[0,0].axis('off')

axes[0,1].imshow(img_stretch)
axes[0,1].set_title('Contrast Stretching')
axes[0,1].axis('off')

axes[1,0].imshow(img_grayworld)
axes[1,0].set_title('Gray World')
axes[1,0].axis('off')

if img_whitepatch is not None:
    axes[1,1].imshow(img_whitepatch)
    axes[1,1].set_title('White Patch')
    axes[1,1].axis('off')

# plot settings
#plt.tight_layout() # adjusts spacing between the subplots
plt.show()

print('Restoration complete.')
if img_whitepatch is None:
    print('White patch algorithm was skipped because no bright white region was found.')

# %%*