import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

path = "/home/harsh/Desktop/Lane_detect/lane2.jpeg"
img = cv2.imread(path,0)
gimg = img.copy()
images = cv2.imread(path,1)
h,w = img.shape


#7/12 is the ideal y-cutoff
for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		if i<img.shape[0]//2:
			gimg[i][j]=0


#erosion followed by canny edge detection
krnl = np.ones((3,3),np.uint8)
out3 = cv2.erode(gimg,krnl,iterations = 1 )
edges = cv2.Canny(out3,100,230)
#cv2.imshow('a',edges)
'''
lines = cv2.HoughLinesP(edges,6,np.pi/60,100,minLineLength = 40,maxLineGap = 25,lines = np.array([])) 
print(lines)

for line in lines:
	for x1,y1,x2,y2 in line:
		cv2.line(images,(x1,y1),(x2,y2),[0,255,0],1)
'''
#mask : in ROI
for i in range(edges.shape[0]):
	for j in range(edges.shape[1]):
		if edges[i][j] == 255:
			if i>15*edges.shape[0]//24:
				l = math.floor(w*(1-(i/h)))
				r = math.floor(w*i/h)
				if j>l and j<r:
					images[i][j]=[0,0,255]


#cv2.imshow('img',crpimg)
#cv2.imshow('out',out)
#cv2.imshow('out1',edges)
cv2.imshow('img1',images)
cv2.waitKey(0)
cv2.destroyAllWindows()


# By Shriya Gautam

















