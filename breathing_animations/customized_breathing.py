import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive 'Agg'
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from scipy.ndimage import rotate
import math
import warnings
import colorsys
import os
from PIL import Image
import logging

# Suppress matplotlib warnings about clipping
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib.image")

# Animation parameters
FRAME_RATE = 25
FRAME_INTERVAL = int(1000 / FRAME_RATE)
MAX_SCREEN_HEIGHT = 5

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple normalized to [0,1] range"""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return tuple(x/255.0 for x in rgb)  # Normalize to [0,1] range

def resize_image(image, target_width, target_height=None):
    """Resize image while maintaining aspect ratio and transparency"""
    try:
        # If image is a path, load it
        if isinstance(image, str):
            with Image.open(image) as img:
                # Convert to RGBA if necessary
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Calculate new dimensions
                width, height = img.size
                aspect_ratio = width / height
                
                if target_height is None:
                    new_width = target_width
                    new_height = int(target_width / aspect_ratio)
                else:
                    new_width = target_width
                    new_height = target_height
                
                # Resize image using LANCZOS resampling to maintain quality
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert to numpy array and normalize
                img_array = np.array(img) / 255.0
                return img_array
        
        # If image is already a numpy array
        elif isinstance(image, np.ndarray):
            if len(image.shape) not in [3, 4]:
                raise ValueError(f"Invalid image shape: {image.shape}")
            
            height, width = image.shape[:2]
            aspect_ratio = width / height
            
            if target_height is None:
                new_width = target_width
                new_height = int(target_width / aspect_ratio)
            else:
                new_width = target_width
                new_height = target_height
            
            # Convert to PIL Image for resizing
            if image.shape[-1] == 4:  # RGBA
                img = Image.fromarray((image * 255).astype('uint8'), 'RGBA')
            else:  # RGB
                img = Image.fromarray((image * 255).astype('uint8'), 'RGB')
                img = img.convert('RGBA')
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            return np.array(img) / 255.0
        
        else:
            raise ValueError("Input must be either a file path or numpy array")
            
    except Exception as e:
        logging.error(f"Error in resize_image: {str(e)}")
        return None

def create_breathing_steps(pattern):
    return [
        {"name": "inhale", "duration": pattern["inhaleDuration"]},
        {"name": "hold", "duration": pattern["firstHoldDuration"]},
        {"name": "exhale", "duration": pattern["exhaleDuration"]},
        {"name": "hold", "duration": pattern["secondHoldDuration"]},
    ]

def assign_y_coordinates(steps, max_screen_height):
    max_duration = max(step["duration"] for step in steps if step["duration"] > 0)
    height_scale = max_screen_height / max_duration
    for i, step in enumerate(steps):
        if step["name"] == "inhale":
            step["y_start"] = 0
            step["y_end"] = min(step["duration"] * height_scale, max_screen_height)
        elif step["name"] == "exhale":
            step["y_start"] = steps[i-1]["y_end"] if i > 0 else max_screen_height
            step["y_end"] = 0
        elif step["name"] == "hold":
            step["y_start"] = steps[i-1]["y_end"] if i > 0 else 0
            step["y_end"] = step["y_start"]
    return steps

def generate_line_coordinates(steps, cycles):
    x_line = []
    y_line = []
    current_x = 0
    for _ in range(cycles):
        for step in steps:
            if step["duration"] > 0:
                x_line.append(current_x)
                y_line.append(step["y_start"])
                current_x += step["duration"]
                x_line.append(current_x)
                y_line.append(step["y_end"])
    return np.array(x_line), y_line

def get_y_at_time(t, steps, cycle_duration):
    t_cycle = t % cycle_duration
    current_time = 0
    for step in steps:
        step_end = current_time + step["duration"]
        if current_time <= t_cycle < step_end:
            if step["duration"] > 0:
                fraction = (t_cycle - current_time) / step["duration"]
                return step["y_start"] + (step["y_end"] - step["y_start"]) * fraction
            return step["y_start"]
        current_time = step_end
    return steps[-1]["y_end"]

def draw_scene(patterns, line_color='#0000ff', text_color='#000000', background_image=None, ball_image=None):
    try:
        # Set up the figure and axis
        dpi = 200
        fig_width = 1080 / dpi
        fig_height = 1920 / dpi
        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)
        
        # Calculate dimensions for 16:9 aspect ratio
        TOTAL_WIDTH = sum(sum(step["duration"] for step in create_breathing_steps(pattern)) * pattern["numReps"] 
                         for pattern in patterns)
        BALL_X_CENTER = TOTAL_WIDTH / 2
        x_half_width = 5.4 / 2
        
        # Set up the plot
        ax.set_xlim(BALL_X_CENTER - x_half_width, BALL_X_CENTER + x_half_width)
        ax.set_ylim(-1, 8.6)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        
        # Load and display background image if provided
        if background_image and os.path.exists(background_image):
            try:
                bg_img = resize_image(background_image, 1080)
                if bg_img is not None:
                    ax.imshow(bg_img, extent=[BALL_X_CENTER - x_half_width, BALL_X_CENTER + x_half_width, -1, 8.6], 
                             aspect='auto', zorder=0)
                    logging.info("Background image loaded successfully")
                else:
                    logging.error("Failed to resize background image")
            except Exception as e:
                logging.error(f"Error loading background image: {str(e)}")
        
        # Load ball image
        try:
            if ball_image and os.path.exists(ball_image):
                logging.info(f"Loading ball image from: {ball_image}")
                ball_img = resize_image(ball_image, 200, 200)
                if ball_img is None:
                    raise ValueError("Failed to resize ball image")
                logging.info(f"Successfully loaded ball image: {ball_image}")
            else:
                logging.error(f"Ball image not found at: {ball_image}")
                return False
        except Exception as e:
            logging.error(f"Error loading ball image: {str(e)}")
            return False
        
        # Create the ball image box with transparency
        imagebox = OffsetImage(ball_img, zoom=0.2)
        imagebox.image.axes = ax
        ab = AnnotationBbox(imagebox, (BALL_X_CENTER, 0), frameon=False, pad=0.0)
        ax.add_artist(ab)
        
        # Generate line coordinates
        all_steps = []
        for pattern in patterns:
            steps = create_breathing_steps(pattern)
            steps = assign_y_coordinates(steps, MAX_SCREEN_HEIGHT)
            for _ in range(pattern["numReps"]):
                all_steps.extend(steps)
        
        x_line_base, y_line = generate_line_coordinates(all_steps, 1)
        line_rgb = hex_to_rgb(line_color)
        text_rgb = hex_to_rgb(text_color)
        
        line, = ax.plot(x_line_base, y_line, color=line_rgb, linewidth=2)
        timer_text = ax.text(BALL_X_CENTER, MAX_SCREEN_HEIGHT + 0.5, '3s',
                           horizontalalignment='center',
                           verticalalignment='center',
                           fontsize=12,
                           fontweight='bold',
                           color=text_rgb)
        
        TOTAL_FRAMES = int(TOTAL_WIDTH * FRAME_RATE)
        
        def update(frame):
            t = frame / FRAME_RATE
            y_at_t = get_y_at_time(t, all_steps, TOTAL_WIDTH)
            ab.xybox = (BALL_X_CENTER, y_at_t)
            
            # Rotate the ball image
            angle = -(frame * (360 / (TOTAL_FRAMES / 4)))
            img_rotated = rotate(ball_img, angle, reshape=False)
            
            # Ensure proper alpha channel handling
            if img_rotated.shape[-1] == 4:
                # Clip values to valid range while preserving alpha channel
                rgb = np.clip(img_rotated[..., :3], 0, 1)
                alpha = img_rotated[..., 3]
                img_rotated = np.dstack((rgb, alpha))
            
            imagebox.image.set_array(img_rotated)
            
            # Update line position
            shift = BALL_X_CENTER - (t % TOTAL_WIDTH)
            x_line_shifted = x_line_base + shift
            line.set_data(x_line_shifted, y_line)
            
            # Update countdown timer
            current_time = 0
            for step in all_steps:
                step_end = current_time + step["duration"]
                if current_time <= t < step_end:
                    remaining_time = step_end - t
                    countdown = math.ceil(remaining_time) if remaining_time > 0 else 1
                    timer_text.set_text(f'{countdown}s')
                    break
                current_time = step_end
            
            return line, ab, timer_text
        
        ani = animation.FuncAnimation(fig, update, frames=TOTAL_FRAMES,
                                    interval=FRAME_INTERVAL, blit=True)
        
        ani.save("animation.mp4", writer="ffmpeg", fps=FRAME_RATE)
        plt.close(fig)
        logging.info("Animation saved as 'animation.mp4'")
        return True
        
    except Exception as e:
        logging.error(f"Error generating animation: {e}")
        if 'fig' in locals():
            plt.close(fig)
        return False

if __name__ == '__main__':
    # Example usage
    patterns = [
        {
            "name": "Box Breathing",
            "numReps": 2,
            "inhaleDuration": 4,
            "firstHoldDuration": 4,
            "exhaleDuration": 4,
            "secondHoldDuration": 4
        }
    ]
    draw_scene(patterns)