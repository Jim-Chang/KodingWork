import cv2
from flask import Flask, render_template, Response
from io import BytesIO
from PIL import Image


app = Flask(
    __name__,
    static_url_path='', 
    static_folder='./',
    template_folder='./',
)

cap = cv2.VideoCapture(0)


def resize_img_2_bytes(image, resize_factor, quality):
    bytes_io = BytesIO()
    img = Image.fromarray(image)

    w, h = img.size
    img.thumbnail((int(w * resize_factor), int(h * resize_factor)))
    img.save(bytes_io, 'jpeg', quality=quality)

    return bytes_io.getvalue()


def get_image_bytes():
    success, img = cap.read()
    if success:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_bytes = resize_img_2_bytes(img, resize_factor=0.5, quality=30)
        return img_bytes

    return None


def gen_frames():
    while True:
        img_bytes = get_image_bytes()
        if img_bytes:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')


@app.route("/", methods=['GET'])
def get_stream_html():
    return render_template('stream.html')


@app.route('/api/stream')
def video_stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0')