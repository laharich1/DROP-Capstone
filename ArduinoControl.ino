#include <Servo.h>

int dist;
int trigPin = 7;
int echoPin = 6;
int LED1Pin = 2;
int LED2Pin = 4;

int PWMPin1 = 11 ;
int PWMPin2 = 10;
int PWMPin3 = 9;

int startButtonPin = 8;
Servo ESC1;
Servo ESC2;
Servo ESC3;



unsigned long curr;
unsigned long start;

boolean newData = false;
int thrust[] = {1000, 1000, 1000}; 


void setup() {
  Serial.begin(9600); // Starts the serial communication
  
  // put your setup code here, to run once:
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

  pinMode(LED1Pin, OUTPUT);
  pinMode(LED2Pin, OUTPUT);

  pinMode(startButtonPin, INPUT_PULLUP);

  Serial.println("Pins Initialized");
  


  ESC1.attach(PWMPin1, 1000, 2000); //ESC Min/Max Microseconds
  ESC2.attach(PWMPin2, 1000, 2000);
  ESC3.attach(PWMPin3, 1000, 2000);
  ESC1.writeMicroseconds(1000); //Write Minimum Pulse
  ESC2.writeMicroseconds(1000);
  ESC3.writeMicroseconds(1000);

  Serial.println("Starting ESC Calibration");
  delay(10000); //Wait for 10 seconds for motors to initialize
  digitalWrite(LED1Pin, HIGH);
  Serial.println("Waiting for Button Press...");
  while(digitalRead(startButtonPin) == HIGH)
  {
    delay(1); //Wait for button to be pressed to start
  }
  digitalWrite(LED1Pin, LOW);
  delay(10000);
  digitalWrite(LED1Pin, HIGH);

  Serial.println("GO GO GO");
  start = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  
  get_data();
  dist = get_dist(); // shut off if close to ground
  curr = millis();
  
  if( ((curr - start) >= 20000 ) || (dist < 30))
  {
    
    ESC1.writeMicroseconds(1000); //turn off 
    ESC2.writeMicroseconds(1000);
    ESC3.writeMicroseconds(1000);
    Serial.println("Shut Down");
    digitalWrite(LED2Pin, HIGH);
    while(true)
    {
      delay(1); //loop forever 
    }
    
  }
  delay(5);
}

int get_dist()
{
  long duration;
  int distance;
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.034/2;
  //Serial.print("Distance: ");
  //Serial.println(distance);
  // Prints the distance on the Serial Monitor
  return distance;
}


void get_data()
{
  char rc; 
  int idx = 0;
  int numChars = 7;
  byte arr[] = {0,0,0,0,0,0,0};
  char endMarker = 'p';
  byte c1;
  byte c2;
  while (Serial.available() > 0 && newData == false) {
        rc = Serial.read(); //get byte
  
        if (rc != endMarker) {
            arr[idx] = rc;

            if (idx == 1)
            {
              c1 = arr[0];
              c2 = arr[1];
              thrust[0] = (c1 << 8) | c2;
            }
            else if (idx == 3)
            {
              c1 = arr[2];
              c2 = arr[3];
              thrust[1] = (c1 << 8) | c2;
            }
            if (idx == 5)
            {
              c1 = arr[4];
              c2 = arr[5];
              thrust[2] = (c1 << 8) | c2;
            }

            idx++;
        }
        else {
            arr[idx] = '\0'; // terminate the string
            
            if (idx == 6)
            {
              newData = true;
            }
            idx = 0;
        }
  }
  
  if(newData)
  {
    
    Serial.println("GOT NEW DATA");

    Serial.println(thrust[0]);
    Serial.println(thrust[1]);
    Serial.println(thrust[2]);
    ESC1.writeMicroseconds(thrust[0]);
    ESC2.writeMicroseconds(thrust[1]);
    ESC3.writeMicroseconds(thrust[2]);
    newData = false;
  }
  }
  
