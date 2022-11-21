###############_to-use the camera to capture image_######################
# import cv2 as cv
# from cv2 import aruco 
# cap = cv.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#     cv.imshow("frame",frame)
#     key = cv.waitKey(1)
#     if key ==ord('q'):
#         break
# cap.release()
# cv.destroyAllWindows()
#############################################################################
import serial
import time
import cv2 as cv
from cv2 import aruco 
import numpy as np
#############################################################################
data = [[0,"mango",12],[1,"apple",22],[2,"banana",14],[3,"pineapple",30],[4,"lichi",2]]
######_activating serial communication_######
serialcomm = serial.Serial('COM6', 9600)
serialcomm.timeout = 1
########################################

total = 0
def check_price(ID,data,total):
    for i in range (len(data)):
        if (ID == data[i][0]):
            total = total + data[i][2]

            string_item = str(data[i][1])
            send_id(string_item)
            time.sleep(0.5)

            string_price = str(data[i][2])
            send_id(string_price)
            time.sleep(0.5)

            stirng_total = str(total)
            send_id(stirng_total)
            time.sleep(0.5)
            print(total)
###########################################################################

def send_id(id):
    serialcomm.write(id.encode()) #to send to arduino
    time.sleep(0.5)
    print(serialcomm.readline()) #.decode('ascii')

#################################

marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50) #initialise to read aruco code
param_markers = aruco.DetectorParameters_create() #creates a parameter for aruco code detection

cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #convert image to grayscale for decreasing processing time
    marker_corners, marker_IDs, reject = aruco.detectMarkers( #detect aruco code,marker_corners = get into frame,
    gray_frame, marker_dict, parameters=param_markers)        # "marker_IDs= to store the id"
                                                              #reject = to reject images which are not actually a aruco code
                                                              # gray_frame, marker_dict, parameters=param_markers --> ye parameters hai
   
    # for ids, corners in zip(marker_IDs, marker_corners):
    #     print(ids, corners)                                  #prints scanned id and corners location

################_drawing line around aruco code_#############################
    if marker_corners:  
        for ids, corners in zip(marker_IDs, marker_corners):
                cv.polylines(
                    frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA #import numpy for this 
                )                                                                          #draws lines around the aruco code
                #print(corners.shape) #prints shape of the aruco code
##################################################################################

############_need to reshape lines around aruco to display its value on it_################
                corners = corners.reshape(4,2) #these arguments are not actually integer
                corners = corners.astype(int) #convertinf the above arguments to integer
                top_right = corners[0].ravel() #stored the top right corner position of the aruco

                #printing text on it
                cv.putText(
                frame,
                f"id: {ids[0]}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv.LINE_AA,
            )
            ##########_send id to arduino_######################
                # input = str(ids[0])
                # send_id(input)
                ###########################################
                check_price(ids[0],data,total)
    ###############################################################
                # print(type(ids[0]))
                # a=ids[0].toint()
                # print(type(a))
                # time.sleep(0.5)
               # print(marker_IDs) #scanned id number example -->[[5]]
                

    cv.imshow("frame",frame)
    key = cv.waitKey(1)
    if key ==ord('q'):
        break

serialcomm.close()
cap.release()
cv.destroyAllWindows()
