import cv2
import torch
from cvzone import FPS
from time import strftime
import smtplib
from email.mime.image import MIMEImage
import requests
import serial

def send_gmail(capture): #建立寄信函式
    mime = MIMEImage(capture)
    mime["Content-Type"] = "application/octet-stream" #設定檔案類型
    mime["Content-Disposition"] = f'attachment; filename="{filename}"'  # 附件的檔案名稱
    mime["Subject"] = "注意,有入侵者!"  # 撰寫郵件標題
    mime["From"] = "任"  # 撰寫你的暱稱或是信箱
    mime["To"] = "任"  # 撰寫寄件人稱呼
    mime["Cc"] = "tdac99@gmail.com, tdac99@gmail.com"  # 副本收件人
    msg = mime.as_string()  # 將msg將text轉成str
    smtp = smtplib.SMTP("smtp.gmail.com", 587)  # gmail的port
    smtp.ehlo()  # 申請身分
    smtp.starttls()  # 加密文件，避免私密信息被截取
    smtp.login("tdac99@gmail.com", "persytmkbqqtrhwq") #登入寄件人Gmail帳戶&應用程式密碼
    from_addr = "tdac99@gmail.com" #寄件人Gmail
    to_addr = ["tdac99@gmail.com"] #收件人Gmail
    status = smtp.sendmail(from_addr, to_addr, msg)
    if status == {}:
        print("郵件傳送成功!")
    else:
        print("郵件傳送失敗!")
    smtp.quit() #登出smtp

def send_line_notify(filename):
    url = "https://notify-api.line.me/api/notify"
    token = "dKLBZqd9sUycSxRpINVrlO4FCo7zYffZQE2towdcnUE"

    headers = {"Authorization": "Bearer " + token}

    payload = {"message": '有入侵者!'}
    files = {"imageFile": open(filename, "rb")}

    response = requests.post(url, headers=headers, data=payload, files=files)

stream_url = 'https://5671-140-127-33-219.jp.ngrok.io'  # 發送端的串流 URL
filename = f"person{strftime('%Y%m%d%H%M%S')}.png"
# 設定YOLOv5模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'G:\專題 A柱死角\exp_last\weights', force_reload=False)
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt', force_reload=False)
# 設定相機
cap = cv2.VideoCapture(stream_url)
# cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
fps_reader = FPS()
i = 0
ser = serial.Serial('COM3', 9600)
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
                    send_gmail(capture2)
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