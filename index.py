import cv2
import mediapipe as mp
import serial
import time

# --- Serial setup ---
ser = serial.Serial('COM5', 115200, timeout=1)
time.sleep(2)
print("✅ Connected to ESP32")

# --- MediaPipe setup ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

def get_finger_angles(hand_landmarks):
    lm = hand_landmarks.landmark
    fingers = []

    # ✅ THUMB angle (x-axis) + extra 40
    thumb_diff = (lm[4].x - lm[3].x) * 1000
    thumb_angle = int(90 + thumb_diff + 40)     # 👈 +40 added here
    thumb_angle = max(0, min(180, thumb_angle)) # clamp to 0–180
    fingers.append(thumb_angle)

    # ✅ Other fingers stay same (y-axis)
    for tip in [8, 12, 16, 20]:
        diff = (lm[tip - 2].y - lm[tip].y) * 1000
        angle = int(max(0, min(180, 90 + diff)))
        fingers.append(angle)

    return fingers



print("🖐 Starting camera... Press ESC to quit")

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            angles = get_finger_angles(handLms)

            data = ",".join(map(str, angles)) + "\n"
            ser.write(data.encode())
            print("Sent:", data.strip())

    cv2.imshow("🤚 Hand Tracking - 5 Servo Control", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
