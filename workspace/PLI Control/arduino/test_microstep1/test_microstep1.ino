void setup() {
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  digitalWrite(8,LOW);
  digitalWrite(9,LOW);

  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Hello world!");  // prints hello with ending line break 

}

int num = 0;

void loop() {


  while(Serial.available() > 0){
    num = (Serial.read()-'0');
    if(num == 1){
      Serial.println("Run one cicle.");
      digitalWrite(8,HIGH);
      delayMicroseconds(2000);
      digitalWrite(8,LOW);
      delayMicroseconds(1000);
      num = 0;
    }
  }
}
