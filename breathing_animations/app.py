from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def serve_video():
    # Get the path to the animation.mp4 file
    video_path = os.path.join(os.path.dirname(__file__), 'animation.mp4')
    return send_file(video_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True) 