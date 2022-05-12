#classes and subclasses to import
import cv2
import numpy as np
import os

filename = 'results.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)
    filep.close()

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))


def main(path_to_video_mp4_file_with_name):
	cap = cv2.VideoCapture(path_to_video_mp4_file_with_name)
	global image_red
	global image_blue
	global image_green
	image_red = cv2.imread("Overlay_Images/yellow_flower.png",-1)
	image_blue = cv2.imread("Overlay_Images/pink_flower.png",-1)
	image_green = cv2.imread("Overlay_Images/red_flower.png",-1)

	global old_contours
	global trigger
	global skip_frames
	global insert
	global trigger
	global final_list
	final_list=[]
	old_contours =[]
	insert =[]
	trigger=0
	#skip_frames = 0
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('video_output.mp4',fourcc, 16.57, (1280,720))

	# Blue Mask
	lower_blue = np.array([110,50,50])
	upper_blue = np.array([130,255,255])

	# Green Mask
	lower_green = np.array([50,50,50])
	upper_green = np.array([70,255,255])

	# Red Mask
	lower_red = np.array([0,50,50])
	upper_red = np.array([10,255,255])

	total_count =[0,0]		# Initial total count of contours
	prev_count = 0			# Initial previous count of contours
	while (True):
		global img
		ret, img = cap.read()
		if ret==True:
			img = cv2.GaussianBlur(img,(5,5),0)		# Blur the input image
			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)	# As detection of colors is easy on HSV image

			maskr = cv2.inRange(hsv, lower_red, upper_red)	# Red Mask
			maskr = cv2.GaussianBlur(maskr,(5,5),0)		# Blur the mask 

			maskb = cv2.inRange(hsv, lower_blue, upper_blue) # Blue mask
			maskb = cv2.GaussianBlur(maskb,(5,5),0)		 # Blur the mask
		
			maskg = cv2.inRange(hsv, lower_green, upper_green) # Green Mask
			maskg = cv2.GaussianBlur(maskg,(5,5),0)		   # Blur the mask

			total_count[prev_count %2] = total_contours(maskr+maskb+maskg)		#Counts total no. of contours in a frame
			if total_count[0] != total_count [1]:		# Skip 2 frames on detection of a new contour
				skip_frames=0
				insert =[]				# To detect if there is a change in number of contours in the frame
			# Find contours respective to each RGB value
			contours(maskr,'Red')
			contours(maskb,'Blue')
			contours(maskg,'Green')
							
			if total_count[prev_count % 2] == 0:
				trigger = 0				# Boundary check
			prev_count +=1
		
			# For canny edge detection
			#canny=cv2.Canny(dilate,100,200)

			putshape()		# Put overlay 
			cv2.imshow('frame',img)
			out.write(img)
		
			if cv2.waitKey(40) & 0xFF == ord('q'):
				break
		else:
			break

	print final_list
	cap.release()
	out.release()
	cv2.destroyAllWindows()

def total_contours(image):	# To find the total no. of contours in each frame
	image,contours, heirarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	return len(contours)

def contours (image,color):		# Detect contours for masked images
	image,contours, heirarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
       	for i in contours:
		if cv2.contourArea(i)>200:		# Boundary check
			detected_contours =[]
			M = cv2.moments(i)
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			detected_contours.extend([color,cx,cy])

			if detected_contours not in old_contours :		# To detect if any new contours has occured in the frame
				global skip_frames	
				if skip_frames<2:	# To skip 2 frames between contour detection and overlaying of flowers
					skip_frames += 1	# Mostly used to skip the frames where shapes are distorting
					return 
				global trigger
				vertices = cv2.approxPolyDP(i,0.01*cv2.arcLength(i,True),True)
				shape_detect=[]
				shape_detect.append(color)
				x,y,w,h = cv2.boundingRect(i)		# To find the bounding rectangle
				insert.extend([color,x,y,w,h])		# Can detect if multiple new shapes come to the frame at a single time
				trigger = 1	

				if len(vertices) == 3: # It is a triangle
					shape_detect.insert(1,"Triangle")
					#cv2.drawContours(img,[i],0,(255,0,0),2)

				elif len(vertices) == 4: # It is either a trapezium or a rhombus
					apratio = cv2.contourArea(i)/(w*h)
					
					if apratio>0.73 : # It is a trapezium
						shape_detect.insert(1,"Trapezium")
						#cv2.drawContours(img,[i],0,(255,0,0),2)
					elif apratio<0.73 : 	# It is a rhombus
						shape_detect.insert(1,"Rhombus")
						#cv2.drawContours(img,[i],0,(255,0,0),2)

				elif len(vertices) == 5: # It is a pentagon
					shape_detect.insert(1,"Pentagon")
					#cv2.drawContours(img,[i],0,(0,255,0),2)

				elif len(vertices) == 6: # It is a hexagon
					shape_detect.insert(1,"Hexagon")
					#cv2.drawContours(img,[i],0,(0,255,0),2)
				
				else : # It is a circle
					shape_detect.insert(1,"Circle")
					#cv2.drawContours(img,contours,0,(0,255,0),2)

				shape_detect.insert(2,cx)
				shape_detect.insert(3,cy)
				#shape_detect=["-".join("%s" %(k) for k in shape_detect)]
				old_contours.append(detected_contours)		# Stores the previous occured shapes in a list 
				final_list.append(shape_detect)		# Gets the final output
				writecsv(color,shape_detect[1],(cx,cy))

				
def putshape():			# To insert the flower overlay
		global image_red
		global image_blue
		global image_green
		if trigger == 1 :	# Boundary check
			for i in range(0,len(insert),5) :	
				x = insert[i+1]
				y = insert[i+2]
				w = insert[i+3]
				h = insert[i+4]
				if insert[i] == 'Red':
					image_red = cv2.resize(image_red,(w,h))
    					img[y:y+h,x:x+w,:] = blend_transparent(img[y:y+h,x:x+w,:],image_red)
				elif  insert[i] == 'Blue':
					image_blue = cv2.resize(image_blue,(w,h))
   					img[y:y+h,x:x+w,:] = blend_transparent(img[y:y+h,x:x+w,:],image_blue)
				elif  insert[i] == 'Green':
					image_green = cv2.resize(image_green,(w,h))
    					img[y:y+h,x:x+w,:] = blend_transparent(img[y:y+h,x:x+w,:],image_green)

	

	
#####################################################################################################
    #sample of overlay code for each frame
    #x,y,w,h = cv2.boundingRect(current_contour)
    #overlay_image = cv2.resize(image_red,(h,w))
    #frame[y:y+w,x:x+h,:] = blend_transparent(frame[y:y+w,x:x+h,:], overlay_image)
#######################################################################################################

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    main('./Video.mp4')
