import cv2
import numpy as np

# 1. 원본 이미지
img = cv2.imread("monster.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

# 2. 틀 불러오기
frame = cv2.imread("die_frame.jpg")

# 흰색 배경 제거
lower = np.array([240, 240, 240], dtype=np.uint8)
upper = np.array([255, 255, 255], dtype=np.uint8)
mask = cv2.inRange(frame, lower, upper)
mask_inv = cv2.bitwise_not(mask)
frame_fg = cv2.bitwise_and(frame, frame, mask=mask_inv)

# 3. 틀 크기 줄이기
scale = 0.2
fw, fh = int(gray.shape[1] * scale), int(gray.shape[0] * scale)
frame_resized = cv2.resize(frame_fg, (fw, fh))
mask_resized = cv2.resize(mask_inv, (fw, fh))

# 4. 원본에서 틀 영역 잘라내기 (중앙 배치)
x = (gray.shape[1] - fw) // 2 + 200
y = (gray.shape[0] - fh) // 2 - 500
roi = gray[y:y+fh, x:x+fw]

# 5. ROI를 틀 마스크로 오려내기
roi_cropped = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask_resized))

# 6. 틀 합성
roi_fg = cv2.bitwise_and(frame_resized, frame_resized, mask=mask_resized)
final = cv2.add(roi_cropped, roi_fg)

h, w = final.shape[:2]
cropped = final[52:h, 0:w]

cv2.imwrite("die_final.jpg", cropped)
cv2.imshow("Cropped", cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()

