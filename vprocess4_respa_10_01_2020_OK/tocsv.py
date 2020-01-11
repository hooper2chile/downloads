import csv, sqlite3, sys

#python aer2.py testa.db 10
def csv_file(FILE_DB, dt):

    db = sqlite3.connect( FILE_DB )
    c  = db.cursor()

    FILE_CSV = '/home/pi/vprocess4/csv/' + FILE_DB[28:-3] + 'T=' + str(dt) + '.csv'

    ################# SOMBRERO ########################
    c.execute('SELECT * FROM T_SOMBRERO')
    j = 1
    temporal = {}
    #dt = int(sys.argv[2])

    for i in c:
        temporal[j] = [ i[1][:-7], i[2] ]
        j+=1

    ###################################################
    i=1
    temp = {}
    while i<=len(temporal)/dt:
        temp[i]=temporal[i*dt]
        i+=1
    ###################################################

    with open(FILE_CSV, 'a+') as fp:
        a = csv.writer(fp)
        k=1
        data = []
        a.writerow( ['date hour', 'T_SOMBRERO'] )
        for k in range(1,len(temp)):
            data += [temp[k]]
        a.writerows(data)




    #################  MOSTO  ########################
    c.execute('SELECT * FROM T_MOSTO')
    j = 1
    temporal = {}
    #dt = int(sys.argv[2])

    for i in c:
        temporal[j] = [ i[1][:-7], i[2] ]
        j+=1

    #################################################
    i=1
    temp = {}
    while i<=len(temporal)/dt:
        temp[i]=temporal[i*dt]
        i+=1
    #################################################

    with open(FILE_CSV, 'a+') as fp:
        a = csv.writer(fp)
        k=1
        data = []
        a.writerow( [''] )
        a.writerow( ['date hour', 'T_MOSTO'] )
        for k in range(1,len(temp)):
            data += [temp[k]]
        a.writerows(data)

    #################  PROMEDIO  ##########################
    c.execute('SELECT * FROM T_PROMEDIO')
    j = 1
    temporal = {}
    #dt = int(sys.argv[2])

    for i in c:
        temporal[j] = [ i[1][:-7], i[2] ]
        j+=1

    ################################################
    i=1
    temp = {}
    while i<=len(temporal)/dt:
        temp[i]=temporal[i*dt]
        i+=1
    ################################################

    with open(FILE_CSV, 'a+') as fp:
        a = csv.writer(fp)
        k=1
        data = []
        a.writerow( [''] )
        a.writerow( ['date hour', 'T_PROMEDIO'] )
        for k in range(1,len(temp)):
            data += [temp[k]]
        a.writerows(data)

    c.close()
    db.close()
