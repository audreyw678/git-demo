import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from config import MODEL_PATH
import cv2
from cv_utils import *
from gui_utils import *
from notes import *
from hand_info import *
from audio_engine import ChordEngine

engine = ChordEngine()

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result, output_image, timestamp_ms: int):
    #print('hand landmarker result: {}'.format(result))
    global landmarks
    landmarks = result.hand_landmarks
    engine.set_volume(get_volume_as_float(get_triangle_area_2d(result, "Right")))
    engine.play_chord(get_chord_freqs(get_chord_type(
        get_finger_states(result, "Left"), 
        is_hand_spread(result, "Left")), 
        get_hand_region(result, "Left"), 
        is_palm_front(result, "Left")))

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result,                # runs callback after each detection
    num_hands = 2
)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

landmarks = None

with HandLandmarker.create_from_options(options) as landmarker:
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # wrap frame as an Image object for mediapipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw_regions(frame)
        # detects landmarks
        landmarker.detect_async(mp_image, timestamp_ms=frame_count)
        frame_count += 1

        if landmarks:                           # draw landmarks and skeleton, show on webcam viewer
            draw_landmarks(frame, landmarks)
            draw_hand_skeleton(frame, landmarks)
            draw_triangles(frame, landmarks)
        mirrored_frame = cv2.flip(frame, 1)
        cv2.imshow("Hand Tracker", mirrored_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):   # breaks loop if user presses 'q'
            break

cap.release()
cv2.destroyAllWindows()

