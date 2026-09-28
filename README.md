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
