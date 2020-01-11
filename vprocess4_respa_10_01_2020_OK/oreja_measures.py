import time, zmq
tau_zmq_connect = 0.05

def zmq_client():
    #####Listen measures
    port_sub = "5557"
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    socket_sub.connect ("tcp://localhost:%s" % port_sub)
    topicfilter = "w"#"w"
    socket_sub.setsockopt(zmq.SUBSCRIBE, topicfilter)

    while 1:
        #espero y retorno valor
        time.sleep(tau_zmq_connect)
        data = socket_sub.recv()

        print "largo de data: ", len(data)
        print data
'''
        try:
            text = data.split()
            #print text[9]
        except:
            print "vacio"
'''
if __name__=='__main__':
    zmq_client()
