# BOLT Wave Animation

A p5.js animation for breathing exercises with wave visualization.

## Prerequisites

- Node.js (Download from https://nodejs.org)
- npm (comes with Node.js)

## Setup

1. Install a simple HTTP server globally:
```bash
npm install -g http-server
```

2. Navigate to the project directory:
```bash
cd /Users/manuangel/Github/thebreathmanu/breathing_animations/bolt_wave_animationv1
```

3. Start the server:
```bash
http-server
```

4. Open your browser and go to:
```
http://localhost:8080
```

## Alternative Method (Python)

If you prefer using Python's built-in HTTP server:

1. Navigate to the project directory:
```bash
cd /Users/manuangel/Github/thebreathmanu/breathing_animations/bolt_wave_animationv1
```

2. Start Python's HTTP server:
```bash
# For Python 3
python3 -m http.server 8080

# For Python 2
python -m SimpleHTTPServer 8080
```

3. Open your browser and go to:
```
http://localhost:8080
```

## Project Structure

```
bolt_wave_animationv1/
├── index.html
├── sketch.js
└── README.md
```

## Controls

- The animation runs automatically through three phases:
  - Inhale (4 seconds)
  - Exhale (4 seconds)
  - Wave Out (40 seconds)

## Troubleshooting

- If you see a blank page, check the browser's console for errors
- Ensure all files are in the correct directory
- Check if p5.js is loading correctly from CDN