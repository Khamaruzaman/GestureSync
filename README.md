# GestureSync

GestureSync is a hand gesture detection and tracking application using OpenCV and MediaPipe, which synchronizes gesture-based inputs with system actions or applications. This project utilizes MediaPipe’s hand-tracking API to detect hand landmarks and determine positions for gesture control.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

GestureSync enables gesture-based control of applications, making it easier to interact with systems hands-free. It detects hand gestures and landmarks, providing input that can be used to control applications or interact with virtual interfaces.

## Features

- Real-time hand tracking using MediaPipe.
- Gesture-based control for applications or actions.
- Customizable gesture detection with easy-to-modify code structure.
- Bounding box and landmark detection for precise tracking.

## Installation

To set up GestureSync, ensure you have Python installed and follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Khamaruzaman/GestureSync.git
   cd GestureSync
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. The application will open the camera feed, detect your hands, and display the hand landmarks in real-time.

3. Perform gestures within the camera frame to see tracking results or trigger configured actions.

### Example Gesture Code

You can add or modify gestures in the `gesture_detection.py` file, where you define specific hand poses or movements for different commands.

## Configuration

- **Camera Source**: Modify the camera source in `main.py` if you want to use a different camera.
- **Hand Landmarks and Actions**: Customize actions based on hand landmarks by modifying the methods in `HandDetectionModule.py`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bug fixes, new features, or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
