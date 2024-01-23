# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 12:26:14 2022

@author: hughd
"""
import copy
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 
from IPython.display import Image
import glob

# Initialize variables and arrays
x_copy = 0
y_copy = 0
video_array = []
xcoordinates = []
ycoordinates = []
X_radius = []
Y_radius = []
velocity_array = []
ratio_radius_deform = []
strain_array = []

# Set path to directory containing the images
path = r"C:\Users\hughd\Desktop\final year project\new video"
files = glob.glob(path + '\*.jpeg')
files.sort()

# Loop through each image file in the directory
for filename in files:
    new_img = cv2.imread(filename)
    video_array.append(new_img)

# Loop through each image in the video array
for pic in video_array:
    # Convert image to grayscale for contouring
    grayscale = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    # Apply binary threshold to image to make pixels white or black
    thresh, BW = cv2.threshold(grayscale, 100, 255, cv2.THRESH_BINARY)
    # Find contours in the binary image
    contours, h = cv2.findContours(BW, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Initialize array for ellipse fitting
    minEllipse = [None]*len(contours)
    # Loop through each contour found
    for j, c in enumerate(contours):
        # Draw contour on image
        cv2.drawContours(pic, contours, j,[255])
        # Check if contour has enough points for ellipse fitting
        if c.shape[0] > 5:
            # Fit an ellipse to the contour
            ellipse = cv2.fitEllipse(c)
            # Add ellipse to image if it meets size requirements
            if ellipse[1][0] > 15 and ellipse[1][1] > 15:
                cv2.ellipse(pic, ellipse,[255],2)
                # Append ellipse parameters to their respective arrays
                xcoordinates.append(ellipse[0][0])
                ycoordinates.append(ellipse[0][1])
                X_radius.append(ellipse[1][0])
                Y_radius.append(ellipse[1][1])
                # Calculate deformation and strain of cell
                deformation = (ellipse[1][1]*2) / (ellipse[1][0]*2)
                strain = ((ellipse[1][1]*2) - (ellipse[1][0]*2)) / ((ellipse[1][1]*2) + (ellipse[1][0]*2))
                strain_array.append(strain)
                ratio_radius_deform.append(deformation)
                # Calculate velocity of cell
                if x_copy == 0:
                    deltax = 0
                if y_copy == 0:
                    deltay = 0
                if x_copy != 0:
                    deltax = x_copy - ellipse[0][0]
                if y_copy != 0:
                    deltay = y_copy - ellipse[0][0]
                velocity = np.sqrt((deltax**2 + deltay**2))
                velocity_array.append(velocity)
                # Update x_copy and y_copy for next iteration
                x_copy = copy.copy(ellipse[0][0])
                y_copy = copy.copy(ellipse[0][1])
    # Set up plot for displaying image with drawn contours
    Ydata=np.arange(len(ycoordinates))
    Rdata=np.arange(len(ratio_radius_deform))
    # show video of microfluidic channel
    cv2.imshow('cell deformation',pic)
    if cv2.waitKey(100) & 0xff == ord('w'):
        # allows the video to close when 'w' is clicked
       break
cv2.destroyAllWindows()
# creates 4 subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1, figsize=(8, 6))
# sets the layout type
fig.tight_layout()
# calculates the average value for strain, DI and velocity
average_1=np.mean(ratio_radius_deform)
average_2=np.mean(strain_array)
average_3=np.mean(velocity_array)
# calculates the max value for strain, DI and velocity
max_1=max(ratio_radius_deform)
max_2=max(strain_array)
max_3=max(velocity_array)
# produces the graph of Y coordinates vs frames
ax1.scatter(Ydata, ycoordinates, s= 10,  c='r', label='ycoordinates vs frames')
ax1.set_xlabel('frames')
ax1.set_ylabel('ycoordinate')
ax1.set_ylim([0, 320])
ax1.set_title('Ycoordinates of cells passing through a microfluidic channel')
ax1.legend()
# produces the graph of Deformation index vs frames   
ax2.scatter(Rdata, ratio_radius_deform, s=10 , c='b', marker='x', label='deformity vs frames')
ax2.axhline(y=average_1, color='r', linestyle='-', label='average cell deformation')
ax2.axhline(y=2.84, color='g', linestyle='-', label='critical deformation before rupture ')
ax2.set_xlabel('frames')
ax2.set_ylabel('deformity')
ax2.set_ylim([0, 3.5])
ax2.set_title('DI of cells passing through a microfluidic channel')
ax2.legend()
# produces the graph of strain vs frames
ax3.scatter(Rdata, strain_array, s=10,  c='g', label='Strain vs frames')
ax3.axhline(y=average_2, color='r', linestyle='-', label='average cell strain')
ax3.set_xlabel('frames')
ax3.set_ylabel('strain')
ax3.set_ylim([0, 0.6])
ax3.set_title('strain of cells passing through a microfluidic channel')
ax3.legend()
# produces the graph of velocity vs frames
ax4.scatter(Rdata, velocity_array, s=10,  c='y', label='Velocity vs time')
ax4.axhline(y=average_3, color='r', linestyle='-', label='average cell velocity')
ax4.set_xlabel('frames')
ax4.set_ylabel('velocity')
ax4.set_ylim([0, 200])
ax4.set_title('velocity of cells passing through a microfluidic channel')
ax4.legend()