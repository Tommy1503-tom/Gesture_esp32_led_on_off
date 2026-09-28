import cv2
import mediapipe as mp
import serial
import time
import math


# ============================================================
# USER SETTINGS
# ============================================================

SERIAL_PORT = "COM24"       # <<< แก้เป็น COM ของ ESP32
BAUD_RATE = 115200

CAMERA_INDEX = 0

# เวลาป้องกันการส่งคำสั่งซ้ำ
COMMAND_COOLDOWN = 1.0


# ============================================================
# CONNECT ESP32
# ============================================================

print("Connecting to ESP32...")

try:
    esp32 = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=0.1
    )

    time.sleep(2)

    print("ESP32 connected:", SERIAL_PORT)

except Exception as e:

    print()
    print("ERROR: Cannot connect to ESP32")
    print("Check COM port:", SERIAL_PORT)
    print(e)
    exit()


# ============================================================
# MEDIAPIPE
# ============================================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65
)


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():

    print("ERROR: Cannot open webcam")

    esp32.close()
    exit()


# ============================================================
# VARIABLES
# ============================================================

last_command = ""
last_command_time = 0

current_gesture = "NONE"

light_state = False


# ============================================================
# SEND COMMAND
# ============================================================

def send_command(command):

    global last_command
    global last_command_time
    global light_state

    now = time.time()

    # ป้องกันการส่งซ้ำเร็วเกินไป
    if command == last_command:
        if now - last_command_time < COMMAND_COOLDOWN:
            return

    try:

        esp32.write((command + "\n").encode())

        last_command = command
        last_command_time = now

        if command == "ON":
            light_state = True

        elif command == "OFF":
            light_state = False

        print("SEND ->", command)

    except Exception as e:

        print("Serial error:", e)


# ============================================================
# DISTANCE
# ============================================================

def distance(p1, p2):

    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


# ============================================================
# FINGER DETECTION
# ============================================================

def get_finger_states(hand_landmarks):

    lm = hand_landmarks.landmark

    # --------------------------------------------------------
    # Thumb
    # --------------------------------------------------------
    #
    # ใช้ระยะจากปลายนิ้วโป้งไปยังข้อนิ้ว
    # และตำแหน่งสัมพันธ์กับนิ้วก้อย
    #

    thumb_tip = lm[4]
    thumb_ip = lm[3]

    index_mcp = lm[5]
    pinky_mcp = lm[17]

    thumb_tip_to_index = distance(thumb_tip, index_mcp)
    thumb_tip_to_pinky = distance(thumb_tip, pinky_mcp)

    thumb_extended = (
        thumb_tip_to_pinky >
        thumb_tip_to_index
    )


    # --------------------------------------------------------
    # Index
    # --------------------------------------------------------

    index_extended = (
        lm[8].y < lm[6].y
    )


    # --------------------------------------------------------
    # Middle
    # --------------------------------------------------------

    middle_extended = (
        lm[12].y < lm[10].y
    )


    # --------------------------------------------------------
    # Ring
    # --------------------------------------------------------

    ring_extended = (
        lm[16].y < lm[14].y
    )


    # --------------------------------------------------------
    # Pinky
    # --------------------------------------------------------

    pinky_extended = (
        lm[20].y < lm[18].y
    )


    return (
        thumb_extended,
        index_extended,
        middle_extended,
        ring_extended,
        pinky_extended
    )


# ============================================================
# GESTURE RECOGNITION
# ============================================================

def recognize_gesture(states):

    thumb, index, middle, ring, pinky = states

    # ========================================================
    # ✌️ V SIGN
    #
    # Index + Middle = OPEN
    # Thumb/Ring/Pinky = CLOSED
    # ========================================================

    if (
        index and
        middle and
        not ring and
        not pinky
    ):

        return "V"


    # ========================================================
    # 👍 THUMB
    #
    # Thumb = OPEN
    # Other fingers = CLOSED
    # ========================================================

    if (
        thumb and
        not index and
        not middle and
        not ring and
        not pinky
    ):

        return "THUMB"


    return "NONE"


# ============================================================
# MAIN LOOP
# ============================================================

print()
print("------------------------------------------")
print("Gesture Light Control")
print("------------------------------------------")
print("✌️  V       = LIGHT ON")
print("👍  THUMB   = LIGHT OFF")
print("Q           = EXIT")
print("------------------------------------------")
print()


while True:

    ret, frame = cap.read()

    if not ret:
        print("Cannot read webcam")
        break


    # --------------------------------------------------------
    # Mirror image
    # --------------------------------------------------------

    frame = cv2.flip(frame, 1)


    # --------------------------------------------------------
    # Convert BGR -> RGB
    # --------------------------------------------------------

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # --------------------------------------------------------
    # MediaPipe
    # --------------------------------------------------------

    results = hands.process(rgb)


    gesture = "NONE"


    # --------------------------------------------------------
    # Detect hand
    # --------------------------------------------------------

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]


        # Draw hand
        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )


        # Finger states
        states = get_finger_states(
            hand_landmarks
        )


        # Gesture
        gesture = recognize_gesture(
            states
        )


    # ========================================================
    # GESTURE ACTION
    # ========================================================

    if gesture == "V":

        current_gesture = "V SIGN"

        # ✌️ OPEN LIGHT
        send_command("ON")


    elif gesture == "THUMB":

        current_gesture = "THUMBS UP"

        # 👍 CLOSE LIGHT
        send_command("OFF")


    else:

        current_gesture = "NONE"


    # ========================================================
    # DISPLAY
    # ========================================================

    # Header
    cv2.rectangle(
        frame,
        (0, 0),
        (640, 100),
        (0, 0, 0),
        -1
    )


    # Gesture
    cv2.putText(
        frame,
        "Gesture: " + current_gesture,
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    # Light status
    if light_state:

        status = "LIGHT: ON"

    else:

        status = "LIGHT: OFF"


    cv2.putText(
        frame,
        status,
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    # Instructions

    cv2.putText(
        frame,
        "V = ON    THUMB = OFF    Q = EXIT",
        (20, 450),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # Show
    # --------------------------------------------------------

    cv2.imshow(
        "ESP32 Gesture Light Control",
        frame
    )


    # --------------------------------------------------------
    # Exit
    # --------------------------------------------------------

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break


# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()

hands.close()

esp32.close()

print("Program stopped.")
