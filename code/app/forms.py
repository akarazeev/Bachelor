from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import SubmitField, SelectField


class UploadFileForm(FlaskForm):
	uploaded_file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'Only csv!')])
	submit = SubmitField(label='Загрузить')


class GraphSettingsForm(FlaskForm):
	axis_x = SelectField(label="Первая координата")
	axis_y = SelectField(label="Вторая координата", choices=[])
	submit = SubmitField('Show Graph')

	submit_graph = SubmitField(label='Показать')

	def __init__(self, header, *args, **kwargs):
		super(GraphSettingsForm, self).__init__(*args, **kwargs)
		
		if header is not None:
			axes = [(col_name, col_name) for col_name in header if col_name != 'Index']
		else:
			axes = []

		self.axis_x.choices = axes
		self.axis_y.choices = axes

	def change_choices(self, axes):
		axes = [(col_name, col_name) for col_name in axes if col_name != 'Index']
		
		self.axis_x.choices = axes
		self.axis_y.choices = axes


class AnomaliesForm(FlaskForm):
	axis_x = SelectField(label="Ось X")
	axis_y = SelectField(label="Ось Y", choices=[])
	submit = SubmitField('Detect Anomalies')

	submit_anomalies = SubmitField('Показать')

	def __init__(self, header, *args, **kwargs):
		super(AnomaliesForm, self).__init__(*args, **kwargs)

		if header is not None:
			axes = [(col_name, col_name) for col_name in header if col_name != 'Index']
		else:
			axes = []

		self.axis_x.choices = axes
		self.axis_y.choices = axes

	def change_choices(self, axes):
		axes = [(col_name, col_name) for col_name in axes if col_name != 'Index']

		self.axis_x.choices = axes
		self.axis_y.choices = axes
