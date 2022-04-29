import cv2
import numpy as np

cap = cv2.VideoCapture("/home/harsh/Desktop/Lane_detect/Lane Detection Test Video 01.mp4")

ur = []
ul = []

ctl,ctr = 0,0

dr = []
dl = []

dist = []

msg = 'Straight'

'''
Initial few seconds will not be accurate since the program gathers information first and then it starts enacting.
Will tell the robot to move ledt or right depending on whether they are too left or too right.

We maintain an array of upper right,left and lower right,left coordinates when left lane and right lane are detected.
And try to construct the lane when there is no detection by using previous data and also checking about position.
The distance between the lanes is also maintained in an array for positioning.

'''

while(cap.isOpened()):
        # Capture frame-by-frame
	ret, frame = cap.read()
	image = frame[500:700,300:900]
	cv2.imshow("ROI Frame",frame)

        #OPERATIONS:

        #erosion followed by canny edge detection
	krnl = np.ones((3,3),np.uint8)
	out3 = cv2.erode(image,krnl,iterations = 1 )
	edges = cv2.Canny(out3,100,230)
	cv2.imshow('Edges',edges)
	
	#creating mask
	mask = np.zeros(image.shape, dtype="uint8")
	maskk = np.zeros(edges.shape, dtype="uint8")
	pts = np.array([[25, 190], [275, 50], [380, 50], [575, 190]], dtype=np.int32)
	cv2.fillConvexPoly(mask, pts, [255,255,255])
	cv2.fillConvexPoly(maskk, pts, [255,255,255])
	cv2.imshow("Mask", mask)

	#masked ROI
	roi = cv2.bitwise_and(image,mask)
	cv2.imshow('Region Of Interest',roi)
	edges = cv2.bitwise_and(edges,maskk)
	cv2.imshow('B/W R.O.I.',edges)

 	#houghLineP
	lines = cv2.HoughLinesP(edges,6,np.pi/60,100,minLineLength = 40,maxLineGap = 25,lines = np.array([])) 
	
	rlane = []
	llane = []
	avgr,nr = 0,0
	avgl,nl = 0,0
	x1r = []
	x2r = []
	x1l = []
	x2l = []
	y1r = []
	y2r = []
	y1l = []
	y2l = []
	clr = [0,255,0]
	
	if lines is not None:
		for line in lines:
			#print(line)
			for x1,y1,x2,y2 in line:
				slope = (y1-y2)/(x1-x2)
				c = y1-slope*x1
				if slope<0:
					llane.append([x1,y1,x2,y2])
				else:
					rlane.append([x1,y1,x2,y2])
	
	drawl,drawr=1,1
	#print("LEFT")
	if len(llane)!=0:
		for x1,y1,x2,y2 in llane:
			x1l.append(x1) 
			x2l.append(x2)
			y1l.append(y1)
			y2l.append(y2)

		x1ll = np.median(x1l)
		y1ll = np.median(y1l)
		x2ll = np.median(x2l)
		y2ll = np.median(y2l)
		

		m = (y2ll-y1ll)/(x2ll-x1ll)
		c = y1ll - m*x1ll
		a = (51-c)/m
		if np.isnan(a)==0:
			a=int(a)
		else:
			drawl=0
		b = (191-c)/m
		if np.isnan(b)==0:
			b=int(b)
		else:
			drawl=0
		
		ul.append(a)
		dl.append(b)
		ctl += 1

		if drawl:	
			cv2.line(image,(a,51),(b,191),[0,255,0],2)
		al = a	

	elif len(llane)==0:
		if len(ul)>30:
			a = int(np.median(ul[-30:]))
			b = int(np.median(dl[-30:]))
		
		if len(dist)>100:
			thold = np.median(dist)
			if (ur[-1:][0]-a)<thold-20:
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(image,'Move Left',(image.shape[1]//3,170), font, 1,(0,0,255),2,cv2.LINE_AA)
				msg = "Move Left"				
				drawl = 0
				clr = [0,0,255]
			elif (ur[-1:][0]-a)>thold+20:
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(image,'Move Right',(image.shape[1]//3,170), font, 1,(0,0,255),2,cv2.LINE_AA)
				msg = "Move Right"
				drawl = 0
				clr = [0,0,255]

		cv2.line(image,(a,51),(b,191),clr,2)				
			

	
	#print("RIGHT")
	if len(rlane)!=0:
		for x1,y1,x2,y2 in rlane:
			x1r.append(x1) 
			x2r.append(x2)
			y1r.append(y1)
			y2r.append(y2)

		x1rr = np.median(x1r)
		y1rr = np.median(y1r)
		x2rr = np.median(x2r)
		y2rr = np.median(y2r)

		m = (y2rr-y1rr)/(x2rr-x1rr)
		c = y1rr - m*x1rr
		a = (51-c)/m
		if np.isnan(a)==0:
			a=int(a)
		else:
			drawr=0
		b = (191-c)/m
		if np.isnan(b)==0:
			b=int(b)
		else:
			drawr=0
		
		ur.append(a)
		dr.append(b)

		if drawr:	
			cv2.line(image,(a,51),(b,191),[255,0,0],2)
		if len(llane)>0:
			dist.append(ur[-1:][0]-ul[-1:][0])
			
	
	

	elif len(rlane)==0:
		if len(ur)>30 and ctr<500:
			a = int(np.median(ur[-30:]))
			b = int(np.median(dr[-30:]))
		
		

		cv2.line(image,(a,51),(b,191),[0,0,255],2)

	
	
	cv2.imshow("Lanes",image)
	print(msg)
	msg = 'Straight'
	
        # Display the resulting frame
	if cv2.waitKey(30) & 0xFF == ord('q'):
		break


		# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()




#BY SHRIYA GAUTAM
