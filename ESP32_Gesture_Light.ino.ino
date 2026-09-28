/*
  ESP32 Gesture Light Control
  ----------------------------
  Command from Notebook:

  ON  -> LED ON
  OFF -> LED OFF

  USB Serial 115200 baud
*/
#define LED_PIN 2
//#define LED_PIN LED_BUILTIN

String command = "";

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);

  // เริ่มต้นปิดไฟ
  digitalWrite(LED_PIN, LOW);

  Serial.println("ESP32 Gesture Light Ready");
  Serial.println("Waiting for ON / OFF...");
}

void loop() {

  if (Serial.available()) {

    command = Serial.readStringUntil('\n');

    command.trim();

    // -------------------------
    // เปิดไฟ
    // -------------------------
    if (command == "ON") {

      digitalWrite(LED_PIN, HIGH);

      Serial.println("LIGHT_ON");
    }

    // -------------------------
    // ปิดไฟ
    // -------------------------
    else if (command == "OFF") {

      digitalWrite(LED_PIN, LOW);

      Serial.println("LIGHT_OFF");
    }
  }
}