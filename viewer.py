import cv2
import socket
import zlib
import base64
import numpy as np

server_ip = "0.0.0.0"  # Listen on all interfaces
server_port = 4000

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((server_ip, server_port))

print("Listening for video stream...")

while True:
    try:
        # Receive the compressed frame
        data, _ = s.recvfrom(65536)
        decompressed_data = zlib.decompress(data)
        frame_data = base64.b64decode(decompressed_data)
        
        # Convert to numpy array and decode to an image
        frame = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        
        # Display the frame
        cv2.imshow("Remote Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    except Exception as err:
        print("Error: ", err)
        break

# Clean up
s.close()
cv2.destroyAllWindows()
