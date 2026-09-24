from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "hand_landmarker.task"

BASE_FREQUENCY = 123.47  # B2 note
MAX_CHORD_NOTES = 8