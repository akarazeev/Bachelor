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


# вход - получает путь к файлу(пока только с расширением .csv)
# цель - распарсить файл и сделать запрос к БД для создания таблицы и ее заполнения
# выход - название таблицы в БД
def upload(filepath, user_id=1):
	# проверить файл
	file_extension = os.path.splitext(filepath)[1]
	if file_extension == '.csv':
		# выделить название столбцов и матрицу значений
		input = pd.read_csv(filepath)
		column_names = list(input.columns._data) # название колонок нашей таблицы
		filename = os.path.basename(filepath)
		first_str = list(input.iloc[0])
		column_types = [type_column(e) for e in first_str]
		# удалить файл из системы
		os.remove(filepath)
		# сделать запрос к БД для создания таблицы(передать матрицу значений и название столбцов)
		file_id = create_file(user_id, filename, input, column_names, column_types)
		# возвратить название таблицы в БД
		return file_id
