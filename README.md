# ascii-video-web-converter
Real-time video to ASCII art converter running directly in the browser using Python and PyScript.
# Video to ASCII Art Web Player (PyScript & Python)

An open-source, serverless web application that converts videos into real-time animated ASCII art directly in your browser using Python (via PyScript / WebAssembly). 

No backend server or local installation is required. Hostable for free forever on GitHub Pages.

---

## Features

- In-Browser Python Execution: All pixel luminance processing and character mapping run directly in the browser using PyScript.
- Multiple Input Sources: 
  - Upload local video files (.mp4, .webm, .mov).
  - Stream directly from a direct media URL (CORS-enabled).
- Export Functionality: Download any currently rendered frame as a standard .txt ASCII art file with a single click.
- Aspect Ratio Correction: Automatically calculates monospace font stretching so circles and spheres retain their natural proportions.
- Zero Dependencies to Install: Runs out of the box in modern web browsers on desktop and mobile.

---

## Live Demo & Deployment

This project consists of a single standalone file: index.html.

### How to host on GitHub Pages:
1. Fork or clone this repository.
2. Ensure index.html is in the root directory.
3. In your GitHub repository, go to Settings > Pages.
4. Under Build and deployment > Branch, select main (or master) and folder /(root).
5. Click Save. Your site will be live at:
   https://<your-username>.github.io/<your-repo-name>/

---

## How It Works

1. HTML5 Video Engine: Reads the media stream and pipes individual frames into an off-screen HTML5 Canvas.
2. PyScript & Pyodide: Python reads the raw RGBA image data buffer from the canvas context.
3. Luminance Mapping: Each pixel's brightness is calculated using standard Rec. 601 luma coefficients:
   brightness = 0.299 * R + 0.587 * G + 0.114 * B
4. ASCII Character Quantization: Brightness is quantized into the character ramp:
   ASCII_CHARS = " .':;!*=#$@"
5. Real-Time Rendering: The formatted text string updates inside an optimized monospace pre container on every animation frame.

---

## Requirements

- Any modern browser with WebAssembly support (Chrome, Firefox, Safari, Edge).
- Internet access on first load to fetch PyScript runtime from the CDN.

---

## License

This project is open-source under the MIT License.
