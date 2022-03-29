#define Sensor_in A7
#define Flag_in 22
#define RED 53
#define GREEN 51

int HG_C1050=0;
float avg=0;

void setup() {
  Serial.begin(115200);
  pinMode(Flag_in,INPUT);
  pinMode(RED,OUTPUT);
  pinMode(GREEN,OUTPUT);
}

double mapf(long val, long in_min, long in_max, double out_min, double out_max) {
  return (double)(val-in_min)*(out_max-out_min)/(double)(in_max-in_min)+out_min;
}

void loop() {
  int FLAG=digitalRead(Flag_in);
  int HG_C1050=analogRead(Sensor_in);//-8;
  for(int i=0;i<29;i++) {
    int HG_C1050=analogRead(Sensor_in);//-8;
    avg=avg+HG_C1050;
  }
  avg=avg/30;
  
  double dis=(mapf(avg,0,1024,-15.04,14.11));//*1.004);//0.956
  
  if(FLAG==1) {
    digitalWrite(RED,HIGH);
    digitalWrite(GREEN,LOW);
  }
  else {
    digitalWrite(GREEN,HIGH);
    digitalWrite(RED,LOW);
  }
  Serial.print(FLAG);
  Serial.print("V");
  Serial.println(dis,2);
}
