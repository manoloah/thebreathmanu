# Breathing Animation Generator

A Flask application that generates customized breathing animations with user-defined patterns and visual elements.

## Prerequisites

- Python 3.13 or higher
- Homebrew (for macOS users)
- Git

## System Dependencies (macOS)

Before installing Python dependencies, you need to install some system-level dependencies:

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required system dependencies
brew install gfortran openblas libomp pkg-config
```

## Quick Start

### Option 1: Using the Setup Script (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd breathing_animations/customized_breathing_exercises
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

3. Start the application:
```bash
./run.sh
```

### Option 2: Manual Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Development

### Virtual Environment Management

To make it easier to work with the virtual environment, you can add these aliases to your shell configuration file (e.g., `~/.zshrc` or `~/.bashrc`):

```bash
# Add these lines to your shell config file
alias breathe-env="source /path/to/breathing_animations/customized_breathing_exercises/venv/bin/activate"
alias breathe-run="cd /path/to/breathing_animations/customized_breathing_exercises && python app.py"
```

After adding these aliases, you can simply run:
```bash
breathe-env  # Activates the virtual environment
breathe-run  # Runs the application
```

### Directory Structure

```
customized_breathing_exercises/
├── app.py                 # Main Flask application
├── customized_breathing.py # Animation generation logic
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
├── run.sh                # Run script
├── venv/                 # Virtual environment
├── uploads/              # User uploads directory
│   ├── ball_images/      # Custom ball images
│   └── background_images/ # Custom background images
└── templates/            # HTML templates
```

## Usage

1. Open your web browser and navigate to `http://localhost:5001`
2. Upload custom images (optional)
3. Configure breathing patterns and visual settings
4. Generate and download your animation

## Troubleshooting

### Common Issues

1. **OpenCV Installation Issues**
   - Make sure you have all system dependencies installed
   - Try running `brew install opencv` if the Python package installation fails

2. **Virtual Environment Issues**
   - If you get "command not found" errors, make sure you've activated the virtual environment
   - Try recreating the virtual environment if you encounter dependency issues

3. **Permission Issues**
   - Make sure the `uploads` directory and its subdirectories have write permissions
   - Run `chmod -R 755 uploads` if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here] 