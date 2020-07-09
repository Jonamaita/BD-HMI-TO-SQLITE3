# BD HMI TO Sqlite3.

Este pequeño script nos permite ordenar la base de datos (Mantos producidos) descargada de una HMI KINCO MT4434T. 

Crea una base de datos nueva de manera que podemos copiar los datos y pegarlo en excel de una manera mas presentable.

# Script Plot

El script "plot.py", grafica una producción de mantos en un turno de 12 o 24 horas en un rango de fecha dado por el usuario.

El rango de fecha solo puede ser de 24 horas.

**Ejemplo:**

Un rango de fecha desde **08-07-2020** hasta el **09-07-2020**

## Para correr el script plot.py:

### Opción 1

Si no se especifica la fecha al ejecutar el Script, tomara un rango de **ayer** hasta **hoy**.

```bash
python plot.py
```

### Opción 2 

Especificando la fecha al ejecutar el Script. La fecha debe estar en formato **dd-mm-aaaa**.

```bash
python plot.py 08-07-2020 09-07-2020
```

