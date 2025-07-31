# Volume Hand Controller

This project allows you to control your system's volume using hand gestures. By adjusting the distance between your thumb and index finger, you can intuitively increase or decrease the volume.

## Features

-   **Gesture-based volume control**: Control your system's volume by changing the distance between your thumb and index finger.
-   **Real-time visual feedback**: The application displays the camera feed with hand landmarks and a volume bar.
-   **Cross-platform support**: Works on Windows, macOS, and Linux.

## How It Works

The application uses `OpenCV` to capture video from your webcam and `MediaPipe` to detect hand landmarks. The distance between the thumb and index finger is calculated and mapped to a volume range (0-100). This value is then used to set the system's volume.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/volume-hand-controller.git
    cd volume-hand-controller
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the following command to start the application:

```bash
python src/main.py
```