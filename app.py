import os
import cv2
from flask import Flask, request, render_template, redirect, url_for, Response
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import logging

# Inisialisasi aplikasi Flask
app = Flask(__name__, template_folder='templates')

# Konfigurasi path
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan direktori ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Muat model YOLOv8
try:
    model = YOLO('yolov8n.pt')
    logging.info("Model YOLOv8 berhasil dimuat.")
except Exception as e:
    logging.error(f"Gagal memuat model YOLOv8: {e}")

# Ekstensi file yang diizinkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_frames(source):
    cap = cv2.VideoCapture(source)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)
        annotated_frame = results[0].plot()

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            file_ext = filename.rsplit('.', 1)[1].lower()
            if file_ext in ['png', 'jpg', 'jpeg']:
                results = model.predict(source=filepath)
                detected_labels = []
                if results:
                    for result in results:
                        if result.boxes:
                            for box in result.boxes:
                                class_id = int(box.cls)
                                label = model.names[class_id]
                                detected_labels.append(label)
                
                detected_labels = list(set(detected_labels))

                return render_template('index.html', 
                                       original_image=os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                       labels=detected_labels)
            elif file_ext in ['mp4', 'avi', 'mov']:
                return render_template('video.html', video_file=filename)

    return render_template('index.html')

@app.route('/video_feed/<filename>')
def video_feed(filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return Response(generate_frames(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cctv', methods=['POST'])
def cctv():
    cctv_url = request.form['cctv_url']
    return render_template('cctv.html', cctv_url=cctv_url)

@app.route('/cctv_feed')
def cctv_feed():
    cctv_url = request.args.get('url')
    return Response(generate_frames(cctv_url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/local_camera')
def local_camera():
    return render_template('local_camera.html')

@app.route('/local_camera_feed')
def local_camera_feed():
    return Response(generate_frames(0), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)