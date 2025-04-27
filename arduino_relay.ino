void setup() { Serial.begin(9600); pinMode(7, OUTPUT); }

void loop() { if (Serial.available()) { char cmd = Serial.read(); digitalWrite(7, cmd == '1' ? LOW : HIGH); } }