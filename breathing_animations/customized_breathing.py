import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.transforms import Affine2D
from scipy.ndimage import rotate

# Animation timing parameters (in seconds)
ANIMATION_DURATION = 8.0  # Total duration of one breathing cycle
FRAME_RATE = 25  # Frames per second
TOTAL_FRAMES = int(ANIMATION_DURATION * FRAME_RATE)  # Calculate total frames based on duration
FRAME_INTERVAL = int(1000 / FRAME_RATE)  # Interval between frames in milliseconds

# Segment timing parameters
TIME_TO_FIRST = 4.0  # Time to reach first point
TIME_TO_MID = 2.0    # Time to reach middle point
TIME_TO_END = 3.0    # Time to reach end point
TIME_TO_NEW_END = 2.0  # Time to reach new end point

# Calculate absolute times for each point
TIME_TO_MID_ABS = TIME_TO_FIRST + TIME_TO_MID
TIME_TO_END_ABS = TIME_TO_MID_ABS + TIME_TO_END
TIME_TO_NEW_END_ABS = TIME_TO_END_ABS + TIME_TO_NEW_END

def draw_scene():
    fig, ax = plt.subplots(figsize=(5.4, 9.6), dpi=200)  # Aspect ratio 1080x1920
    ax.set_xlim(-5, 5)
    ax.set_ylim(-8.888, 8.888)
    ax.set_aspect('equal')

    # Load the image from the images folder
    try:
        image = imread('images/ball.png')  # Image is now loaded from the images directory
        print(f"Image loaded successfully. Shape: {image.shape}")
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Create an OffsetImage for the ball
    imagebox = OffsetImage(image, zoom=0.2)  # Adjust zoom to scale the image

    # Initial position of the ball (x=0, y=0)
    ab = AnnotationBbox(imagebox, (0, 0), frameon=False, pad=0.0)
    ax.add_artist(ab)

    # Line initialization
    line, = ax.plot([-15, 0, 5, 15], [0, 0, 4, 4], 'b-', linewidth=2)

    # Add timer text
    timer_text = ax.text(0, 8, '4s', 
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=24,
                        fontweight='bold',
                        color='black')

    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    # Animation function
    def update(frame):
        # Convert frame number to time in seconds
        t = frame / FRAME_RATE
        
        # Calculate countdown based on current position
        if t < TIME_TO_FIRST:
            # First segment: count down from 4 to 1
            countdown = min(4, int(TIME_TO_FIRST - t) + 1)
            timer_text.set_text(f'{countdown}s')
        elif t < TIME_TO_END_ABS:
            # Second segment: count down from 4 to 1
            countdown = min(4, int(4 - (t - TIME_TO_FIRST)) + 1)
            timer_text.set_text(f'{countdown}s')
        elif t < TIME_TO_NEW_END_ABS:
            # Final segment: count down from 2 to 1
            countdown = min(4, int(TIME_TO_NEW_END - (t - TIME_TO_END_ABS)) + 1)
            timer_text.set_text(f'{countdown}s')
        else:
            timer_text.set_text('1s')
        
        # Define moving points
        start_x = -15 - 10 * (t / ANIMATION_DURATION)
        mid_x = 0 - 10 * (t / ANIMATION_DURATION)
        end_x = 5 - 10 * (t / ANIMATION_DURATION)
        new_end_x = 15 - 10 * (t / ANIMATION_DURATION)

        # Calculate the y-position of the line at x=0
        if mid_x < 0 and end_x > 0:  # Rising phase (mid_x to end_x)
            slope = (4 - 0) / (end_x - mid_x)
            y_at_zero = slope * (0 - mid_x)
        elif end_x <= 0 and new_end_x > 0:  # Flat phase at y=4 (end_x to new_end_x)
            y_at_zero = 4
        elif mid_x >= 0:  # Flat phase at y=0 (start_x to mid_x)
            y_at_zero = 0
        elif new_end_x <= 0:  # Flat phase at y=4 continues
            y_at_zero = 4
        else:
            y_at_zero = 0

        # Ensure y_at_zero stays within bounds
        y_at_zero = max(0, min(4, y_at_zero))

        # Update line position
        line.set_data([start_x, mid_x, end_x, new_end_x], [0, 0, 4, 4])

        # Update ball position
        ab.xybox = (0, y_at_zero)

        # Calculate rotation angle (counterclockwise spin)
        angle = -frame * (360 / TOTAL_FRAMES)  # Full rotation over total frames
        # Rotate the image directly
        rotated_image = rotate(image, angle, reshape=False)
        imagebox.image.set_array(rotated_image)

        return line, ab, timer_text

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=FRAME_INTERVAL, blit=True)

    # Save animation as MP4
    ani.save("animation.mp4", writer="ffmpeg", fps=FRAME_RATE)

    # Only show the plot if this script is run directly
    if __name__ == '__main__':
        plt.show()

if __name__ == '__main__':
    draw_scene()