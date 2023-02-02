from flask import Flask, render_template_string, Response
from io import BufferedIOBase
from threading import Condition
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder, Quality
from picamera2.outputs import FileOutput
from libcamera import controls, Transform

template = '''
    <!DOCTYPE html>
    <html lang="en">
        <body>
            <img src="{{ url_for('video_stream') }}" width="100%">
        </body>
    </html>
    '''

app = Flask(__name__)


class StreamingOutput(BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


output = StreamingOutput()


def gen_frames():
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/", methods=['GET'])
def get_stream_html():
    return render_template_string(template)


@app.route('/api/stream')
def video_stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    cam = Picamera2()
    config = cam.create_video_configuration(
        {'size': (1920, 1080), 'format': 'XBGR8888'},
        transform=Transform(vflip=1),
        controls={'NoiseReductionMode': controls.draft.NoiseReductionModeEnum.HighQuality, 'Sharpness': 1.5}
    )
    cam.configure(config)
    cam.start_recording(JpegEncoder(), FileOutput(output), Quality.VERY_HIGH)

    app.run(host='0.0.0.0')

    cam.stop()
