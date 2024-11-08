import time

import cv2
import mediapipe as mp

from HandCV.frame_processor import FrameProcessor
from HandCV.cv_mode import CVMode
from GUI.time_formatter import format_duration, clock
from HandCV.model_result import ModelResult


# this is the main CV loop

# todo: function too long, refactor
def run(processor: FrameProcessor,
        mode: CVMode,
        video_path: str = None,
        camera_index: int = 0,
        display_video: bool = False
        ):
    # todo: write doc below
    """

    :param processor:
    :param mode:
    :param video_path:
    :param camera_index:
    :param display_video:
    :return:
    """
    # make sure there's a video path when in video mode
    if mode == CVMode.VIDEO and video_path is None:
        raise Exception("No video path")

    cap = cv2.VideoCapture(video_path if mode == CVMode.VIDEO else camera_index)

    # if the mode is set to VIDEO, set the capture to the video stream, else set it to the camera index
    if mode == CVMode.VIDEO:
        print('Entering Video Mode')
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    else:
        print('Entering Camera (live) Mode')

    with (mp.solutions.hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.2,
            min_tracking_confidence=0.5) as hands):

        # analytics for the UI
        start_time = time.time()
        frame_count = 0

        # start reading the video
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                # If loading a video, use 'break' instead of 'continue'
                # as an unsuccessful read means the end of a video but could simply be lag in a stream
                if video_path:
                    print("End of Video")
                    break
                else:
                    print("Ignoring empty camera frame.")
                    continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            foreign_result = hands.process(image)

            # prep the image for writing
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # draw the hand annotations on the image.
            process_is_success = bool(foreign_result.multi_hand_landmarks)
            if process_is_success:
                # convert from the foreign result to the ModelResult class
                result = ModelResult.get_from_raw_output(foreign_result)
                processor.process_frame(frame_count, image, result)

            # optionally show the video as its being analyzed to the user
            if display_video or mode == CVMode.LIVE_STREAM:
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
                cv2.imshow('Main', image)

            if mode == CVMode.VIDEO:
                # update UI vars
                frame_count += 1
                elapsed_time = time.time() - start_time

                # calculate remaining time
                if frame_count > 0:
                    avg_time_per_frame = elapsed_time / frame_count
                    remaining_frames = total_frames - frame_count
                    estimated_remaining_time = avg_time_per_frame * remaining_frames
                else:
                    estimated_remaining_time = 0

            # break on 'q'
            if cv2.waitKey(1) == ord('q'):
                break

    cap.release()