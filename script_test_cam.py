from flask import Flask, Response
import picamera

app = Flask(__name__)

def generate_frames():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        # Start the preview
        camera.start_preview()
        # Allow the camera to warm up
        time.sleep(2)

        # Continuously yield frames
        for frame in camera.capture_continuous(format='bgr', use_video_port=True):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Vous pouvez changer le port si nécessaire
