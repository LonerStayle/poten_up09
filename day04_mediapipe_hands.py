import sys
import cv2

vcap = cv2.VideoCapture(0)

while True:
    ret, frame = vcap.read()   
    if not ret:
        print("카메라가 작동하지 않습니다.")
        sys.exit()
    
    #좌우 반전
    flipped_frame = cv2.flip(frame,1)
    contrast_frame = 255 - flipped_frame
    
    cv2.imshow("webcam",contrast_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

vcap.release()
cv2.destroyAllWindows()
