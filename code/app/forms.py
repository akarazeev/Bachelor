from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import SubmitField, SelectField


def prepare_axes(axes):
    res = list()
    if axes is not None:
        res = [(str(i), col_name) for i, col_name in enumerate(axes)]
    return res


class UploadFileForm(FlaskForm):
    uploaded_file = FileField(
        validators=[FileRequired(), FileAllowed(["csv"], "Only csv!")]
    )
    submit = SubmitField(label="Загрузить")


class SimpleGraphForm(FlaskForm):
    axis_x = SelectField(label="Первая координата", choices=[], default=2)
    axis_y = SelectField(label="Вторая координата", choices=[], default=3)

    submit_graph = SubmitField(label="Показать")
    submit = SubmitField("Show Graph")

    def __init__(self, header, *args, **kwargs):
        super(SimpleGraphForm, self).__init__(*args, **kwargs)

        axes = prepare_axes(header)
        self.axis_x.choices = axes
        self.axis_y.choices = axes

    def change_choices(self, axes):
        axes = prepare_axes(axes)
        self.axis_x.choices = axes
        self.axis_y.choices = axes


class AnomaliesForm(FlaskForm):
    selected_algorithm = SelectField(label="Метод поиска аномалий", default=0)
    submit_anomalies = SubmitField("Показать")
    submit = SubmitField("Detect Anomalies")

    def __init__(self, algorithms, *args, **kwargs):
        super(AnomaliesForm, self).__init__(*args, **kwargs)
        algorithms = prepare_axes(algorithms)
        self.selected_algorithm.choices = algorithms

    def change_choices(self, algorithms):
        algorithms = prepare_axes(algorithms)
        self.selected_algorithm.choices = algorithms


class DataOverviewForm(FlaskForm):
    submit_dataoverview = SubmitField("Показать данные")
    submit = SubmitField("Build overview")

    def __init__(self, *args, **kwargs):
        super(DataOverviewForm, self).__init__(*args, **kwargs)
