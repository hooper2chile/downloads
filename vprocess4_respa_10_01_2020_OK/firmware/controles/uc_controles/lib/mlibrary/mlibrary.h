#include "Arduino.h"
#include "Wire.h"
#include "SoftwareSerial.h"
#include "rgb_lcd.h"

SoftwareSerial mySerial(2, 3);  //RX(Digital2), TX(Digital3) Software serial port.

rgb_lcd lcd;
const int colorR = 255;
const int colorG = 0;
const int colorB = 0;

#define  INT(x)   (x-48)  //ascii convertion
#define iINT(x)   (x+48)  //inverse ascii convertion

#define SPEED_MAX 150.0 //MIN_to_us/(STEPS*TIME_MIN)
#define SPEED_MIN 1
#define TEMP_MAX  60

#define REMONTAJE_PIN  A0 //bomba remontaje
#define AGUA_FRIA      A1 //D10 = rele 1 (cable rojo)
#define AGUA_CALIENTE  A2 //D11 = rele 2 (cable amarillo)
#define VENTILADOR     A3 //ventilador

#define k0 0.1
#define k1 0.2//0.2
#define k2 0.3//0.3
#define k3 0.4//0.4
#define k4 0.5
#define k5 0.6
#define k6 0.7
#define k7 0.8
#define k8 0.9
#define k9 1.0

#define Gap_temp0 0.5
#define Gap_temp1 1.0    //1C
#define Gap_temp2 2.0
#define Gap_temp3 3.0
#define Gap_temp4 4.0
#define Gap_temp5 5.0
#define Gap_temp6 7.0    //6.0
#define Gap_temp7 9.0    //7.0
#define Gap_temp8 11.0   //8.0
#define Gap_temp9 13.0   //9.0

String  new_write   = "wf000u000t000r111d111\n";
String  new_write0  = "";

String message = "";
String state   = "";

boolean stringComplete = false;  // whether the string is complete

//Re-formatting
String  uset_temp = "";
String  svar      = "";

// RST setup
uint8_t rst1 = 1;       uint8_t rst2 = 1;       uint8_t rst3 = 1;
uint8_t rst1_save = 1;  uint8_t rst2_save = 1;  uint8_t rst3_save = 1;
//DIRECTION SETUP
uint8_t dir1 = 1;  uint8_t dir2 = 1;  uint8_t dir3 = 1;

uint8_t pump_enable = 0;

float mytemp_set = 0;
float mytemp_set_save = 0;

uint8_t unload = 0;
uint8_t unload_save = 0;

uint8_t feed = 0;
uint8_t feed_save = 0;

uint8_t u_temp_save = 0;


//variables control temperatura
float dTemp  = 0;
float Temp_  = 0;
float u_temp = 0;
float umbral_temp = SPEED_MAX;
//fin variables control temperatura
//******


//for communication i2c
void receiveEvent() {
  while ( Wire.available() > 0 ) {
    byte x = Wire.read();
     message += (char) x;
     if ( (char) x == '\n' ) {
      stringComplete = true;
     }
  }  //Serial.println(message);         // print the character
}

//for hardware serial
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    message += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}


void crumble() {
    if ( message[0] == 'w' && message[9] == 't' ) {
      mytemp_set = message.substring(10,13).toFloat();
      feed   = message.substring(2,5).toInt();
      unload = message.substring(6,9).toInt();
      rst1 = int(INT(message[14]));  //rst_feed
      rst2 = int(INT(message[15]));  //rst_unload
      rst3 = int(INT(message[16]));  //rest_temp

      //trama remontaja unificada el 29-09-19 con la trama de setpoint
      pump_enable = INT(message[18]);
      Temp_ = message.substring(24).toFloat();
    }
  return;
}

void remontaje(int pump_enable) {
  if (pump_enable) digitalWrite(REMONTAJE_PIN, LOW);
  else digitalWrite(REMONTAJE_PIN, HIGH);

  return;
}


void cooler(int rst1, int rst2, int rst3) {
  if (rst1 == 0 || rst2 == 0 || rst3 == 0)
	  digitalWrite(A3, LOW );
  else    digitalWrite(A3, HIGH);

}

//Control temperatura para agua fria y caliente
void control_temp(int rst3) {
  if (rst3 == 0) {
    //touch my delta temp
    dTemp = mytemp_set - Temp_;

    //CASO: necesito calentar por que setpoint es inferior a la medicion
    if ( dTemp >= -0.1 ) {
      delay(1);
      digitalWrite(AGUA_FRIA, HIGH);
      delay(1);
      digitalWrite(AGUA_CALIENTE, LOW);
    }
    //CASO: necesito enfriar por que medicion es mayor a setpoint
    else if ( dTemp < 0.2 ) {
      delay(1);
      digitalWrite(AGUA_FRIA, LOW);
      delay(1);
      digitalWrite(AGUA_CALIENTE, HIGH);
      dTemp = (-1)*dTemp;
    }

    if ( dTemp <= Gap_temp0 )      u_temp = 90;
    else if ( dTemp <= Gap_temp1 ) u_temp = 95;
    else if ( dTemp <= Gap_temp2 ) u_temp = 100;
    else if ( dTemp <= Gap_temp3 ) u_temp = 110;
    else if ( dTemp <= Gap_temp4 ) u_temp = 120;
    else if ( dTemp <= Gap_temp5 ) u_temp = 130;
    else if ( dTemp <= Gap_temp6 ) u_temp = 135;
    else if ( dTemp <= Gap_temp7 ) u_temp = 140;
    else if ( dTemp <= Gap_temp8 ) u_temp = 145;
    else if ( dTemp > Gap_temp9  ) u_temp = SPEED_MAX;
  }
  else {
    //el sistema se deja stanby
    digitalWrite(AGUA_CALIENTE, HIGH);
    digitalWrite(AGUA_FRIA, HIGH);
  }

  u_temp_save = int(u_temp);

  //for debug
  /*
  Serial.println("mytemp_set:  " + String(mytemp_set));
  Serial.println("Temp_:       " + String(Temp_));
  Serial.println("dTemp :      " + String(dTemp));
  Serial.println("u_temp_save: " + String(u_temp_save));
  Serial.println("uset_temp:   " + String(uset_temp));
  Serial.println("\n\n");
  */
  return;
}

//function for transform numbers to string format of message
void format_message(int var) {
  //reset to svar string
  svar = "";
  if (var < 10)
    svar = "00"+ String(var);
  else if (var < 100)
    svar = "0" + String(var);
  else
    svar = String(var);
  return;
}

void broadcast_setpoint(uint8_t select) {
  //se prepara el setpoint para el renvio hacia uc_step_motor.
  format_message(u_temp_save); //string variable for control: uset_temp_save
  uset_temp = svar;

  switch (select) {
    case 0: //only re-tx and update pid uset's.
      new_write0 = "";
      new_write0 = "wf" + new_write.substring(2,5) + 'u' + new_write.substring(6,9) + 't' + uset_temp + 'r' + new_write.substring(14,17) + 'd' + "111\n";
      mySerial.print(new_write0);
      break;

    case 1: //update command and re-tx.
      new_write  = "";
      new_write  = "wf" + message.substring(2,5)  + 'u' + message.substring(6,9)    + 't' + uset_temp + 'r' + message.substring(14,17)   + 'd' + "111\n";
      mySerial.print(new_write);
      break;

    default:
      break;
  }

  return;
}


void clean_strings() {
  //clean strings
  stringComplete = false;
  message   = "";
  uset_temp = "";
}


int validate_write() {
  if ( message[0] == 'w' ) {
    Serial.println("echo: " + message);
    return 1;
  }
  else {
    Serial.println("BAD command to uc_controles");
    return 0;
  }
}
