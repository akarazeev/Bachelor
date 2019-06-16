import pandas as pd
import argparse
import os
import numpy
from db_communication.db_queries import create_file


def type_column(s):
	if type(s) == int:
		return 'INT'
	if type(s) == str:
		return 'VARCHAR(20)'
	if type(s) == numpy.int64:
		return 'INT'
	return 'FLOAT'


def upload(filepath, user_id=1):
	"""
	Receive `filepath`. As for now, work only with .csv files.
	Parse the file and create a query to db to create and fill the table.

	:param filepath:
	:param user_id:
	:return: ID of the created table.

	"""
	# Check extension of the file.
	file_extension = os.path.splitext(filepath)[1]
	if file_extension == '.csv':
		input = pd.read_csv(filepath)
		column_names = list(input.columns._data)
		column_names = list(map(lambda x: '"{}"'.format(x), column_names))
		filename = os.path.basename(filepath)
		first_str = list(input.iloc[0])
		column_types = [type_column(e) for e in first_str]
		# Send a query to db to create table corresponding to the passed file.
		file_id = create_file(user_id, filename, input, column_names, column_types)
		return file_id
