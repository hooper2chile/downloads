/*
*  uc_controles: control de temperatura, bomba Remontaje
*  y reles de electrovalvulas.
*  01/05/2019
*  Writed by: Felipe Hooper
*  Electronic Engineer
*/

#include <avr/wdt.h>
#include "mlibrary.h"

void setup() {
  wdt_disable();

  pinMode(A0, OUTPUT); //Bomba remontaje
  pinMode(A1, OUTPUT); //Valvula 1
  pinMode(A2, OUTPUT); //Valvula 2
  pinMode(A3, OUTPUT); //Ventilador

  digitalWrite(A0, HIGH);
  digitalWrite(A1, HIGH);
  digitalWrite(A2, HIGH);
  digitalWrite(A3, HIGH);

  Serial.begin(9600);
  mySerial.begin(9600);

  message.reserve(65);

  DDRB = DDRB | (1<<PB0) | (1<<PB5);
  PORTB = (0<<PB0) | (1<<PB5);

  Wire.begin(2);  //se inicia i2c slave con direccion: 2
  Wire.onReceive(receiveEvent); // data slave recieved


  //inicia enviando apagado total al uc_step_motor
  mySerial.print(new_write);

  wdt_enable(WDTO_8S);
}

void loop() {
  if ( stringComplete ) {
      if ( validate_write() ) {
        //se "desmenuza" el command de setpoints
        crumble();
	      cooler(rst1, rst2, rst3);

        //###################################################################################
        //Codigo para bomba remontaje
        remontaje(pump_enable);
        //###################################################################################

        //nuevo control de temperatura con agua fria y caliente (no PID)
        control_temp(rst3);
        // fin control temperatura

        if (message[0] == 'w') broadcast_setpoint(1);
        else                   broadcast_setpoint(0);

      }
      else Serial.println("bad validate");

      clean_strings();
      wdt_reset();
  }
  //wdt_reset();
}
