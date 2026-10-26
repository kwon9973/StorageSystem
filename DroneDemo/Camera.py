import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
import cv2

cap = cv2.VideoCapture("rtsp://192.168.1.1:7070/webcam, cv2.CAP_FFMPEG")
while True:
    ok, frame = cap.read()
    if not ok:
        break
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()


