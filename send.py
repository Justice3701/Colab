import cv2
from flask import Flask, Response

app = Flask(__name__)


def generate_frames():
    while True:
        success, frame = camera.read()  # 擷取當前影像
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)  # 將影像轉換為 JPEG 格式
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 傳送影像串流
        if input == '.':
            break


@app.route('/')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


camera = cv2.VideoCapture(0)  # 開啟攝像頭

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
