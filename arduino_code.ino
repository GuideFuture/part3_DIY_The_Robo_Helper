// Smart Robot Data Sender
// Στέλνει απόσταση (HC-SR04) και θερμοκρασία (analog) μέσω Serial
// Δημιουργός: Greg Ios 

// Ορισμός pin για τον υπερηχητικό αισθητήρα
const int trigPin = 9;
const int echoPin = 10;

// Pin θερμοκρασίας (π.χ. LM35)
const int tempPin = A0;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  int distance = readUltrasonic();
  int temp = readTemperature();

  // Αποστολή δεδομένων με μορφή: distance:123,temp:25
  Serial.print("distance:");
  Serial.print(distance);
  Serial.print(",temp:");
  Serial.println(temp);

  delay(1000);
}

// Υπολογισμός απόστασης σε cm από HC-SR04
int readUltrasonic() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;
  return distance;
}

// Ανάγνωση θερμοκρασίας από αισθητήρα (π.χ. LM35)
int readTemperature() {
  int analogValue = analogRead(tempPin);
  float voltage = analogValue * (5.0 / 1023.0);  // μετατροπή σε Volt
  int temperatureC = voltage * 100;              // LM35: 10mV/°C
  return temperatureC;
}
