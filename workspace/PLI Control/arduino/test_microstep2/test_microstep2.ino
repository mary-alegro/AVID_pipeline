int PUL = 8;
int DIR = 9;
int num = 0;
int nCicDeg = 9;
int counter = 1;
int corrFactor = 80; //a cada 81 passos eu pulo 1
int totalDeg = 1;
int degTurn = 5;

void setup() {
  pinMode(PUL,OUTPUT);
  pinMode(DIR,OUTPUT);
  digitalWrite(PUL,LOW);
  digitalWrite(DIR,LOW);

  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("IC initialized!");  // prints hello with ending line break 

}


void loop() {

  while(Serial.available() > 0){
    num = (Serial.read()-'0');
    if(num == 1){
    Serial.print("Round: ");
    Serial.println(totalDeg);
      for(int t=0; t < degTurn; t++){
        if(totalDeg % corrFactor == 0){
          Serial.print("Skip step ");
          Serial.println(totalDeg);
          counter++;
          totalDeg++;
          continue;
        }
        for(int i =0; i < nCicDeg; i++){ //turn 1 degree
          digitalWrite(PUL,HIGH);
          delayMicroseconds(200);
          digitalWrite(PUL,LOW);
          delayMicroseconds(100);
        }
        num = 0;
        counter++;
        totalDeg++;
      }
    }
  }
}
