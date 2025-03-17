from flask import Flask, send_file, render_template, request, jsonify
import os
import logging
import json
from customized_breathing import draw_scene
from werkzeug.utils import secure_filename
import traceback
from PIL import Image

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configure upload folders
UPLOAD_FOLDER = 'uploads'
BALL_IMAGES_FOLDER = 'uploads/ball_images'
BACKGROUND_IMAGES_FOLDER = 'uploads/background_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BALL_IMAGES_FOLDER'] = BALL_IMAGES_FOLDER
app.config['BACKGROUND_IMAGES_FOLDER'] = BACKGROUND_IMAGES_FOLDER

# Create necessary directories
os.makedirs(BALL_IMAGES_FOLDER, exist_ok=True)
os.makedirs(BACKGROUND_IMAGES_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_png_with_transparency(input_path):
    try:
        if not os.path.exists(input_path):
            logging.error(f"Input file does not exist: {input_path}")
            return None

        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGBA
            if img.mode in ['RGB', 'L']:
                # For RGB or grayscale images, create transparency around non-white pixels
                if img.mode == 'L':
                    img = img.convert('RGB')
                
                # Convert to RGBA
                img = img.convert('RGBA')
                
                # Get image data
                data = img.getdata()
                
                # Create new data with transparency
                new_data = []
                for item in data:
                    # If pixel is white-ish, make it transparent
                    if item[0] > 240 and item[1] > 240 and item[2] > 240:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                
                img.putdata(new_data)
            elif img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Generate output path
            output_path = os.path.splitext(input_path)[0] + '.png'
            
            # Save as PNG with transparency
            try:
                img.save(output_path, 'PNG')
                
                # Verify the file was saved
                if os.path.exists(output_path):
                    logging.info(f"Successfully saved PNG file: {output_path}")
                    return output_path
                else:
                    logging.error(f"Failed to save PNG file: {output_path}")
                    return None
                    
            except Exception as e:
                logging.error(f"Error saving PNG file: {str(e)}")
                return None
                
    except Exception as e:
        logging.error(f"Error converting image to PNG: {str(e)}")
        return None

def save_uploaded_file(file, folder):
    if not file:
        logging.warning(f"No file provided for folder: {folder}")
        return None
        
    if not allowed_file(file.filename):
        logging.warning(f"Invalid file type: {file.filename}")
        return None
        
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config[folder], filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the file
        file.save(filepath)
        logging.info(f"Successfully saved file to: {filepath}")
        
        # Convert to PNG with transparency if it's a ball image
        if folder == 'BALL_IMAGES_FOLDER':
            png_path = convert_to_png_with_transparency(filepath)
            if png_path and os.path.exists(png_path):
                logging.info(f"Successfully converted and saved PNG file: {png_path}")
                # Only remove the original if it's different and the conversion was successful
                if filepath != png_path and os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                        logging.info(f"Removed original file: {filepath}")
                    except Exception as e:
                        logging.warning(f"Could not remove original file {filepath}: {str(e)}")
                filepath = png_path
            else:
                logging.error("Failed to convert image to PNG")
                return None
        
        # Final verification
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            logging.info(f"Final verification: File exists at {filepath}, size: {file_size} bytes")
            return filepath
        else:
            logging.error(f"Final verification failed: File does not exist at {filepath}")
            return None
            
    except Exception as e:
        logging.error(f"Error saving file: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        return None

def generate_animation(patterns, customization):
    logging.info("Generating animation with patterns: %s", patterns)
    
    try:
        # Handle image uploads
        background_image = None
        ball_image = None
        
        # Check if files were actually uploaded
        if 'backgroundImage' in request.files:
            background_file = request.files['backgroundImage']
            if background_file and background_file.filename:
                logging.info(f"Processing background image: {background_file.filename}")
                background_image = save_uploaded_file(background_file, 'BACKGROUND_IMAGES_FOLDER')
                if not background_image:
                    raise ValueError("Failed to save background image")
                logging.info(f"Background image saved to: {background_image}")
        
        if 'ballImage' in request.files:
            ball_file = request.files['ballImage']
            if ball_file and ball_file.filename:
                logging.info(f"Processing ball image: {ball_file.filename}")
                ball_image = save_uploaded_file(ball_file, 'BALL_IMAGES_FOLDER')
                if not ball_image:
                    raise ValueError("Failed to save ball image")
                logging.info(f"Ball image saved to: {ball_image}")
        
        # Generate animation with custom parameters
        success = draw_scene(
            patterns=patterns,
            line_color=customization.get('lineColor', '#0000ff'),
            text_color=customization.get('textColor', '#000000'),
            background_image=background_image,
            ball_image=ball_image
        )
        
        if not success:
            raise Exception("Failed to generate animation")
        
        logging.info("Animation generated successfully")
        return True
    except Exception as e:
        error_message = str(e)
        logging.error("Error generating animation: %s", error_message)
        logging.error("Traceback: %s", traceback.format_exc())
        raise Exception(f"Error generating animation: {error_message}")

@app.route('/')
def index():
    logging.debug("Serving index page")
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Log the request data
        logging.info("Received generate request")
        logging.info(f"Files in request: {list(request.files.keys())}")
        logging.info(f"Form data: {list(request.form.keys())}")
        
        patterns = json.loads(request.form['patterns'])
        customization = json.loads(request.form['customization'])
        
        generate_animation(patterns, customization)
        return jsonify({"status": "success"})
    except Exception as e:
        error_message = str(e)
        logging.error("Error in /generate endpoint: %s", error_message)
        logging.error("Traceback: %s", traceback.format_exc())
        return jsonify({"status": "error", "message": error_message}), 500

@app.route('/video')
def video():
    video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'animation.mp4')
    logging.debug(f"Attempting to serve video from: {video_path}")
    if not os.path.exists(video_path):
        return jsonify({"status": "error", "message": "Animation file not found"}), 404
    return send_file(video_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 