import sys 
import cv2 
import mediapipe as mp 

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

vcap = cv2.VideoCapture(0)

while True:
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다.")
        sys.exit()
    
    # 좌우반전
    frame = cv2.flip(frame, 1)

    ###### Hands Landmark 추출 ######
    # 손 그리기 설정
    frame.flags.writeable = True 

    # 손 감지
    results = hands.process(frame)

    # 추출 및 그리기 
    if results.multi_hand_landmarks:
        # print(len(results.multi_hand_landmarks))
        for hand_landmarks in results.multi_hand_landmarks:
            # print(len(hand_landmarks.landmark))  
            # 자동 그리기 
            # mp_drawing.draw_landmarks(
            #     frame, 
            #     hand_landmarks,
            #     mp_hands.HAND_CONNECTIONS,
            #     mp_drawing_styles.get_default_hand_landmarks_style(),
            #     mp_drawing_styles.get_default_hand_connections_style()
            # )
            # 좌표 데이터 리스트로 만들기,  직접 그리기
            landmarks = []
            height, width, _ = frame.shape 
            for landmark in hand_landmarks.landmark:
                # print(landmark.x, landmark.y)
                ## 좌표 데이터 리스트로 만들기
                landmarks.append([landmark.x, landmark.y, landmark.z])
                ## 좌표 데이터 그리기
                point_x = int(landmark.x * width)
                point_y = int(landmark.y * height)

                cv2.circle(frame, (point_x, point_y), 5, (0,0,255), 2)
    ################################

    # 화면 띄우기
    cv2.imshow("webcam", frame)

    # 꺼지는 조건
    key = cv2.waitKey(1) # ASCII 코드
    if key == ord("1"):
        print("1을 눌렀습니다.")
    elif key == ord("2"):
        print("2를 눌렀습니다.")
    elif key == ord("3"):
        print("3을 눌렀습니다.")

    if key == 27: # ESC 
        break

vcap.release()
cv2.destroyAllWindows()