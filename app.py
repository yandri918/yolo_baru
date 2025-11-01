import os
from flask import Flask, request, render_template, redirect, url_for
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import logging

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi path
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Pastikan direktori ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Muat model YOLOv8 (cukup sekali saat aplikasi dimulai)
# 'yolov8n.pt' adalah model terkecil dan tercepat.
# Anda bisa menggunakan model lain seperti 'yolov8s.pt', 'yolov8m.pt', dll.
try:
    model = YOLO('yolov8n.pt')
    logging.info("Model YOLOv8 berhasil dimuat.")
except Exception as e:
    logging.error(f"Gagal memuat model YOLOv8: {e}")
    # Anda bisa memilih untuk menghentikan aplikasi jika model gagal dimuat
    # exit() 

# Ekstensi file yang diizinkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Fungsi untuk memeriksa ekstensi file yang diizinkan."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Periksa apakah ada file dalam request
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        
        # Jika pengguna tidak memilih file, browser mengirim file kosong
        if file.filename == '':
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Amankan nama file untuk mencegah path traversal
            filename = secure_filename(file.filename)
            original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Simpan file asli
            file.save(original_filepath)
            
            # Lakukan prediksi dengan YOLO
            results = model.predict(source=original_filepath)
            
            # Ekstrak label dari hasil prediksi
            detected_labels = []
            if results:
                for result in results:
                    if result.boxes:
                        for box in result.boxes:
                            class_id = int(box.cls)
                            label = model.names[class_id]
                            detected_labels.append(label)
            
            # Hapus duplikat label jika perlu
            detected_labels = list(set(detected_labels))

            # Kirim label ke template untuk ditampilkan
            return render_template('index.html', 
                                   original_image=os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                   labels=detected_labels)

    # Untuk request GET, tampilkan halaman upload
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)