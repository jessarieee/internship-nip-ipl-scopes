# %%

# instructions

# PART 1
# open your dark-looking image in python and convert to grayscale

# importing libraries
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

img = mpimg.imread('act1p4.jpeg')     
gray = rgb2gray(img)    
plt.imshow(gray, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)

plt.title("Histogram of the Image")
#plt.show()

# reference: https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python

# PART 2
# obtain the grayscale histogram of image
# normalize by the number of pixels to get its PDF

gray_u8 = np.round(gray * 255).astype(np.uint8)
    # coverts the image to 8-bit integers
    # gray contains intensities between black (0) and white (1)
        # (gray * 255) converts values 0-1 to 0-255
        # np.round rounds up
        # astype(np.uint8) converts numbers to 8-bit unsigned integers:
counts, bin_edges = np.histogram(gray_u8, bins=256, range=(0, 255))
    # computes for the histogram (pixel counts per intensity)
    # bins=256 - one bin per grayscale level
    # range=(0, 255) only consider pixel values bet 0 to 255
    # counts - number of pixels
        # ex: counts(0) - number of black pixels

pdf = counts / counts.sum()
    # counts.sum total number of pixels
    # formula: total pixel count in (0) / overall pixel count
cdf = np.cumsum(pdf)
    # cumulative sum of PDF

figure, pdf_plt = plt.subplots(figsize=(8, 6))
    # 8 x 6 inches of figure
pdf_plt.bar(np.arange(256), pdf, color='red', alpha=0.6)
    # plotting the pdf figure
        # from 0-255, pdf = height of each bar, alpha = transparency (0paque-1nvisible)
pdf_plt.set_ylabel('PDF', color='red')
    # labelling the y-axis

cdf_plt = pdf_plt.twinx()
    #creates a superimposed plot sharing the same x axis
cdf_plt.plot(np.arange(256), cdf, color='blue')
    # plotting the cdf line that rises from 0-1 as always
cdf_plt.set_ylabel('CDF', color='blue')
    # labelling the y-axis

# plot settings
plt.title("PDF & CDF via Histogram")
#plt.show()

# reference: 
# https://www.geeksforgeeks.org/python/how-to-calculate-and-plot-a-cumulative-distribution-function-with-matplotlib-in-python/

# desired CDF for a uniform 8-bit grayscale distribution
x = np.arange(256) # set up x 
desiredCDF = (1/255.0) * x
    # desired CDF = k/255 is a straight line which means theres equal probability for every intensity

# backproject pixel values using the inverse of the desired CDF
pixel_cdf = cdf[gray_u8.flatten()]
    # pixel_cdf is the CDF value for each original graylevel pixel
    # flatten the image to make it a 1D array
    # cdf[] uses gray level as indices where each px is now replaced by its cumulative probability
newGrayLvl = np.interp(pixel_cdf, desiredCDF, x)
    # interpolation: finding the new gray levels
    # np.interp(value, x_values, y_values) finds the y-value corresponding to a given x-value
        # pixel_cdf = 0 to 1
        # x = 0 to 255
img_newEq = newGrayLvl.reshape(gray_u8.shape).astype(np.uint8)
    # put back into the image from flattened back to its original dimensions
    # astype(np.uint8) converts it to 8-bit unsigned integers which enables plotting

#notes
# og image -> cdf -> px to cdf value -> straight line cdf -> new gray levels -> image
# gray_u8  -> cdf -> pixel_cdf       -> desiredCDF        -> newGS           ->

# display the original and the mapped image

plt.figure(figsize=(12,6)) # new plot
plt.subplot(1, 2, 1)
    # dividing the plot to (row, column, image#)
    # 1 row, 2 columns, 1st image
plt.imshow(gray_u8, cmap='gray') 
    # plt.imshow displays 2D array as image
plt.title('Original Grayscale')
plt.axis('off')

plt.subplot(1, 2, 2) # 2nd image
plt.imshow(img_newEq.astype(np.uint8), cmap='gray', vmin=0, vmax=255)
    # astype(np.uint8) converts it to uint8
    # vmin and vmax normalizes the values of the grayscale 0black, 255white
        # truncates other values outside of this range
plt.title('Histogram Equalized Image')
plt.axis('off')
#plt.show()

# plotting the histogram and CDF from the Histogram Equalized Image values
# to check if the desired CDF was achieved

# histogram (similar process as the first)
counts_newEq, bins_newEq = np.histogram(img_newEq, bins=256, range=(0,255))
pdf_newEq = counts_newEq / counts_newEq.sum()
cdf_newEq = np.cumsum(pdf_newEq)

# desired uniform cdf
x = np.arange(256)
desiredCDF_newEq = x / 255.0

# pdf of equalized image
fig, pdf_newEq_plt = plt.subplots(figsize=(12,6))
    # dividing the plot to (row, column, image#)
    # 1 row, 2 columns, 1st image
pdf_newEq_plt.bar(x, pdf_newEq, color='red', alpha=0.6, label='PDF')
pdf_newEq_plt.set_xlabel('Gray Level')
pdf_newEq_plt.set_ylabel('PDF', color='red')

# cdf of equalized image
cdf_newEq_plt = pdf_newEq_plt.twinx()
    #creates a superimposed plot sharing the same x axis
cdf_newEq_plt.plot(np.arange(256), cdf, color='blue')
    # plotting the cdf line that rises from 0-1 as always
cdf_newEq_plt.set_ylabel('CDF', color='blue')
    # labelling the y-axis

plt.title("Equalized PDF & CDF via Histogram Equalized Image values")
# plt.show()

# PART 3: CONTRAST STRETCHING (Activity 1.5)
# Apply contrast stretching using percentiles and normalization to find Imin and Imax
# Formula: Inew = (Iold - Imin) / (Imax - Imin)

# grayscale image (0-255 values as uint8) 
# -> min percentile (lower; 0.1 for 10th percentile) 
# -> max percentile (upper; 0.9 for 90th percentile)

def contrast_stretch(image, percentile_min = 0.1, percentile_max = 0.9):
    
    # flatten image to get all the pixel values
    flat_image = image.flatten()
    
    # find the grayscale values at the percentiles using the CDF
    # np.searchsorted finds the indices where elements should be inserted to maintain order in a sorted array
    Imin = np.searchsorted(cdf, percentile_min)
    Imax = np.searchsorted(cdf, percentile_max)
    
    print(f"Percentiles: {percentile_min*100:.0f}%-{percentile_max*100:.0f}%")
    print(f"Imin (at {percentile_min*100:.0f}% CDF) = {Imin}, Imax (at {percentile_max*100:.0f}% CDF) = {Imin}")
        #:.0f f-stirng format specifier and shows 0 afte decimal point 
    
    ## applying contrast stretching formula: Inew = (Iold - Imin) / (Imax - Imin)

    # clip values to to make sure its within the range [Imin, Imax]
    clipped_img = np.clip(image, Imin, Imax)
    
    # normalize to 0-1 range
    if Imax > Imin:
        stretched = (clipped_img - Imin) / (Imax - Imin)
    else:
        stretched = clipped_img
    
    # scale back to 0-255 range and convert to uint8
    stretched_img = (stretched * 255).astype(np.uint8)
    
    return stretched_img

# test with different percentiles
percentile_sets = [
    (0.1, 0.9),   # 10th to 90th percentile
    (0.05, 0.95), # 5th to 95th percentile
    (0.02, 0.98), # 2nd to 98th percentile
]

# Create a figure with subplots showing different percentile settings
fig, axes = plt.subplots(2, len(percentile_sets) + 1, figsize=(15, 8))

# Display original image in top-left
axes[0, 0].imshow(gray_u8, cmap='gray')
axes[0, 0].set_title('Original Image')
axes[0, 0].axis('off')

axes[1, 0].imshow(gray_u8, cmap='gray')
axes[1, 0].set_title('Original Image')
axes[1, 0].axis('off')

# Apply contrast stretching with different percentiles
for idx, (pmin, pmax) in enumerate(percentile_sets):
    stretched = contrast_stretch(gray_u8, pmin, pmax)
    
    # Top row: stretched images
    axes[0, idx + 1].imshow(stretched, cmap='gray')
    axes[0, idx + 1].set_title(f'Stretched\n({pmin*100:.0f}%-{pmax*100:.0f}%)')
    axes[0, idx + 1].axis('off')
    
    # Bottom row: histograms of stretched images
    axes[1, idx + 1].hist(stretched.flatten(), bins=256, color='steelblue', alpha=0.7)
    axes[1, idx + 1].set_title(f'Histogram\n({pmin*100:.0f}%-{pmax*100:.0f}%)')
    axes[1, idx + 1].set_xlim([0, 255])

plt.tight_layout()
plt.show()

# Additional exploration: Show the effect with custom percentiles
print("\n" + "="*60)
print("EXPLORING CUSTOM PERCENTILES FOR CONTRAST STRETCHING")
print("="*60)

custom_percentiles = [
    (0.15, 0.85),
    (0.2, 0.8),
    (0.3, 0.7),
]

fig, axes = plt.subplots(1, len(custom_percentiles) + 1, figsize=(16, 4))

# Original
axes[0].imshow(gray_u8, cmap='gray')
axes[0].set_title('Original')
axes[0].axis('off')

# Custom percentile stretches
for idx, (pmin, pmax) in enumerate(custom_percentiles):
    stretched = contrast_stretch(gray_u8, pmin, pmax)
    axes[idx + 1].imshow(stretched, cmap='gray')
    axes[idx + 1].set_title(f'Stretch: {pmin*100:.0f}%-{pmax*100:.0f}%')
    axes[idx + 1].axis('off')

plt.tight_layout()
plt.show()

# %%
