from flask import request, render_template, session, send_from_directory
from app import app

from app.forms import UploadFileForm, GraphSettingsForm, AnomaliesForm
from app.utils import get_json_data, get_header, get_values
from db_communication import file_processing
from plot_charts import plot_df, karazeev_plot

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage, Headers
import pandas as pd

import sys
import os


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	selected_dataset = request.args.get('dataset')
	print(selected_dataset)

	header = None
	if session.get("current_data") is not None:
		header = get_header(session["current_data"])

	graph_settings_form = GraphSettingsForm(header)
	anomalies_settings_form = AnomaliesForm(header)
	upload_form = UploadFileForm()

	if upload_form.validate_on_submit() or selected_dataset is not None:
		if selected_dataset is not None:
			session["current_data"] = get_json_data('uploads/{}'.format(selected_dataset))
			d = Headers()
			d.add('Content-Disposition', 'form-data; name="uploaded_file"; filename="{}"'.format(selected_dataset))
			d.add('Content-Type', 'text/csv')
			uploaded_file = FileStorage(filename=selected_dataset, content_type='text/csv', headers=d)
			uploaded_file.name = 'uploaded_file'
		else:
			uploaded_file = upload_form.uploaded_file.data
			session["current_data"] = get_json_data(uploaded_file)

		header = get_header(session["current_data"])
		values = get_values(session["current_data"])

		graph_settings_form.change_choices(header)
		anomalies_settings_form.change_choices(header)

		session["current_file_id"] = save_uploaded_file(uploaded_file)

		return render_template(
			'showcsv.html',
			dataset=upload_form.uploaded_file.data.filename,
			upload_form=upload_form,
			graph_settings_form=graph_settings_form,
			anomalies_settings_form=anomalies_settings_form,
			header=header,
			data=values
		)

	# naive_plot_df
	if graph_settings_form.submit_graph.data and graph_settings_form.validate_on_submit():
		axis_x = graph_settings_form.axis_x.data
		axis_y = graph_settings_form.axis_y.data

		filename = plot_df.naive_plot_df(session["current_file_id"], axis_x, axis_y, columns=header)

		return render_template(
			"showgraph.html",
			upload_form=upload_form,
			graph_settings_form=graph_settings_form,
			anomalies_settings_form=anomalies_settings_form,
			filename=filename
		)

	# Anomaly Detection.
	if anomalies_settings_form.submit_anomalies.data and anomalies_settings_form.validate_on_submit():
		axis_x = anomalies_settings_form.axis_x.data
		axis_y = anomalies_settings_form.axis_y.data

		filename_simple_plot = karazeev_plot.simple_plot(session["current_file_id"], axis_x, axis_y, columns=header)
		filename_simple_anomalies = karazeev_plot.simple_anomalies(session["current_file_id"], axis_x, axis_y, columns=header)

		return render_template(
			"showanomalies.html",
			upload_form=upload_form,
			graph_settings_form=graph_settings_form,
			anomalies_settings_form=anomalies_settings_form,
			filename_simple_plot=filename_simple_plot,
			filename_simple_anomalies=filename_simple_anomalies,
			axis_x=axis_x,
			axis_y=axis_y
		)

	datasets = sorted(os.listdir("uploads/"))
	datasets = list(filter(lambda x: x.startswith('.') == False, datasets))

	return render_template(
		'showdatasets.html',
		datasets=datasets,
		upload_form=upload_form,
		graph_settings_form=graph_settings_form,
		anomalies_settings_form=anomalies_settings_form
	)


@app.route('/images/<filename>')
def get_image_file(filename):
	return send_from_directory(app.config['IMAGE_FOLDER'], filename)


@app.route('/anomalies/<filename>')
def get_anomalies_file(filename):
	return send_from_directory(app.config['IMAGE_FOLDER'], filename)


def save_uploaded_file(uploaded_file):
	filename = secure_filename(uploaded_file.filename)
	filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	uploaded_file.stream.seek(0)
	uploaded_file.save(filepath)
	file_id = file_processing.upload(filepath)

	return file_id

