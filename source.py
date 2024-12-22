import cv2
import time
import socket
import zlib
import base64

viewer_ip = "192.168.xx.xx"
viewer_port = 4000

# Create socket for sending data
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

# Initialize USB camera
camera = cv2.VideoCapture(0)  # '0' is typically the default USB camera

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 30)

time.sleep(0.1)  # Allow camera to warm up
msg = True

while True:
    try:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Display the frame locally (uncomment this line if you want to view frame locally)

        # cv2.imshow("Source", frame)
        
        if msg:
            print("Video Stream Started")
            msg = False
        
        key = cv2.waitKey(1) & 0xFF
        
        # Encode and compress frame
        ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        pre_compress = base64.b64encode(buffer)
        vid_frame = zlib.compress(pre_compress)
        
        # Send the compressed frame over UDP
        s.sendto(vid_frame, (viewer_ip, viewer_port))
        
        # Break loop on 'q' key press
        if key == ord("q"):
            break

    except Exception as err:
        print("Error: ", err)
        break

# Release resources
camera.release()
cv2.destroyAllWindows()
