import cv2
import numpy as np
import socket
import pyautogui

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 22222
Message = "0"
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

lower_blue = np.array([100, 100, 60])
upper_blue = np.array([130, 255, 255])

screen_width, screen_height = pyautogui.size()
frame_width, frame_height = 400, 300
frame_x = screen_width - frame_width
frame_y = screen_height - frame_height

cap = cv2.VideoCapture(0)
cv2.namedWindow("Pong Input System - Developed By Sachira Madhushan", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Pong Input System - Developed By Sachira Madhushan", cv2.WND_PROP_TOPMOST, 1)
cv2.moveWindow("Pong Input System - Developed By Sachira Madhushan", frame_x, frame_y)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Mirror effect

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]

    areas = [cv2.contourArea(c) for c in contours]

    try:
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        M = cv2.moments(cnt)

        area = cv2.contourArea(cnt)

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        Message = str(-(cx - 320) * (3.7 / 320))

        clientSock.sendto(bytes(Message, 'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
        print("Sent:", Message)
    except:
        clientSock.sendto(bytes(Message, 'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
        pass

    cv2.putText(frame, str(str(cx) + "," + str(Message)), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Pong Input System - Developed By Sachira Madhushan", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
