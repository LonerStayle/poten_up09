
import sys 
import cv2 
import os
import csv
import mediapipe as mp 


# hand landmark 옵션
# (New) 저장할 파일명 넣기 file_path
# (New) 만약에 파일경로가 없으면 새로 만들기
# 웹캠
    # 카메라 감지
    # 좌우 반전
    # 손 그리기 준비
    # 손 감지
    # Hand Landmark 추출
        # 손 하나의 Hand Landmark 추출
        # 저장 데이터 만들기, 포인트 그리기
        # (New) 1누르면 rock, 2누르면 scissors, 3누르면 paper 그리고 데이터 저장
    # 화면 띄우기
    # ESC 누르면 종료
# 마무리


# mediapipe hand landmark 옵션
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 저장할 데이터 설정
file_path = "data/hand_data.csv"

if not os.path.exists(file_path):
    with open(file_path, "w") as file:
        writer = csv.writer(file)

# 카메라 설정
vcap = cv2.VideoCapture(0)

while True:
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다.")
        sys.exit()
    
    frame = cv2.flip(frame, 1)

    # BGR → RGB 변환
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        one_hand = results.multi_hand_landmarks[0]

        landmarks = []
        height, width, _ = frame.shape
        for landmark in one_hand.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
            point_x = int(landmark.x * width)
            point_y = int(landmark.y * height)
            cv2.circle(frame, (point_x, point_y), 5, (0,0,255), 2)

        # 키 입력은 여기서 하지 말고 ↓ 마지막에서 처리
        # 대신 여기서는 landmarks만 준비

    # 화면 띄우기
    cv2.imshow("webcam", frame)

    # 키 입력 처리
    key = cv2.waitKey(1) & 0xFF
    if key == ord("1") and results.multi_hand_landmarks:
        landmarks.append("rock")
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(landmarks)
        cv2.putText(frame, "Save Rock Data!", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    elif key == ord("2") and results.multi_hand_landmarks:
        landmarks.append("scissors")
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(landmarks)
        cv2.putText(frame, "Save Scissors Data!", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    elif key == ord("3") and results.multi_hand_landmarks:
        landmarks.append("paper")
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(landmarks)
        cv2.putText(frame, "Save Paper Data!", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    elif key == 27:  # ESC
        break
vcap.release()
cv2.destroyAllWindows()