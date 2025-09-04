# uv add mediapipe
import sys 
import cv2 
import mediapipe as mp 

# mediapipe의 Hand Landmark를 추출을 위한 옵션
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode = False, 
    max_num_hands = 2,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

# 웹캠 연결
vcap = cv2.VideoCapture(0)

while True:
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다.")
        sys.exit()

    # 좌우 반전
    frame = cv2.flip(frame, 1)
    
    ###### Hands Landmark 설정하기 ######
    # 손 그리기 설정
    frame.flags.writeable = True

    # 손 감지하기 
    results = hands.process(frame)

    # 그리기 
    if results.multi_hand_landmarks:
        print(len(results.multi_hand_landmarks)) # 손이 몇 개 탐지 되는가?
        for hand_landmarks in results.multi_hand_landmarks:
            # print(len(hand_landmarks.landmark)) # 한 개의 손마다 좌표가 몇 개 나오는가? 21개
            # print(hand_landmarks.landmark)

            height, width, _ = frame.shape # (h, w, c)

            for landmark in hand_landmarks.landmark:
                print(landmark.x, landmark.y)

                point_x = int(landmark.x * width)
                point_y = int(landmark.y * height)

                cv2.circle(frame, (point_x, point_y), 5, (0,0,255), 2)

            ## 자동그리기 
            # mp_drawing.draw_landmarks(
            #     frame, 
            #     hand_landmarks,
            #     mp_hands.HAND_CONNECTIONS,
            #     mp_drawing_styles.get_default_hand_landmarks_style(),
            #     mp_drawing_styles.get_default_hand_connections_style()
            # )
    ####################################

    # 화면 띄우기
    cv2.imshow("webcam", frame)

    # 꺼지는 조건 
    key = cv2.waitKey(1)
    if key == 27:
        break 

vcap.release()
cv2.destroyAllWindows()