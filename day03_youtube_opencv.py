import yt_dlp
import cv2
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

youtube_url = "https://www.youtube.com/watch?v=kUnZ58TwS-A&t=1646s"

ydl_opts = {
    "format": "best[ext=mp4][protocol=https]/best",
    "quite": True,
    "no_warnings": True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(youtube_url, download=False)
    stream_url = info_dict["url"]

vcap = cv2.VideoCapture(stream_url)

while True:
    if not vcap.isOpened():
        print("비디오를 열 수 없습니다.")
        break

    ret, frame = vcap.read()
    if not ret:
        print("비디오 프레임을 읽어올 수 없습니다.")
        break

    results = model(frame, conf = 0.7)
    result = results[0]
    boxes = result.boxes
    print(boxes.data)

    cnt = 0
    for x1, y1, x2, y2, conf, idx in boxes.data:
        if idx > 0:
            continue

        cnt += 1
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
    
    # 프레임, 텍스트, 위치, 폰트, 크기, 색상, 두께
    cnt_text = f"People Count: {cnt}"
    cv2.putText(frame, cnt_text, (0,30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0,255,255),2)
    
    # model.predict(frame)
    cv2.imshow("Youtube Vidio", frame)

    # 종료 조건
    key = cv2.waitKey(1)
    if key == 27:
        break


vcap.release()
cv2.destroyAllWindows()
