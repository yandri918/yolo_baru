# YOLO Object Detection with Flask

This is a simple Flask application that uses the YOLOv8 model to perform object detection on uploaded images. The application allows users to upload an image, and it will return a list of detected objects (labels) in the image.

## Features

*   Upload images (PNG, JPG, JPEG) for object detection.
*   Utilizes the `yolov8n.pt` model for fast and efficient detection.
*   Displays the original image and a list of detected labels.

## Setup and Installation

Follow these steps to set up and run the application locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yandri918/yolo_baru.git
    cd yolo_baru
    ```

2.  **Create a virtual environment:**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv gemini_venv
    ```

3.  **Activate the virtual environment:**

    *   **Windows:**
        ```bash
        .\gemini_venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source gemini_venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```

    The application will typically run on `http://127.0.0.1:5000/`. Open this URL in your web browser.

## Usage

1.  Open your web browser and navigate to the application's URL (e.g., `http://127.0.0.1:5000/`).
2.  Click on "Choose File" to select an image from your local machine.
3.  Click "Deteksi Objek" to upload the image and see the detected labels.

## Project Structure

```
.
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── yolov8n.pt              # Pre-trained YOLOv8 nano model
├── Templates/
│   └── index.html          # HTML template for the web interface
└── .gitignore              # Specifies intentionally untracked files to ignore
```