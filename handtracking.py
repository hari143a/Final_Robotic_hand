import requests
import cv2
import mediapipe as mp
import threading
import time

ESP32_IP = "10.174.129.20"   # <-- replace with the printed IP
ESP32_URL_ON = f"http://{ESP32_IP}/on"
ESP32_URL_OFF = f"http://{ESP32_IP}/off"

# Performance optimizations
PROCESS_WIDTH = 320  # Process at lower resolution for speed (320 = 4x faster than 640)
SHOW_WIDTH = 640    # Display at higher resolution for visibility
FRAME_SKIP = 1      # Process every 2nd frame for better performance (0 = all frames, 1 = every 2nd, 2 = every 3rd)
MIN_STATE_CHANGE_INTERVAL = 0.3  # Minimum seconds between state changes (prevents request spam)

# Optimized MediaPipe settings for speed
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,          # False = faster for video
    max_num_hands=1,                  # Only detect one hand
    min_detection_confidence=0.5,     # Lower = faster (was 0.5 default)
    min_tracking_confidence=0.5       # Lower = faster tracking
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)  # Limit FPS

last_state = None
frame_count = 0
last_state_change_time = 0

# Non-blocking HTTP requests using threading with request throttling
def send_request(url, state_name):
    """Send HTTP request in background thread to avoid blocking"""
    try:
        requests.get(url, timeout=0.2)  # Very short timeout for faster failure
        print(f"✅ {state_name}")
    except:
        pass  # Silently fail if ESP32 is not reachable

print("🖐️ Hand-tracking started. Open hand → ON, Closed hand → OFF")
print("Press ESC to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    
    # Skip frames for better performance
    if frame_count % (FRAME_SKIP + 1) != 0:
        continue

    # Resize frame for faster processing (smaller = faster)
    frame_small = cv2.resize(frame, (PROCESS_WIDTH, int(frame.shape[0] * PROCESS_WIDTH / frame.shape[1])))
    
    # Convert to RGB for MediaPipe
    rgb = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on original frame (landmarks are normalized, work on any size)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Simple logic: distance between thumb tip (4) and index tip (8)
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]
            dist = ((thumb.x - index.x)**2 + (thumb.y - index.y)**2) ** 0.5

            # Throttle state changes to prevent request spam
            current_time = time.time()
            time_since_last_change = current_time - last_state_change_time

            if dist > 0.1 and last_state != "on" and time_since_last_change >= MIN_STATE_CHANGE_INTERVAL:
                # Use threading to avoid blocking
                threading.Thread(target=send_request, args=(ESP32_URL_ON, "🖐️ Hand open → LED ON"), daemon=True).start()
                last_state = "on"
                last_state_change_time = current_time
            elif dist < 0.05 and last_state != "off" and time_since_last_change >= MIN_STATE_CHANGE_INTERVAL:
                # Use threading to avoid blocking
                threading.Thread(target=send_request, args=(ESP32_URL_OFF, "✊ Hand closed → LED OFF"), daemon=True).start()
                last_state = "off"
                last_state_change_time = current_time
    else:
        # No hand detected - could optionally reset state here
        pass

    cv2.imshow("Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
