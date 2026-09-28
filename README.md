                 NOTEBOOK
              ┌─────────────┐
              │ Webcam      │
              └──────┬──────┘
                     │
                     ▼
              MediaPipe AI
                     │
          ┌──────────┴──────────┐
          │                     │
        ✌️ V                   👍 Thumb
          │                     │
          ▼                     ▼
        LIGHT ON             LIGHT OFF
          │                     │
          └──────────┬──────────┘
                     │
                 USB Serial
                     │
                     ▼
              ┌─────────────┐
              │    ESP32    │
              │             │
              │ GPIO2/LED   │
              └─────────────┘

              
 กล้อง Notebook
     │
     ▼
Python + OpenCV
     │
     ▼
MediaPipe Hand Tracking
     │
     ├── ✌️ นิ้วชี้ + นิ้วกลาง
     │       └──> ส่ง "ON"
     │
     └── 👍 นิ้วโป้ง
             └──> ส่ง "OFF"
                     │
                     ▼
                 USB Serial
                     │
                     ▼
                   ESP32
                     │
                     ▼
               LED บนบอร์ด

1.ติดตั้ง Python บน Notebook เปิด Command Prompt แล้วใช้
pip install opencv-python mediapipe pyserial
python --version
pip show mediapipe

2.ตรวจสอบ COM Port ของ ESP32 เสียบ ESP32 เข้ากับ Notebook
เปิด Arduino IDE → Tools → Port

3.โปรแกรม AI ตรวจจับท่าทางจากกล้อง
สร้างไฟล์  gesture_light.py

4.วิธีรัน หลังจากแก้
SERIAL_PORT = "COM5"
python gesture_light.py

5.โค้ด ESP32 สร้างไฟล์ Arduino เช่น
ESP32_Gesture_Light.ino แล้ว Upload ลง ESP32





               
