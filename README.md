# Chord Visualizer v1

A real-time hand gesture-controlled musical instrument that uses computer vision to detect hand positions and synthesizes musical chords based on finger states.

## Features

- **Real-time hand tracking**: Uses MediaPipe's HandLandmarker for accurate hand landmark detection
- **Gesture-to-chord mapping**: Maps finger states and hand position to different chord types
- **Multiple chord types**: Supports Major, Minor, Diminished 7, Minor 7, Dominant 7, Major 7, Sus2, Sus4, and Sus24 chords in all keys
- **Audio synthesis**: Chord sounds created using pyo with sawtooth and sine oscillators
- **Visual feedback**: Displays hand landmarks, skeleton, and hand triangles in real-time
- **Volume control**: Right hand position controls audio volume

## How It Works

The system detects hand landmarks using MediaPipe and determines which fingers are in or out. The combination of finger states and hand spread determines the chord type played. The left hand controls which chord type is synthesized, while the right hand position (via triangle area) controls the volume. The location and orientation of the left hand controls the root note of the chord.

### Chord Type Mapping (Left Hand)
- **All fingers up + spread**: Major chord
- **All fingers up + close**: Minor chord
- **No fingers up**: Octave
- **Thumb only**: Fifth
- **Index finger only**: Diminished 7 chord
- **Index + Middle**: Minor 7 chord
- **Index + Middle + Ring**: Dominant 7 chord
- **Index + Middle + Ring + Pinky**: Major 7 chord
- **Thumb + Index**: Sus2 chord
- **Thumb + Pinky**: Sus4 chord
- **Thumb + Index + Pinky**: Sus24 chord

### Root Note Control
The root note of the chord is determined by the hand's position in the 6-box grid shown on the screen as well as the hand's orientation. This is determined by the knuckle of the middle finger, which is at the approximate center of the hand. The mapping scheme is as follows:
```
 Palm forward: F  |  Palm forward: C  |  Palm forward: G  |
Palm backward: F# | Palm backward: C# | Palm backward: G# |
-----------------------------------------------------------
 Palm forward: E  |  Palm forward: A  |  Palm forward: D  |
Palm backward: B  | Palm backward: A# | Palm backward: D# |
```

### Volume Control
The right hand's position (the triangle formed by thumb, index, and middle finger) determines the volume level. A triangle with a larger area corresponds to a louder volume, while a triangle with a smaller area corresponds to a quieter volume.

## Requirements

- Python 3.10
- Webcam
- macOS (currently optimized for macOS with CoreAudio)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/audreyw678/chord-visualizer-v1
cd chord-visualizer-v1
```

### 2. Create conda environment
```bash
conda env create -f environment.yml
conda activate chord-visualizer-py310
```

### 3. macOS Setup
pyo requires libFLAC. If you see an ImportError about libFLAC.12.dylib:
1. Make sure Homebrew is installed.
2. Install FLAC: `brew install flac`
3. Create symlink so pyo can find it:
   `ln -s /opt/homebrew/opt/flac/lib/libFLAC.14.dylib /opt/homebrew/opt/flac/lib/libFLAC.12.dylib`

## Usage

1. Ensure your webcam is connected and accessible
2. Activate the conda environment:
   ```bash
   conda activate chord-visualizer-py310
   ```
3. Run the main application:
   ```bash
   python src/main.py
   ```
4. Position your hands in front of the camera
5. Bend your fingers to different angles to create different chords
6. Press 'q' to quit

## Project Structure

```
chord-visualizer-v1/
├── environment.yml          # Conda environment specification
├── models/
│   └── hand_landmarker.task # MediaPipe hand tracking model
├── src/
│   ├── audio_engine.py      # Audio synthesis engine using pyo
│   ├── config.py           # Configuration constants
│   ├── cv_utils.py         # Computer vision utilities for hand tracking
│   ├── hand_info.py        # Hand landmark definitions and connections
│   ├── main.py             # Main application entry point
│   └── notes.py            # Note mapping and frequency calculations
└── README.md
```

## Key Components

### Hand Tracking (`cv_utils.py`)
- `draw_landmarks()`: Visualizes detected hand landmarks
- `draw_hand_skeleton()`: Draws connections between hand joints
- `get_angle()`: Calculates 3D angles between hand landmarks

### Audio Engine (`audio_engine.py`)
- Synthesizes chords using triangle wave oscillators
- Applies effects: low-pass filtering, distortion, chorus, reverb

### Note Mapping (`notes.py`)
- Maps finger angles to musical notes
- Calculates frequencies using 12-tone equal temperament
- Generates chord frequencies from note indices

## Dependencies

- **mediapipe**: Hand tracking and landmark detection
- **opencv-python**: Computer vision and image processing
- **pyo**: Real-time audio synthesis
- **numpy**: Numerical computations
- **sounddevice**: Audio output (used by pyo)

## Project Timeline
- 1/16/2026: Started project, implemented basic hand detection functionality (hand detection, displaying hand landmarks)
- 1/17/2026: Implemented audio synthesis engine with pyo, legacy note mapping system, and gesture recognition. Added real-time chord synthesis and multi-hand support
- 1/20/2026: Implemented triangle area calculation for volume control based on right hand position
- 1/24/2026: Migrated from angle-based to state-based chord synthesis
- 1/27/2026: Implemented finger state detection and chord type mapping.
- 1/29/2026: Added hand regions and root note mapping based on hand region and orientation.
- 1/31/2026: Added octave and fifth chords

## Future improvements
- Support for additional effects and parameters
- Chord visualization, perhaps using Lissajous curves
- Improved GUI
