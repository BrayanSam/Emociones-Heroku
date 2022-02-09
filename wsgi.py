from flask import jsonify, render_template, Response
from app.main import app
import cv2
import os

"Iniciamos CAMARA"
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml")

def generate():
    while(True):
        "Capturamos Video Frame a Frame"
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y),(x + w, y+h),(0, 255, 0), 2)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')

@app.route("/tomar_foto_guardar")
def guardar_foto():
    nombre_foto ="Rostro.jpg"
    ok, frame = cap.read()
    if ok:
        cv2.imwrite(os.path.join('./app/static/images/Rostro.jpg'), frame)
    return jsonify({
        "ok": ok,
        "nombre_foto": nombre_foto,
    })

def pagina_no_encontrada(error):
    return render_template('404.html'), 404
    #return redirect(url_for('index'))

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
            mimetype="multipart/x-mixed-replace; boundary=frame")
 
if __name__ == "__main__":
        app.register_error_handler(404, pagina_no_encontrada)
        app.run()