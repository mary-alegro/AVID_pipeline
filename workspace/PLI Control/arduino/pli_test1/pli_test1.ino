#include <math.h>

int PUL = 8;
int DIR = 9;
int num = 1;
int listAngs[] = {10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170};
float currCic = 0;
float doneCic = 0;
const float MAX_CIC = 28854; // computed using polynomial
int ind = 0;


// 3rd degree polynomial coeffs (pa = 0)
const float pb = -0.0018;
const float pc = 80.2894;
const float pd = 8.4442;


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
    if(num == 0){
      if(ind > 16){
        Serial.println("Reset index.");
        resetVars();
      }
      if(doneCic > MAX_CIC){
        Serial.println("Max. num. cicles reached.");
        resetVars();
      }
      float ang = (float)listAngs[ind];
      //compute num. duty cicles using the polynomial 
      float currCic = (pb*(ang*ang)) + (pc*ang) + pd;
      float nCic1 = currCic - doneCic;
      int nCic = ceil(nCic1);
      
      Serial.print("Angle "); Serial.println(ang); 
      Serial.print("Cicles performed: "); Serial.println(doneCic);
      Serial.print("Current Cicle: "); Serial.println(currCic);
      Serial.print("Num. cicles: "); Serial.println(nCic); 
        
      rotate(nCic); 
      num = 1;
      ind++;
      doneCic += nCic;
    }else if(num == 2){ //goHome
      goHome();
    }
  }
}

void resetVars(){
        doneCic = 0;
        ind = 0;
        currCic = 0;
}

void rotate(int nC){
        for(int i = 0; i < nC; i++){ 
        digitalWrite(PUL,HIGH);
        delayMicroseconds(200);
        digitalWrite(PUL,LOW);
        delayMicroseconds(100);
      } 
}

void goHome(){
  int nCic = (MAX_CIC - doneCic) - 50;

  Serial.print("Home - num. cics to go: "); Serial.println(nCic); 
  
  rotate(nCic);
  resetVars();
}

