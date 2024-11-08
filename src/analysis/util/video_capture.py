# context manager for cv2 video captures
from cv2 import VideoCapture as cv2VideoCapture

class VideoCapture:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = None

    def __enter__(self):
        self.cap = cv2VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open video file {self.video_path}")
        return self.cap

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cap is not None:
            self.cap.release()

            if exc_type is not None:
                return False  # propogate the error