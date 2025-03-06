import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.transforms import Affine2D

def draw_scene():
    fig, ax = plt.subplots(figsize=(5.4, 9.6), dpi=200)  # Aspect ratio 1080x1920
    ax.set_xlim(-5, 5)
    ax.set_ylim(-8.888, 8.888)
    ax.set_aspect('equal')

    # Load the image from the images folder
    image = imread('images/ball.png')  # Image is now loaded from the images directory

    # Create an OffsetImage for the ball
    imagebox = OffsetImage(image, zoom=0.2)  # Adjust zoom to scale the image

    # Initial position of the ball (x=0, y=0)
    ab = AnnotationBbox(imagebox, (0, 0), frameon=False, pad=0.0)
    ax.add_artist(ab)

    # Line initialization: new segment at y=4 (slope = 0)
    line, = ax.plot([-15, 0, 5, 15], [0, 0, 4, 4], 'b-', linewidth=2)

    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    # Animation function
    def update(frame):
        t = frame / 100  # Normalize time (0 to 1 in 100 frames)

        # Define moving points
        start_x = -15 - 10 * t
        mid_x = 0 - 10 * t
        end_x = 5 - 10 * t
        new_end_x = 15 - 10 * t

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

        # Update ball position
        ab.xybox = (0, y_at_zero)

        # Calculate rotation angle (slow spin synced with line movement)
        angle = (frame / 100) * 360  # Full rotation over 100 frames
        # Create a new transform: base data transform + rotation around (0, y_at_zero)
        transform = Affine2D().rotate_deg_around(0, y_at_zero, angle) + plt.gca().transData
        imagebox.set_transform(transform)

        # Update line position
        line.set_data([start_x, mid_x, end_x, new_end_x], [0, 0, 4, 4])
        return line, ab

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=100, interval=40, blit=True)

    # Save animation as MP4
    ani.save("animation.mp4", writer="ffmpeg", fps=25)

    plt.show()

draw_scene()