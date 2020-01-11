import zmq, time

tau_zmq_connect = 0.3

def zmq_client_data_listen_website():
    #####Listen measures
    port_sub = "5554"
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    socket_sub.connect ("tcp://localhost:%s" % port_sub)
    topicfilter = "w"
    socket_sub.setsockopt(zmq.SUBSCRIBE, topicfilter)

    while True:
        try:
            #espero y retorno valor
            time.sleep(tau_zmq_connect)
            data =  socket_sub.recv(flags=zmq.NOBLOCK)
            print data.split()[1]
            #print data[1:]

        except zmq.Again:
            pass
    
    return True


if __name__ == '__main__':
    zmq_client_data_listen_website()
