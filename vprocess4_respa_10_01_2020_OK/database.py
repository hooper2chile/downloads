#!usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Adquisición de datos por sockets (ZMQ) para la base de datos.
'''
import os, sys, time, datetime, sqlite3, sqlitebck, logging, communication, zmq

logging.basicConfig(filename='/home/pi/vprocess4/log/database.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
TIME_MIN_BD = 1 # 1 [s]
DIR="/home/pi/vprocess4/"
flag_database = "False"
flag_database_local = False

def update_db(real_data, ficha_producto, connector, c, first_time, BACKUP):
    #CREACION DE TABLAS TEMP1(Sombrero), TEMP2(Mosto), TEMP_ (promedio). CADA ITEM ES UNA COLUMNA
    c.execute('CREATE TABLE IF NOT EXISTS T_SOMBRERO (ID INTEGER PRIMARY KEY autoincrement, FECHA_HORA TIMESTAMP NOT NULL, MAGNITUD REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS T_MOSTO    (ID INTEGER PRIMARY KEY autoincrement, FECHA_HORA TIMESTAMP NOT NULL, MAGNITUD REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS T_PROMEDIO (ID INTEGER PRIMARY KEY autoincrement, FECHA_HORA TIMESTAMP NOT NULL, MAGNITUD REAL)')

    #TABLA FULL CON TODA LA DATA
    c.execute('CREATE TABLE IF NOT EXISTS PROCESO (ID INTEGER PRIMARY KEY autoincrement, FECHA TIMESTAMP NOT NULL, HORA TIMESTAMP NOT NULL, FUNDO TEXT NOT NULL, CEPA TEXT NOT NULL, T_MOSTO REAL, T_SOMBRERO REAL, T_Promedio REAL, T_Setpoint REAL, Flujo REAL, Densidad REAL, Yan REAL, pH REAL, Brix REAL, Acidez REAL, Lote REAL, Dosis REAL, Bomba1 REAL, Bomba2 REAL)')


    logging.info("Se crearon las tablas!!!")

    #se guardan las tablas agregados en la db si no existian
    connector.commit()

    #INSERCION DE LOS DATOS MEDIDOS
    #T.SOMBRERO=: real_data[1];  T.MOSTO=: real_data[2], T.PROMEDIO=: real_data[3]
    try:
        #Insercion solo de los datos de sensores
        c.execute("INSERT INTO T_MOSTO    VALUES (NULL,?,?)", (datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S"), real_data[3]))
        c.execute("INSERT INTO T_SOMBRERO VALUES (NULL,?,?)", (datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S"), real_data[2]))
        c.execute("INSERT INTO T_PROMEDIO VALUES (NULL,?,?)", (datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S"), real_data[1]))

        #TABLA FULL CON TODA LA DATA
        # NULL es para el ID
        c.execute("INSERT INTO PROCESO  VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (datetime.datetime.now().strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%H:%M:%S"), ficha_producto[5], ficha_producto[6], real_data[3], real_data[2], real_data[1], ficha_producto[9], ( float(real_data[8])*float(ficha_producto[12]) ), ficha_producto[0], ficha_producto[1], ficha_producto[2], ficha_producto[3], ficha_producto[4], ficha_producto[7], ficha_producto[8], ficha_producto[10], ficha_producto[11] ))
        logging.info("se insertaron todos los datos en db")

    except:
        #print "no se pudo insertar dato en db"
        logging.info("no se pudo insertar datos en db")

    #se guardan los datos agregados en la db
    connector.commit()

    #Backup DB in RAM to DISK SD
    if BACKUP:

        filedb='/home/pi/vprocess4/database/backup__' + first_time + '__.db'

        bck = sqlite3.connect(filedb)
        sqlitebck.copy(connector, bck)

        try:
            os.system('sqlite3 -header -csv %s "select * from T_SOMBRERO;" > /home/pi/vprocess4/csv/%s' % (filedb,filedb[28:-3])+'T_SOMBRERO.csv' )
            os.system('sqlite3 -header -csv %s "select * from T_MOSTO;"    > /home/pi/vprocess4/csv/%s' % (filedb,filedb[28:-3])+'T_MOSTO.csv'    )
            os.system('sqlite3 -header -csv %s "select * from T_PROMEDIO;" > /home/pi/vprocess4/csv/%s' % (filedb,filedb[28:-3])+'T_PROMEDIO.csv' )

            os.system('sqlite3 -header -csv %s "select * from PROCESO;"    > /home/pi/vprocess4/csv/%s' % (filedb,filedb[28:-3])+'PROCESO.csv' )

            logging.info("\n Backup CSV REALIZADO \n")

        except:
            logging.info("\n Backup FULL NO REALIZADO, NO REALIZADO \n")


        try:
            #Se guarda el nombre de la db para ser utilizado en app.py
            f = open(DIR + "name_db.txt","w")
            f.write(filedb + '\n')
            f.close()

        except:
            #print "no se pudo guardar el nombre de la DB para ser revisada en app.py"
            logging.info("no se pudo guardar el nombre de la DB para ser revisada en app.py")

        return True

def main():
    ficha_producto = [0.0,0.0,0.0,0.0,0.0,"fundo0","cepa0",0,0.0,0,0,0] #ficha_producto[9]=set_data[4]:temparatura set point
    ficha_producto_save = ficha_producto                                #ficha_producto[10] = set_data[0]: bomba1
                                                                        #ficha_producto[11] = set_data[3]: bomba2

    #####Listen measures - estructura para zmq listen ###################################
    tau_zmq_connect = 0.3
    port_sub = "5554"
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    socket_sub.connect ("tcp://localhost:%s" % port_sub)
    topicfilter = "w"
    socket_sub.setsockopt(zmq.SUBSCRIBE, topicfilter)
    time.sleep(tau_zmq_connect)
    ####################################################################################

    i = 0                      #Hora__%H_%M_%S__Fecha__%d-%m-%y
    first_time = time.strftime("Fecha__%d-%m-%y__Hora__%H_%M_%S")
    TIME_BCK = 6 #600 #10 min
    connector = sqlite3.connect(':memory:', detect_types = sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = connector.cursor()

    #Algoritmo de respaldo cada "TIME_BCK [s]"
    BACKUP = False
    start_time = time.time()
    end_time   = time.time()

    global flag_database_local, flag_database
    #reviso constantemente
    while True:
        #reviso la primera vez si cambio el flag, y luego sirve para revisar cuando salga por que fue apagado el flag desde app.py
        try:
            f = open(DIR + "flag_database.txt","r")
            flag_database = f.readlines()[-1]
            f.close()

            logging.info("FLAG_DATABASE WHILE SUPERIOR:")

            if flag_database == "True":
                flag_database_local = True
            else:
                flag_database_local = False

        except:
            logging.info("no se pudo leer el flag en el while principal")

        time.sleep(10)

        #depuracion log
        if flag_database_local is False:
            if i is 10:
                try:
                    f = open(DIR + "db_log.txt","a+")
                    f.write("Grabando OFF: " + time.strftime("__Hora__%H_%M_%S__Fecha__%d-%m-%y") + "\n" )
                    f.close()

                    i = 0
                    logging.info("GRABANDO OFF: " + time.strftime("__Hora__%H_%M_%S__Fecha__%d-%m-%y") + "\n")

                except:
                    logging.info("no se pudo leer grabar el log de grabar off")
                #depuracion log

        i += 1
        while flag_database_local:

            #ZMQ connection for download data #string= socket_sub.recv(flags=zmq.NOBLOCK).split()
            real_data = communication.zmq_client().split()

            #ZMQ connection for download data ficha_producto
            try:
                ficha_producto = socket_sub.recv(flags=zmq.NOBLOCK).split()[1];
                ficha_producto = ficha_producto.split(",")
                ficha_producto_save = ficha_producto
                logging.info("ficha de producto a continuacion: ")
                logging.info(ficha_producto)

            except zmq.Again:
                ficha_producto = ficha_producto_save
                pass
            #ficha_producto = [1,2,3,4,5]


            update_db(real_data, ficha_producto, connector, c, first_time, BACKUP)

            delta = end_time - start_time

            if delta <= TIME_BCK:
                BACKUP = False
                end_time = time.time()

            else:
                start_time = time.time()
                end_time   = time.time()
                BACKUP = True

            #Aqui se determina el tiempo con que guarda datos la BD.-
            time.sleep(TIME_MIN_BD)

            try:
                f = open(DIR + "flag_database.txt","r")
                flag_database = f.readlines()[-1][:-1]
                f.close()

                logging.info("FLAG_DATABASE WHILE SECUNDARIO:")


                if flag_database == "True":
                    flag_database_local = True
                else:
                    flag_database_local = False

            except:
                logging.info("no se pudo leer el flag en el while secundario")


            #log de grabacion: cada 10 seg (dado el time sleep: TIME_MIN_BD del while) se actualiza el log
            if i is 10:
                try:
                    f = open(DIR + "db_log.txt","a+")
                    f.write("Grabando ON: " + time.strftime("Hora__%H_%M_%S__Fecha__%d-%m-%y") + "\n")
                    f.close()

                    i = 0
                    logging.info("GRABANDO ON: " + time.strftime("Hora__%H_%M_%S__Fecha__%d-%m-%y") + "\n")

                except:
                    logging.info("no se pudo leer grabar el log de grabar on")
                #depuracion log

            i += 1


if __name__ == "__main__":
    main()
