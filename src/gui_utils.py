from hand_info import *
import cv2

def draw_landmarks(frame, hand_landmarks):
    """draw hand landmarks as green circles"""
    if hand_landmarks:
        for hand in hand_landmarks:
            for lm in hand:
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

def draw_triangles(frame, hand_landmarks):
    """draw triangles between thumb, index and middle fingertips"""
    if hand_landmarks:
        for hand in hand_landmarks:
            points = []
            for lm_idx in [THUMB_TIP, INDEX_TIP, MIDDLE_TIP]:
                lm = hand[lm_idx]
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])
                points.append((x, y))
            cv2.line(frame, points[0], points[1], (255, 0, 0), 2)
            cv2.line(frame, points[1], points[2], (255, 0, 0), 2)
            cv2.line(frame, points[2], points[0], (255, 0, 0), 2)

def draw_hand_skeleton(frame, hand_landmarks, connections = HAND_CONNECTIONS, color=(0,255,0)):
    """draw lines between hand joints"""
    if hand_landmarks:
        for hand in hand_landmarks:
            for start_idx, end_idx in connections:
                start = hand[start_idx]
                end = hand[end_idx]
                x1, y1 = int(start.x * frame.shape[1]), int(start.y * frame.shape[0])
                x2, y2 = int(end.x * frame.shape[1]), int(end.y * frame.shape[0])
                cv2.line(frame, (x1, y1), (x2, y2), color, 2)

def draw_regions(frame, color=(255,255, 255)):
    h, w = frame.shape[:2]
    for i in range(1, 4):
        cv2.line(frame, (((w*i)//4), 0), (((w*i)//4), h), color, 1)
    cv2.line(frame, ((w//4), int(h/2)), (w, int(h/2)), color, 1)