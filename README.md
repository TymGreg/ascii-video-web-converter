# Color Video & 3D ASCII Art Studio (PyScript & Python)

An open-source, serverless web application that renders 3D ASCII animations and converts videos into real-time, full-color animated ASCII art directly in the browser using Python (via PyScript / WebAssembly).

No backend server or local installation is required. Hosted for free on GitHub Pages.

---

## Live Demo

https://tymgreg.github.io/ascii-video-web-converter/

---

## Features

- In-Browser Python Execution: All 3D sphere shading, pixel luminance calculations, and character mapping run directly in the browser using PyScript.
- Built-in 3D Celestial Demo: Features a real-time 3D ASCII simulation of a rotating Sun and Moon with Lambertian directional lighting and a starry background.
- Full RGB Color & Monochrome Modes: Toggle seamlessly between true-color RGB character rendering and classic monochrome ASCII output.
- Adjustable Resolution: Dynamically scale character font size and grid density in real time using the built-in slider.
- Multiple Input Sources:
  - Upload local video files (.mp4, .webm, .mov).
  - Stream from direct media URLs (CORS-enabled).
- Video & Text Export:
  - Record and download the live ASCII canvas animation directly as a video file (.mp4 / .webm) at 30 FPS.
  - Export any individual rendered frame as a standard .txt file.

---

## How It Works

1. Off-Screen Frame Sampling: For video inputs, an HTML5 video element pipes frames into an off-screen canvas scaled to match the current character grid dimensions.
2. Python Processing (PyScript / Pyodide): Python reads the RGBA pixel buffer or computes 3D surface normals for the celestial spheres.
3. Luminance & Color Mapping: Brightness is calculated using standard Rec. 601 luma coefficients:
   brightness = 0.299 * R + 0.587 * G + 0.114 * B
4. Character Quantization: Pixel brightness is mapped to the character density ramp:
   ASCII_CHARS = " .':;!*=#$@"
5. Canvas Rendering & Recording: Characters are drawn onto a high-resolution HTML5 Canvas with their respective RGB values and captured via the MediaRecorder API for video export.

---

## Deployment on GitHub Pages

This project is contained within a single standalone file: index.html.

1. Fork or clone this repository.
2. Go to Settings > Pages in your GitHub repository.
3. Under Build and deployment > Branch, select main and /(root), then click Save.

---

## Requirements

- Any modern web browser with WebAssembly and HTML5 Canvas support (Chrome, Firefox, Edge, Safari).
- Internet connection on initial load to fetch the PyScript runtime from the CDN.

---

## License

This project is open-source under the MIT License.
