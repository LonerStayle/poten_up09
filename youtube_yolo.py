from ultralytics import YOLO

model = YOLO("yolo11n.pt")
youtube_url = "https://youtu.be/S5nsDT5oU90"
results = model(youtube_url, stream=True, show=True)


for res in results:
    print(res)