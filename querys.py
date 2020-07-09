import sqlite3
from datetime import  timedelta,date,datetime
import time

class Query:

	def __init__(self,name_db: str):
		"""
		Query object that is composed of the name_db.

		To initialize:
		:param name_db: name of data base

		USAGE:
			>>> query = Query(name='SampleDataStore_Split.db')
			>>> quatity = query.quatity_mantos_range_hour(range_hour=ranges,range_date=('2018-12-27','2018-12-28'))
			>>> max_date = query.max_date()
			>>> min_date = qury.min_date()
		"""

		self.name_db = name_db

	def max_date(self):
		"""
		This method return the max date of production that the data base have
		"""
		try:
			conexion = sqlite3.connect(self.name_db)
			c = conexion.cursor()
			query = c.execute('SELECT MAX(date) from mantos')
			max_date = query.fetchone()
			max_date = max_date[0]
			return max_date
		except sqlite3.OperationalError as error:
			print(f'Error: {error}')
			time.sleep(5)
		finally:
			conexion.close()

	def min_date(self):
		"""
		This method return the min date of production that the data base have
		"""
		try:
			conexion = sqlite3.connect(self.name_db)
			c = conexion.cursor()
			query = c.execute('SELECT min(date) from mantos')
			min_date = query.fetchone()
			min_date = min_date[0]
			return min_date
		except sqlite3.OperationalError as error:
			print(f'Error: {error}')
			time.sleep(5)
		finally:
			conexion.close()

	def quatity_mantos_range_hour(self,range_hour:tuple,range_date:tuple)->int:
		"""
		This method returns the quantity of mantos produced in a range of hour and range of date
		"""
		try:
			conexion = sqlite3.connect(self.name_db)
			c = conexion.cursor()
			query = c.execute(f'SELECT COUNT(id)  FROM mantos WHERE date BETWEEN \
								"{range_date[0]}" AND "{range_date[1]}" AND hour BETWEEN "{range_hour[0]}" AND "{range_hour[1]}" ')
			quantity = query.fetchone()
			quantity = quantity[0]
			return quantity
		except sqlite3.OperationalError as error:
			print(f'Error: {error}')
			time.sleep(5)
		finally:
			conexion.close()

def main():
	now = datetime.now().date()
	yesterday = now - timedelta(days=1)
	query = Query('SampleDataStore_Split.db')
	data = list()
	ranges_hours = [
		('08:00:00','08:59:59'), ('09:00:00','09:59:59'), ('10:00:00','10:59:59'),
		('11:00:00','11:59:59'), ('12:00:00','12:59:59'), ('13:00:00','13:59:59'),
		('14:00:00','14:59:59'), ('15:00:00','15:59:59'), ('16:00:00','16:59:59'),
		('17:00:00','17:59:59'), ('18:00:00','19:00:00'),
	]
	for ranges in ranges_hours:
		x = query.quatity_mantos_range_hour(range_hour=ranges,range_date=('2018-12-27','2018-12-28'))
		data.append(x)
	
	print(data)


if __name__ == '__main__':
	main()