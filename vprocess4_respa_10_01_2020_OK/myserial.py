from multiprocessing import Process, Queue, Event
import zmq, time, serial, sys, logging

logging.basicConfig(filename='/home/pi/vprocess4/log/myserial.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


#5556: for listen data
#5557: for publisher data

tau_zmq_connect     = 0.5  #0.3=300 [ms]
tau_zmq_while_write = 0.25 #0.5=500 [ms]
tau_zmq_while_read  = 1#0.25 #0.4#0.25   # 0.5=500 [ms]
tau_serial          = 0.01 #0.08   #0.02  #  0.01=10 [ms]

count = 0
save_setpoint1 = 'wf000u000t000r111e0f0.0'
setpoint_reply_uc = save_setpoint1


##### Queue data: q1 is for put data to   serial port #####
##### Queue data: q2 is for get data from serial port #####
def listen(q1):
    #####Listen part: escribe en el uc las acciones: w, etc.
    port_sub = "5556"
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    socket_sub.connect ("tcp://localhost:%s" % port_sub)
    topicfilter = "w"
    socket_sub.setsockopt(zmq.SUBSCRIBE, topicfilter)
    time.sleep(tau_zmq_connect)

    string = ['','','','']
    while True:
        try:
            string= socket_sub.recv(flags=zmq.NOBLOCK).split()
            q1.put(string[1])

        except zmq.Again:
            pass

        time.sleep(tau_zmq_while_write)

    return True


def speak(q1,q2):
    #####Publisher part: publica las lecturas obtenidas por serial.
    port_pub = "5557"
    context_pub = zmq.Context()
    socket_pub = context_pub.socket(zmq.PUB)
    socket_pub.bind("tcp://*:%s" % port_pub)
    topic   = 'w'#'w'
    time.sleep(tau_zmq_connect)

    while True:
        q1.put("read")

        if not q2.empty():
            data = q2.get()
            try:
                socket_pub.send_string("%s %s" % (topic, data))

            except:
                logging.info("================Exception in speak function by reset in micro-controller===========================")

        time.sleep(tau_zmq_while_read) #Tiempo de muestreo menor para todas las aplicaciones que recogen datos por ZMQ.

    return True

def set_dtr():
    global save_setpoint1

    try:
        ser = serial.Serial(port='/dev/ttyUSB0', timeout = 1, baudrate = 9600)
        ser.setDTR(True)
        time.sleep(1)
        ser.setDTR(False)
        time.sleep(1)
        logging.info("======================================================Se ejecuto SET_DTR()======================================")

        logging.info("===================================================== Send last setpoint's post SET_DTR() ======================")
        ser.write(save_setpoint1 + '\n')
        result = ser.readline().split()
        logging.info("===================================================== save_setpoint1 READY =====================================")

    except:
        logging.info("---------------------------------------------------- Fallo Ejecucion set_dtr() ---------------------------------")

def rs232(q1,q2):
    global save_setpoint1
    global setpoint_reply_uc
    global count

    flag = False
    while not flag:
        try:
            logging.info("---------------------------Try Open SerialPort-USB------------------------------------------------------")
            ser = serial.Serial(port='/dev/ttyUSB0', timeout = 1, baudrate=9600)

            #necesario para setear correctamente el puerto serial
            ser.setDTR(True)
            time.sleep(1)
            ser.setDTR(False)
            time.sleep(1)
            logging.info("--------------------------------DTR SET READY----------------------------------------------------------")
            logging.info("Post DTR SET READY: flag = %s", flag)

            if flag:
                ser.write(save_setpoint1 + '\n')
                result = ser.readline().split()
                logging.info("Primer envio de comando save_setpoint1: %s ",  save_setpoint1)

            elif not flag:
                logging.info("Conexion Serial Re-establecida")
                logging.info("Reenviando ultimo SETPOINT %s", save_setpoint1)
                ser.write(save_setpoint1 + '\n')
                result = ser.readline().split()
                logging.info("not flag last command: myserial_w_reply_uc: %s ", result)

            flag = ser.is_open

            if flag:
                logging.info('CONEXION SERIAL EXITOSA, flag= %s', flag)

            while ser.is_open:
                try:
                    if not q1.empty():
                        action = q1.get()

                        #Action for read measure from serial port
                        if action == "read":
                            try:
                                if ser.is_open:
                                    logging.info("myserial_r_action_to_uc: %s ", action)
                                    ser.write('r' + '\n')
                                    SERIAL_DATA = ser.readline()
                                    if SERIAL_DATA != "":
                                        logging.info("myserial_r_reply_uc: %s", SERIAL_DATA)
                                        q2.put(SERIAL_DATA)
                                    else:
                                        logging.info("myserial_r_reply_uc_VACIO?: %s", SERIAL_DATA)

                                    try:
                                        temp = SERIAL_DATA.split()
                                        temp = "".join(map(str, temp[8:]))

                                        if temp != "":
                                            setpoint_reply_uc = temp
                                            logging.info("SETPOINT_REPLY_UC: %s", setpoint_reply_uc[0:23])

                                            if setpoint_reply_uc[0:23] == save_setpoint1:
                                                logging.info("IGUALES:    (save_setpoint1, setpoint_reply_uc) = (%s,%s) ", save_setpoint1, setpoint_reply_uc)

                                            elif setpoint_reply_uc != save_setpoint1:
                                                logging.info("DIFERENTES: (save_setpoint1, setpoint_reply_uc) = (%s,%s) ", save_setpoint1, setpoint_reply_uc)
                                                logging.info("URGENTE: REENVIAR SETPOINT!!!")

                                                logging.info("REENVIANDO SETPOINT A UC _ PERDIDA: %s ", save_setpoint1)
                                                ser.write(save_setpoint1 + '\n')
                                                result = ser.readline().split()
                                                logging.info("RESPUESTA UC A PERDIDA DE SETPOINT: %s ", result)


                                    except:
                                        logging("NO SE PUDO HACER SPLIT")


                                else:
                                    ser.open()
                                    logging.info("******************************* Se aplica ser.open() a puerto serial !!! *******************************")

                            except:
                                logging.error("no se pudo leer SERIAL_DATA del uc")
                                ser.close()
                                flag = False

                        #Action for write command of setpont + remontaje (29-09-19) to serial port
                        else:
                            try:
                                #escribiendo al uc_master
                                logging.info("myserial_w_action_to_uc: %s ", action)
                                ser.write(action + '\n')

                                #leyendo la respuesta del uc_master al comando "action" anterior
                                result = ser.readline().split()
                                logging.info("myserial_w_reply_uc: %s ", result)

                                #nuevo
                                if action[0] == 'w':
                                    save_setpoint1 = action
                                    logging.info("************* Se actualizan save_setpoint1 (write setpoint to UC): %s   *************", save_setpoint1)


                            except:
                                logging.info("no se pudo escribir al uc")
                                #save_setpoint1 = action
                                logging.info("the last setpoint save")
                                #ser.close()
                                #flag = False

                    elif q1.empty():
                        #logging.info("ELIF: q1.empty()=VACIO, se espera tau_serial para que lleguen datos para enviar al uc")
                        time.sleep(tau_serial)



                except:
                    print "se entro al while pero no se pudo revisar la cola"
                    logging.info("se entro al while pero no se pudo revisar la cola")

                time.sleep(tau_serial)

        except serial.SerialException:
            print "conexion serial no realizada"
            logging.info("Sin Conexion Serial")
            flag = False
            time.sleep(2)
            set_dtr() #esta sobrando esto al parecer.

    logging.info("Fin de myserial.py")
    return True


def main():
    q1 = Queue()
    q2 = Queue()

    p0 = Process(target=rs232, args=(q1,q2))  #aca se conjugan los dos de abajo
    p0.start()

    p1 = Process(target=listen, args=(q1,))   #aca se escucha zmq y se escribe en el serial
    p1.start()

    p2 = Process(target=speak, args=(q1, q2)) #aca se lee el serial y se publica por zmq
    p2.start()



if __name__ == "__main__":
    main()
