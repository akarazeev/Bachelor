import pandas as pd


def get_json_data(file):
	df = pd.read_csv(file, nrows=15)
	return df.to_json()


def get_header(json_data):
	return pd.read_json(json_data).columns


def get_values(json_data):
	return pd.read_json(json_data).values
