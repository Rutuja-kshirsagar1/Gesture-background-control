import cv2
import mediapipe as mp
import numpy as np
import pygame

# -----------------------------
# Initialize AUDIO
# -----------------------------
pygame.mixer.init()

audio1 = "assests/fire.mpeg"
audio2 = ""assests/sharengan audio.mp3"
audio3 = ""assests/galaxy audio.mp3"

current_audio = None
current_bg = None  
def play_audio_once(file):
    global current_audio
    pygame.mixer.music.stop()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play() 
    current_audio = file

# -----------------------------
# Load background videos
# -----------------------------
bg_video1 = cv2.VideoCapture(""assests/ultra.mp4")
bg_video2 = cv2.VideoCapture(""assests/sharengan.mp4")
bg_video3 = cv2.VideoCapture(""assests/galaxy.mp4")

# -----------------------------
# MediaPipe setup
# -----------------------------
mp_hands = mp.solutions.hands
mp_selfie = mp.solutions.selfie_segmentation

hands = mp_hands.Hands(max_num_hands=1)
segment = mp_selfie.SelfieSegmentation(model_selection=1)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# -----------------------------
# Finger detection
# -----------------------------
def get_fingers(landmarks):
    fingers = []

    tips = [8, 12, 16, 20]
    dips = [6, 10, 14, 18]

    for tip, dip in zip(tips, dips):
        if landmarks[tip].y < landmarks[dip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# -----------------------------
# Smoothing
# -----------------------------
prev_mask = None

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # -----------------------------
        # HAND detection
        # -----------------------------
        results = hands.process(rgb)

        fingers = [0, 0, 0, 0]

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                fingers = get_fingers(handLms.landmark)

        index_only = fingers == [1, 0, 0, 0]
        index_middle = fingers == [1, 1, 0, 0]
        index_pinky = fingers == [1, 0, 0, 1]

        # -----------------------------
        # SEGMENTATION
        # -----------------------------
        seg = segment.process(rgb)
        mask = cv2.GaussianBlur(seg.segmentation_mask, (15, 15), 0)

        if prev_mask is None:
            prev_mask = mask

        mask = 0.7 * prev_mask + 0.3 * mask
        prev_mask = mask

        alpha = np.clip(mask, 0, 1)
        alpha = np.dstack((alpha, alpha, alpha))

        # -----------------------------
        # CHOOSE VIDEO + AUDIO 
        # -----------------------------
        new_bg = None

        if index_only:
            new_bg = 1
        elif index_middle:
            new_bg = 2
        elif index_pinky:
            new_bg = 3

        # trigger audio 
        if new_bg != current_bg:
            current_bg = new_bg

            if current_bg == 1:
                play_audio_once(audio1)
            elif current_bg == 2:
                play_audio_once(audio2)
            elif current_bg == 3:
                play_audio_once(audio3)
            else:
                pygame.mixer.music.stop()

        # Assign video
        if current_bg == 1:
            bg_video = bg_video1
        elif current_bg == 2:
            bg_video = bg_video2
        elif current_bg == 3:
            bg_video = bg_video3
        else:
            bg_video = None

        # -----------------------------
        # READ BACKGROUND FRAME
        # -----------------------------
        if bg_video is not None:
            ret_bg, bg_frame = bg_video.read()

            if not ret_bg:
                bg_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret_bg, bg_frame = bg_video.read()

            bg_frame = cv2.resize(bg_frame, (640, 480))
            bg_frame = cv2.GaussianBlur(bg_frame, (15, 15), 0)

            output = (frame * alpha + bg_frame * (1 - alpha)).astype(np.uint8)
        else:
            output = frame

        cv2.imshow("Gesture Video Background System", output)

        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    cap.release()
    bg_video1.release()
    bg_video2.release()
    bg_video3.release()
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    cv2.destroyAllWindows()
