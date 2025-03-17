let waveHeight; // Declare globally, initialize in setup
let count = 4; // Countdown for inhale/exhale, count-up for retention
let state = "WAVE_IN_INHALE"; // States: WAVE_IN_INHALE, WAVE_IN_EXHALE, WAVE_OUT
let startTime = 0;
let totalInTime = 4000; // 4 seconds for inhale
let totalExTime = 4000; // 4 seconds for exhale
let outTime = 40000; // 40 seconds for wave-out

function setup() {
  createCanvas(1080, 1920); // 1080x1920 for vertical video
  waveHeight = height; // Initialize waveHeight with the canvas height
  frameRate(60); // Ensure draw loop runs at 60 FPS
  // Set flipped gradient background (sand at bottom, ocean at top)
  for (let y = 0; y < height; y++) {
    let inter = map(y, height, 0, 0, 1); // Bottom (height) to top (0)
    let r = lerp(237, 135, inter); // Sand (237, 201, 175) to ocean (135, 206, 235)
    let g = lerp(201, 206, inter);
    let b = lerp(175, 235, inter);
    stroke(r, g, b);
    line(0, y, width, y);
  }
  console.log("Setup complete, frameRate:", frameRate());
}

function draw() {
  // Redraw flipped gradient background
  for (let y = 0; y < height; y++) {
    let inter = map(y, height, 0, 0, 1);
    let r = lerp(237, 135, inter);
    let g = lerp(201, 206, inter);
    let b = lerp(175, 235, inter);
    stroke(r, g, b);
    line(0, y, width, y);
  }

  console.log("Draw loop running, frameCount:", frameCount, "frameRate:", frameRate().toFixed(2), "waveHeight:", waveHeight.toFixed(2), "state:", state, "count:", count);

  let elapsed = (millis() - startTime) / 1000; // Time in seconds since state started

  if (state === "WAVE_IN_INHALE") {
    // Inhale: Move from bottom (1920) to top (0) in 4 seconds
    let progress = constrain(elapsed / (totalInTime / 1000), 0, 1); // 4 seconds
    waveHeight = map(progress, 0, 1, height, 0); // From 1920 to 0
    count = Math.max(4 - Math.floor(elapsed), 1); // Countdown from 4 to 1
    console.log("WAVE_IN_INHALE: progress =", progress.toFixed(2), "waveHeight =", waveHeight.toFixed(2), "countdown:", count);
    drawWave(waveHeight);
    if (elapsed >= (totalInTime / 1000)) {
      state = "WAVE_IN_EXHALE";
      startTime = millis(); // Reset timer for exhale phase
      waveHeight = 0; // Start exhale from top
      count = 4; // Reset count for exhale
      console.log("Switching to WAVE_IN_EXHALE at:", millis(), "ms");
    }
  } else if (state === "WAVE_IN_EXHALE") {
    // Exhale: Move from top (0) to bottom (1920) in 4 seconds
    let progress = constrain(elapsed / (totalExTime / 1000), 0, 1); // 4 seconds
    waveHeight = map(progress, 0, 1, 0, height); // From 0 to 1920
    count = Math.max(4 - Math.floor(elapsed), 1); // Countdown from 4 to 1
    console.log("WAVE_IN_EXHALE: progress =", progress.toFixed(2), "waveHeight =", waveHeight.toFixed(2), "countdown:", count);
    drawWave(waveHeight);
    if (elapsed >= (totalExTime / 1000)) {
      state = "WAVE_OUT";
      startTime = millis(); // Reset timer for wave-out phase
      waveHeight = height; // Start wave-out from bottom
      count = 0; // Reset count for wave-out count-up
      console.log("Switching to WAVE_OUT at:", millis(), "ms");
    }
  } else if (state === "WAVE_OUT") {
    // Wave out: Retract from bottom (1920) to top (0) in 40 seconds
    let progress = constrain(elapsed / (outTime / 1000), 0, 1); // 40 seconds
    waveHeight = height * (1 - progress); // Linearly interpolate from height to 0
    count = Math.min(Math.floor(elapsed) + 1, 40); // Count up from 1 to 40
    console.log("WAVE_OUT: progress =", progress.toFixed(2), "waveHeight =", waveHeight.toFixed(2), "count:", count);
    drawWave(waveHeight);

    if (count <= 40) {
      textAlign(CENTER, CENTER);
      textSize(150);
      textFont('Unbounded'); // Use Unbounded font from Google Fonts
      fill(255); // White text for contrast
      text(count, width / 2, height / 2);
    }
  }
}

function drawWave(y) {
  // Gradient wave (white foam to light blue ocean)
  let gradientColors = [
    color(255, 255, 255), // White foam
    color(135, 206, 235), // Sky blue base
    color(0, 119, 190)    // Deeper ocean blue
  ];
  
  noStroke();
  beginShape();
  vertex(0, 0); // Top-left
  vertex(width, 0); // Top-right
  vertex(width, y); // Bottom-right of wave

  // Add wave curvature with gradient
  for (let x = width; x >= 0; x -= 10) {
    let waveY = y + sin(x * 0.01 + frameCount * 0.05) * 100; // Wavy effect
    let inter = map(waveY, 0, y, 0, 1); // Gradient based on wave height
    let c = lerpColor(gradientColors[0], gradientColors[2], inter);
    fill(c);
    vertex(x, waveY);
  }

  // Close the shape
  vertex(0, y); // Bottom-left of wave
  endShape(CLOSE);
}