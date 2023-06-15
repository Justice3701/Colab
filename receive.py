import cv2
import torch
import requests
import serial


def send_line_notify(filename):
    url = "https://notify-api.line.me/api/notify"
    token = "輸入申請line Notify的金鑰"

    headers = {"Authorization": "Bearer " + token}

    payload = {"message": '有入侵者!'}
    files = {"imageFile": open(filename, "rb")}

    response = requests.post(url, headers=headers, data=payload, files=files)

stream_url = '輸入發送端使用Ngrok轉譯的url'  # 發送端的串流 URL
filename = f"person{strftime('%Y%m%d%H%M%S')}.png"
# 設定YOLOv5模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path='輸入best.pt的路徑', force_reload=True)
# 設定相機
cap = cv2.VideoCapture(stream_url)
i = 0
ser = serial.Serial('COM3', 9600) #設定Arduino的COM連接埠
while True:
    # 讀取影像
    success, frame = cap.read()
    # 將影像轉為RGB格式
    dst = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 偵測物件
    results = model(dst)
    # 取得偵測框和類別標籤
    boxes = results.xyxy[0]
    labels_p = results.names[0]
    labels_c = results.names[1]
    labels_m = results.names[2]
    labels = [labels_p, labels_c, labels_m]
    # 找出人臉框和對應的距離
    for box in boxes:
        x1, y1, x2, y2, confidence, class1 = box.tolist()
        if confidence > 0.8:
            if int(class1) == 0:
                ser.write(b"A\n")
                if i % 25 == 0:
                    capture = dst[int(y1):int(y2), int(x1):int(x2)]
                    capture = cv2.cvtColor(capture,cv2.COLOR_BGR2RGB)
                    ret, buffer = cv2.imencode('.png', capture)
                    capture2 = buffer.tobytes()
                    cv2.imwrite(filename, capture)
                    send_line_notify(filename)
                    label=labels[0]
                    cv2.rectangle(dst, (int(x1), int(y1)), (int(x2), int(y2)), (255, 140, 0), 5)
                    cv2.putText(dst, label + " " + str(round(confidence, 2)), (int(x1), int(y1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 140, 0), 3)
    ser.write(b"C\n")
    frame2 = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    fps, frame2 = fps_reader.update(frame2, pos=(10, 20), color=(0, 255, 0), scale=1, thickness=1)
    # 顯示影像
    cv2.imshow('Result', frame2)
    # 按下 'q' 鍵退出迴圈
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i+=1
# 釋放攝像頭並關閉視窗
cap.release()
cv2.destroyAllWindows()
