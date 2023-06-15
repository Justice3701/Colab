import cv2

stream_url = 'http://172.20.10.4:5000/video_feed'  # 發送端的串流 URL

# 建立影像串流物件
stream = cv2.VideoCapture(stream_url)

while True:
    ret, frame = stream.read()  # 讀取串流中的影像
    if not ret:
        break

    cv2.imshow('Received Video', frame)  # 顯示接收到的影像
    if cv2.waitKey(1) == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()
