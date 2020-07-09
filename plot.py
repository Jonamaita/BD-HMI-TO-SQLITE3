from bokeh.io import output_file, show
from bokeh.models import FactorRange, LabelSet, ColumnDataSource
from bokeh.plotting import figure
import numpy as np
from typing import Dict,List
from querys import Query
from datetime import timedelta,datetime
import sys


class DailyChart(object):

	def __init__(self,data: List, file_name ="bar_mixed.html", turns = False):
		"""
		DailyChart object that is composed of the data, file_name, turns

		To initialize:
		:param data: data for build the chart
		:param file_name: name with which the html file will be created
		:param turns: if the productions have work shifts

		USAGE:
			>>>	chart = DailyChart(data = x)
			>>>	chart.createChart()
		"""
		self.file_name = file_name
		self.factors = self._factors(turns)
		self.data = data

	def createChart(self,height=700,width=1080):
		"""
		This method create the chart.

		:param height: Height chart
    	:param width: width chart

    	:return: None
		"""
		output_file = self.file_name
		p = figure(x_range=FactorRange(*self.factors), plot_height=height,plot_width=width)
		source = ColumnDataSource(dict(x=[*self.factors],y=self.data))
		p.vbar(x=self.factors, top=x, width=0.9, alpha=0.5)
		labels = LabelSet(x='x',y='y', text='y', level='glyph', x_offset=-10, y_offset=5, source=source, 
							render_mode='canvas', text_baseline='bottom')
		p.add_layout(labels)
		p.y_range.start = 0
		p.x_range.range_padding = 0.1
		p.xaxis.axis_label="Mantos Por Hora"
		p.xaxis.major_label_orientation = 1
		p.xgrid.grid_line_color = None
		p.yaxis.axis_label="Mantos Fabricados"
		show(p)

	def _factors(self,turns:bool)-> List:
		"""
		This method return a list wioth the ranges of hours for build the chart.

		:param turns: If True, the range of production is  24 hours

    	:return: List with the hours
		"""
		if turns:
			hours = [
				("8:00 - 9:00"), ("9:00 - 10:00"), ("10:00 - 11:00"),
				("11:00 - 12:00 "), ("12:00 - 13:00"), ("13:00 - 14:00"),
				("14:00 - 15:00"), ("15:00 - 16:00"), ("16:00 - 17:00"),
				("17:00 - 18:00"), ("18:00 - 19:00"), ("19:00 - 20:00"),
				("20:00 - 21:00"), ("21:00 - 22:00"), ("22:00 - 23:00"),
				("00:00 - 01:00"), ("01:00 - 02:00"), ("02:00 - 03:00"),
				("03:00 - 04:00"), ("04:00 - 05:00"), ("05:00 - 06:00"),
				("06:00 - 07:00"), ("07:00 - 08:00")
			]
		else:
			hours = [
				("8:00 - 9:00"), ("9:00 - 10:00"), ("10:00 - 11:00"),
				("11:00 - 12:00 "), ("12:00 - 13:00"), ("13:00 - 14:00"),
				("14:00 - 15:00"), ("15:00 - 16:00"), ("16:00 - 17:00"),
				("17:00 - 18:00"), ("18:00 - 19:00"),
			]
		
		return hours


def date_format(date:str) ->str:
	"""
	This function format the date of user "d,m,y" in format "y,m,d".

	:param date: date to format

	:return: String with date in format year, month, day
	"""
	try:
		format_str = '%d-%m-%Y'  # format_user
		datetime_obj = datetime.strptime(date, format_str)
		return datetime_obj.strftime('%Y-%m-%d')
	except ValueError as e:
		print ("Formato de fecha incorrecto: " + str(e))
		exit(1)


def get_data(date_gte, date_lte, turns:bool = False) -> List:
	"""
	This function get data from the database in the date range that user request

	:param date_gte: start date
	:param date_lte: end date 

	:return: List with the data

	"""
	query = Query('SampleDataStore_Split.db')
	data = list()
	if turns:
		ranges_hours = [
			('08:00:00','08:59:59'), ('09:00:00','09:59:59'), ('10:00:00','10:59:59'),
			('11:00:00','11:59:59'), ('12:00:00','12:59:59'), ('13:00:00','13:59:59'),
			('14:00:00','14:59:59'), ('15:00:00','15:59:59'), ('16:00:00','16:59:59'),
			('17:00:00','17:59:59'), ('18:00:00','18:59:59'), ('19:00:00','19:59:59'),
			('20:00:00','20:59:59'), ('21:00:00','21:59:59'), ('22:00:00','22:59:59'),
			('23:00:00','23:59:59'), ('00:00:00','00:59:59'), ('01:00:00','01:59:59'),
			('02:00:00','02:59:59'), ('03:00:00','03:59:59'), ('04:00:00','04:59:59'),
			('05:00:00','05:59:59'), ('06:00:00','06:59:59'), ('07:00:00','07:59:59'),
		]
	
	else:
		ranges_hours = [
			('08:00:00','08:59:59'), ('09:00:00','09:59:59'), ('10:00:00','10:59:59'),
			('11:00:00','11:59:59'), ('12:00:00','12:59:59'), ('13:00:00','13:59:59'),
			('14:00:00','14:59:59'), ('15:00:00','15:59:59'), ('16:00:00','16:59:59'),
			('17:00:00','17:59:59'), ('18:00:00','19:00:00'),
		]

	for ranges in ranges_hours:
		x = query.quatity_mantos_range_hour(range_hour=ranges,range_date=(date_gte,date_lte))
		data.append(x)


	return data

if __name__ == '__main__':
	if len(sys.argv) ==3:
		date_gte = date_format(sys.argv[1]) # Start date
		date_lte = date_format(sys.argv[2]) # end date
	else:
		date_lte = datetime.now().date() # end date (today)
		date_gte = date_lte - timedelta(days=1) # start date (yesterday)

	x = get_data(date_gte=date_gte,date_lte = date_lte)
	chart = DailyChart(data = x)
	chart.createChart()