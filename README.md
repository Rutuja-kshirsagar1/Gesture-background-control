# gesture-background-system

# Gesture Controlled Video Background System

A real-time computer vision application that changes video backgrounds and plays audio based on hand gestures detected via webcam.

## Features

- **Hand Gesture Recognition** - Detects specific finger combinations to trigger different backgrounds
- **Real-time Background Replacement** - Uses selfie segmentation to replace background with videos
- **Audio Synchronization** - Plays corresponding audio when background changes
- **Smooth Transitions** - Implements temporal smoothing for natural background blending

## Gesture Controls

| Gesture | Fingers | Action |
|---------|---------|--------|
| ✌️ Index Only | Index finger up, others down | fire |
| ✌️✌️ Index + Middle | Both index & middle up | Sharingan  |
| 🤙 Index + Pinky | Index & pinky up | Galaxy  |

## Requirements

- Python 3.7+
- Webcam
- Audio output device

## Installation

1. **Clone or download** this project to your local machine

2. **Install dependencies** using pip:
   ```bash
   pip install -r requirements.txt
Prepare media files - Place the following files in the same directory as the script:

ultra.mp4 - Background video for index-only gesture

sharengan.mp4 - Background video for index+middle gesture

galaxy.mp4 - Background video for index+pinky gesture

fire.mpeg - Audio for ultra background

sharengan audio.mp3 - Audio for sharingan background

galaxy audio.mp3 - Audio for galaxy background

Usage
Run the script:

bash
python main.py
Show your hand to the webcam

Make the corresponding gesture to change the background:

Raise only your index finger → Ultra background

Raise index and middle fingers → Sharingan background

Raise index and pinky fingers → Galaxy background

Press ESC to exit the application
--------------------------------------------------------------



How It Works

Hand Detection - MediaPipe Hands tracks hand landmarks in real-time

Finger Tracking - Calculates finger positions to detect gestures

Selfie Segmentation - Separates person from background using MediaPipe

Smoothing - Temporal filtering prevents flickering in segmentation mask

Background Compositing - Blends person with selected video background

Audio Trigger - Plays audio once when gesture changes background

-------------------------------------------------------------------------------
Known Limitations


Works best with single hand in frame

Requires relatively uniform background for optimal segmentation

Audio plays once per gesture change (not looped)

Performance depends on system hardware

------------------------------------------------------------------------

Dependencies Details


opencv-python - Video capture, processing, and display

mediapipe - Hand tracking and selfie segmentation

numpy - Array operations for image blending

pygame - Audio playback


------------------------------------------------------------------------
made by Rutuja Kshirsagar with 🤍
