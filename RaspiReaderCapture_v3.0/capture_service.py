# capture an image and send it over bluetooth

import os
import time
import RPi.GPIO as gp
from bluetooth import *
from picamera import PiCamera
from datetime import datetime
from io import BytesIO
import numpy as np
import cv2

gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(8, gp.OUT)
gp.setup(10, gp.OUT)

gp.output(8, gp.HIGH)
gp.output(10, gp.HIGH)

# set up the camera
camera = PiCamera()
camera.resolution = (3280, 2464)
camera.iso = 800
time.sleep(2)
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

if not os.path.isdir('data'):
    os.mkdir('data')

clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(4,4))

server_sock=BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "InfantReader",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
                    )

print "Waiting for connection on RFCOMM channel %d" % port
client_sock, client_info = server_sock.accept()
print "Accepted connection from ", client_info

raw_image = None
while True:          
    try:
        data = client_sock.recv(1024)
        if len(data) == 0: print("len of data is 0"); break
        print "received [%s]" % data
        if data.lower().strip() == "capture":
            output_buffer = np.empty((3296 * 2464 * 3,), dtype=np.uint8)
            start = datetime.now()
            print("taking fingerprint")
            camera.capture(output_buffer, 'bgr')
            end = datetime.now()
            print("Finished capturing in {} seconds".format(end - start))
            start = datetime.now()
            # crop the fingerprint
            output_buffer = output_buffer.reshape((2464, 3296, 3))
            output_buffer = output_buffer[:2464, :3280, :]
            #output_buffer = output_buffer[900:(900+1150), 800:(800+1800), :]
            output_buffer = output_buffer[500:1800, 825:2600, :]
            
            img = cv2.cvtColor(output_buffer, cv2.COLOR_RGB2GRAY)
            resized_image = cv2.resize(img, (448, 448))
            resized_image = cv2.bitwise_not(resized_image)
            resized_image = clahe.apply(resized_image)

            # convert image to bytes
            img_bytes = cv2.imencode('.jpg', resized_image)[1].tostring()
            
            start = datetime.now()
            client_sock.send(img_bytes)
            end = datetime.now()
            print("Finished sending bytes in {} seconds".format(end - start))

        elif data.lower().strip() == "quit":
            break
    except IOError as e:
        print(e)
        print("IOError")
        break
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

try:
    camera.close()
    gp.output(8, gp.LOW)
    gp.output(10, gp.LOW)
    print "disconnected"
    client_sock.close()
    server_sock.close()
    print "all done"
    print("shutting down")
    os.system('sudo poweroff')
except:
    os.system('sudo poweroff')
