#include <Bounce2.h>
#include <math.h>

char ACK_INIT[] = "**##001";
char ACK_ROT[] = "**##002";
char ACK_HOME[] = "**##003";
char ACK_MAX[] = "**##004";
char ACK_RESET[] = "**##005";
char ACK_LEFT[] = "**##006";
char ACK_RIGHT[] = "**##007";

int CMD_ROT = 0;
int CMD_HOME = 2;
int CMD_RESET = 6;
int CMD_LEFT = 3;
int CMD_RIGHT = 4;


int PUL = 8;
int DIR = 9;
int SWT_LEFT = 7;
int SWT_RIGHT = 6;
int RESET = 5;
int num = -1;
int listAngs[] = {10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170};
float currCic = 0;
float doneCic = 0;
const float MAX_CIC = 28700; // num. cics to reach 360 degrees, computed using the polynomial
int ind = 0;

//debounces switch signal
Bounce bouncer_l = Bounce();
Bounce bouncer_r = Bounce();

// 3rd degree polynomial coeffs 
// f(y) = pa*Ang^3 + pb*Ang^2 + pc*Ang + pd
const float pa = 0;
const float pb = -0.0018;
const float pc = 80.2894;
const float pd = 8.4442;

//computer using the jupyter notebook
//[ -1.53356329e-05   6.86476535e-03   7.95952621e+01  -1.28410674e+02]
//const float pa = -1.53356329e-05;
//const float pb = 6.86476535e-03;
//const float pc = 7.95952621e+01;
//const float pd = -1.28410674e+02;

void setup() {
  digitalWrite(RESET,HIGH);
  pinMode(PUL,OUTPUT);
  pinMode(DIR,OUTPUT);
  pinMode(SWT_LEFT,INPUT_PULLUP);
  pinMode(SWT_RIGHT,INPUT_PULLUP);
  digitalWrite(PUL,LOW);
  digitalWrite(DIR,LOW);

  //setup bouncer object
  bouncer_l.attach(SWT_LEFT);
  bouncer_l.interval(5);
  bouncer_r.attach(SWT_RIGHT);
  bouncer_r.interval(5);
  
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("**IC initialized!"); 
  Serial.println(ACK_INIT);
}

void loop() {

  bouncer_l.update();
  if(bouncer_l.read() == LOW){
  //if(digitalRead(SWT_LEFT) == LOW){ //default direction CCW
        digitalWrite(PUL,HIGH);
        delayMicroseconds(200);
        digitalWrite(PUL,LOW);
        delayMicroseconds(100);
  }
  bouncer_r.update();
  if(bouncer_r.read() == LOW){
  //if(digitalRead(SWT_RIGHT) == LOW){ //reverse direction CW
        digitalWrite(DIR,HIGH);
        digitalWrite(PUL,HIGH);
        delayMicroseconds(200);
        digitalWrite(PUL,LOW);
        delayMicroseconds(100);
        digitalWrite(DIR,LOW);
  }
  
  while(Serial.available() > 0){
    num = (Serial.read()-'0');
    //soft reset
    if(num == CMD_RESET){
      Serial.println("Reset.");
      pinMode(RESET,OUTPUT);
      digitalWrite(RESET,LOW);
    }

    //ffw to the left about 1 degree (100 duty cicles)
    if(num == CMD_LEFT){
        for(int i=0;i<100;i++){
          digitalWrite(PUL,HIGH);
          delayMicroseconds(200);
          digitalWrite(PUL,LOW);
          delayMicroseconds(100);
        }
        Serial.println(ACK_LEFT);
    }

    //ffw to the right about 1 degree (100 duty cicles)
    if(num == CMD_RIGHT){
        for(int i=0;i<100;i++){
          digitalWrite(DIR,HIGH);
          digitalWrite(PUL,HIGH);
          delayMicroseconds(200);
          digitalWrite(PUL,LOW);
          delayMicroseconds(100);
          digitalWrite(DIR,LOW);
        } 
        Serial.println(ACK_RIGHT);
    }

    //rotate 10 degrees
    if(num == CMD_ROT){
      if(ind > 16){
        Serial.println("**Maximum reached.");
        Serial.println(ACK_MAX); 
        //resetVars();
        continue;
      }
      if(doneCic > MAX_CIC){
        resetVars();
        Serial.println("Max. num. cicles reached.");
      }
      float ang = (float)listAngs[ind];
      //compute num. duty cicles using the polynomial 
      float currCic = (pa*(ang*ang*ang)) + (pb*(ang*ang)) + (pc*ang) + pd;
      float nCic1 = currCic - doneCic;
      int nCic = ceil(nCic1);
      
       
      //Serial.print("Cicles performed: "); Serial.println(doneCic);
      //Serial.print("Current Cicle: "); Serial.println(currCic);
      //Serial.print("Num. cicles: "); Serial.println(nCic); 
        
      rotate(nCic); 
      num = -1;
      ind++;
      doneCic += nCic;

      Serial.print("**ANGLE: "); Serial.println(ang);
      Serial.println(ACK_ROT);
    }else if(num == 2){ //goHome
      goHome();
      Serial.println("**Filters in position 0");
      Serial.println(ACK_HOME);
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
  int nCic = (MAX_CIC - doneCic) + 90;

  Serial.println("Going home.");
  Serial.println(" ");
  Serial.println(" ");
  //Serial.print("Home - num. cics to go: "); Serial.println(nCic); 
  
  rotate(nCic);
  resetVars();
}

