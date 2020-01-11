
-instalar avrdude.
-condensador 100uF va entre 5V(Arduino a programar), y en RST en el arduiono ISP.
-a veces hay fallos por pines sueltos entre ambos uc.
-el arduino programador usa los pines D13, D12, D11, etc.
-el arduino que se va a programar usar los pines del ISP.

Pagina con ayuda: http://teayudo.con-ip.com/viewtopic.php?f=34&t=422

#usar (estando en la carpeta de optiboot):

avrdude -p atmega328p -c avrisp -P /dev/cu.wchusbserial1410 -b 19200 -v -e -U flash:w:optiboot_atmega328.hex -U lock:w:0x0F:m -F


