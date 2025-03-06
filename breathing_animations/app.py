from flask import Flask, send_file, render_template
import os
import logging
from customized_breathing import draw_scene

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def generate_animation():
    logging.info("Generating animation...")
    draw_scene()
    logging.info("Animation generated successfully")

@app.route('/')
def index():
    logging.debug("Serving index page")
    return render_template('index.html')

@app.route('/video')
def video():
    video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'animation.mp4')
    logging.debug(f"Attempting to serve video from: {video_path}")
    return send_file(video_path, mimetype='video/mp4')

if __name__ == '__main__':
    # Generate animation before starting the server
    generate_animation()
    app.run(host='0.0.0.0', port=5001, debug=True) 