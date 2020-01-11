#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
Syntaxis:
	argv[1] =: indica el archivo .db a desplegar
	argv[2] =: indica la tabla de la db a desplegar
	python desplegar_DB.py NOMBRE_BASE_DATOS.db NOMBRE_DE_LA_TABLA
'''


import sys, sqlite3

#FILE_DB, TABLE_DB is TEXT.
#FIRST_ELEMENT, LAST_ELEMENT is INTEGER.
def window_db(FILE_DB,TABLE_DB, dt):

	db = sqlite3.connect(FILE_DB)
	c = db.cursor()

	SELECT_TABLE = 'SELECT * FROM ' + TABLE_DB
	c.execute(SELECT_TABLE)


	j = 1
	temporal = {}
	for i in c:
		temporal[j] = [ i[1][:-7], i[2] ]
		j+=1

	c.close()
	db.close()


	i=1
	temp = {}
	while i<=len(temporal)/dt:
		temp[i]=temporal[i*dt]
		i+=1


	return temp


def main():
	DATA_LOG = {}

	db = sqlite3.connect(str(sys.argv[1]))
	c = db.cursor()

	#SELECT_TABLE = 'SELECT FECHA_HORA as "ts [TIMESTAMP]", MAGNITUD FROM  ' + str(sys.argv[2])
	SELECT_TABLE = 'SELECT * FROM ' + str(sys.argv[2])
	c.execute(SELECT_TABLE)

	j = 0
	for i in c:
	#	print i[0], i[1] , i[2], "\n"
		DATA_LOG[j]= [ i[0], i[1] , i[2] ]
		j+=1

	c.close()
	db.close()

	for i in range(0,len(DATA_LOG)):
		print DATA_LOG[i]



if __name__ == '__main__':
	main()
