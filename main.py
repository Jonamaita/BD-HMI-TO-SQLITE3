import sqlite3
import os
import time
import sys  # importar opciones de nuestro sistema
fechas = []
horas = []
num_manto = []
arreglo = []
i = 0
try:
    conexion = sqlite3.connect('SampleDataStore.db')
    c = conexion.cursor()
    query = c.execute('SELECT * FROM SrcDat')
    for row in query:
        arreglo = row[0].split(" ")
        fechas.insert(i, arreglo[0])
        horas.insert(i, arreglo[1][0:8])
        num_manto.insert(i, row[1])
        i = i + 1
    conexion.close()
    conexion = sqlite3.connect('SampleDataStore_Separado.db')
    c = conexion.cursor()
    c.execute("""create table mantos (
                              fecha date,
                              hora time,
                              num_manto
                              
                        )""")
    print("se creo la tabla exitosamente")
    time.sleep(5)
    total = len(num_manto)
    for x in range(0, len(num_manto)):
        conexion.execute("insert into mantos(fecha,hora,num_manto) values (?,?,?)",
                         (fechas[x], horas[x], num_manto[x]))
        prog = x * 100 / total
        # Imprimimos en la consola el progreso del llenado de la base de dato
        sys.stdout.write("\r%d %% Progreso" % prog)
        sys.stdout.flush()
        time.sleep(0.01)

    conexion.commit()
    conexion.close()
    sys.stdout.write("\nSe guardaron los datos en la base de datos exitosamente")
    sys.stdout.flush()
    time.sleep(5)

except sqlite3.OperationalError as error:
    print(error)
    time.sleep(5)
