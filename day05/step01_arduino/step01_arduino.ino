#include <Servo.h>

Servo myServo;
int servoPin = 9;  // 아두이노 D9 핀에 서보 신호선 연결

void setup() {
  Serial.begin(9600);      // 파이썬과 통신할 속도 (9600)
  myServo.attach(servoPin);
  myServo.write(0);        // 초기 위치: 0° (닫힘)
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'O') {
      myServo.write(90);   // 90° (열림)
    } else if (cmd == 'C') {
      myServo.write(0);    // 0° (닫힘)
    }
  }
}