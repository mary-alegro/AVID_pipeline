int PUL = 8;
int DIR = 9;
int SWT = 10;
int num = 1;
int nCicDeg = 150; //num. duty cicles per degree (don't change)


void setup() {
  pinMode(PUL,OUTPUT);
  pinMode(DIR,OUTPUT);
  pinMode(SWT,INPUT_PULLUP);
  digitalWrite(PUL,LOW);
  digitalWrite(DIR,HIGH);

  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("IC initialized!");  // prints hello with ending line break 

}

void loop() {
  while(Serial.available() > 0){
    num = (Serial.read()-'0');
    if(num == 0){
      Serial.println("Moved cw");
      for(int i =0; i < nCicDeg; i++){ 
        digitalWrite(PUL,HIGH);
        delayMicroseconds(200);
        digitalWrite(PUL,LOW);
        delayMicroseconds(100);
      }
     num = 1;
    }
  }
}

