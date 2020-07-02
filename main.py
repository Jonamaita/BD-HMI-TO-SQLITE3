import sqlite3
import os
import time
import os.path as path
import sys  # importar opciones de nuestro sistema

class Manto(object):
	"""
	Manto object that composed of the number of manto, 
	date of manufactoring and hour of manufactoring.

	To initialize:
	:param number_manto: number manto
	:param date: date manufactoring manto
	:param hour: hour manufactoring manto

	USAGE:
		>>> manto = Manto(number_manto=1, date='01-06-2020', hour='16:00:00')
	"""

	def __init__ (self, number_manto:int, date:str, hour:str):
		self.number_manto = number_manto
		self.date = date
		self.hour = hour

class Produccion(object):
	"""
	Produccion is object that manipulate information of mantos.
	
	USAGE:
		>>>produccion = Produccion()
		>>>produccion.get_data_db() # it is a method for get data from a data base.
		>>>produccion.create_new_data_base() # it is a method for create a new database with field id, number_manto, date,hour.
		>>>produccion.update_data_base() # it is a method for update data of a existing data base. 
	"""
	def __init__ (self):
		self.mantos : List[Manto] = []
	
	def get_data_db(self, name_data_base:str) -> None:
		aux = []
		if path.exists(name_data_base):
			try:
				conexion = sqlite3.connect(name_data_base)
				c = conexion.cursor()
				query = c.execute('SELECT * FROM SrcDat')
				for row in query:
					aux = row[0].split(" ")
					date = aux[0]
					hour = aux[1][0:8]
					number_manto = row[1]
					manto = Manto (number_manto = number_manto, date = date, hour = hour)
					self.mantos.append(manto)
				conexion.close()
			except sqlite3.OperationalError as error:
				print(f'Error: {error}')
				time.sleep(5)
		else:
			print('La base de dato "{name_data_base}" no existe')
		
	def create_new_data_base(self, name_new_data_base:str):
		if not path.exists  (name_new_data_base):
			try:
				conexion = sqlite3.connect(name_new_data_base)
				c = conexion.cursor()
				c.execute("""create table mantos (
										id INTEGER PRIMARY KEY AUTOINCREMENT,
										number_manto INT,
										date DATE,
										hour TIME						
									)""")
				print("se creo la tabla exitosamente")
				total = len(self.mantos)
				for index,manto in enumerate(self.mantos):
					c.execute("insert into mantos(date,hour,number_manto) values (?,?,?)",
									(manto.date, manto.hour, manto.number_manto))
					prog = index * 100 / total
					# Imprimimos en la consola el progreso del llenado de la base de dato
					sys.stdout.write("\r%d %% Progreso" % prog)
					sys.stdout.flush()
					time.sleep(0.01)
				conexion.commit()
				conexion.close()
				sys.stdout.write(f'\nSe guardaron los datos en la base de datos {name_new_data_base} exitosamente')
				sys.stdout.flush()
			except sqlite3.OperationalError as error:
				print(f'Error: {error} ')
				time.sleep(5)
		else:
			print(f'El nombre de la base de datos {name_new_data_base} ya existe')
			response = str(input(f"""Quiere sobre escribir la base de datos {name_new_data_base}? : 
				Presione s/n:
				[s]i
				[n]o
				 """))
			if response == 's':
				self.update_data_base(name_new_data_base)

	def update_data_base(self,name_data_base):
		try:
			conexion = sqlite3.connect(name_data_base)
			c = conexion.cursor()
			total = len(self.mantos)
			for index,manto in enumerate(self.mantos):
				c.execute("insert into mantos(date,hour,number_manto) values (?,?,?)",
								(manto.date, manto.hour, manto.number_manto))
				prog = index * 100 / total
				# Imprimimos en la consola el progreso del llenado de la base de dato
				sys.stdout.write("\r%d %% Progreso" % prog)
				sys.stdout.flush()
				time.sleep(0.01)
			conexion.commit()
			conexion.close()
			sys.stdout.write(f'\nSe actualizaron los datos de la base de datos {name_data_base} exitosamente')
			sys.stdout.flush()	
		except sqlite3.OperationalError as error:
			print(f'Error: {error}')
			time.sleep(5)

def main():
	name_data_base_hmi = 'SampleDataStore.db'
	name_new_data_base = 'SampleDataStore_Split.db'
	produccion = Produccion()
	produccion.get_data_db(name_data_base_hmi)
	produccion.create_new_data_base(name_new_data_base)


if __name__ == '__main__':
	main()