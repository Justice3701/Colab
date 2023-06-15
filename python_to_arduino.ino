#define left_LED 7
#define right_LED 8
String str;

void setup() {
  pinMode(left_LED, OUTPUT);
  pinMode(right_LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    // 讀取傳入的字串直到"\n"結尾
    str = Serial.readStringUntil('\n');

    if (str == "A") {           // 若字串值是 "LED_ON" 開燈
        digitalWrite(left_LED, HIGH);     // 開燈
        Serial.println("left_LED is ON"); // 回應訊息給電腦
    }
     else if (str == "B"){
        digitalWrite(left_LED, LOW);
        digitalWrite(right_LED, LOW);
        Serial.println("All LED if off");
      }
  }
}

