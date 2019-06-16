from flask import (
    request,
    render_template,
    session,
    send_from_directory,
    redirect,
    url_for,
)
from app import app

from app.forms import UploadFileForm, GraphSettingsForm, AnomaliesForm, DataOverviewForm
from app.utils import get_json_data, get_header, get_values
from db_communication import file_processing
from plot_charts import plot_df, plot_anomalies

from werkzeug.utils import secure_filename
import os

selected_dataset = None
last_dataset = None


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    global selected_dataset, last_dataset
    # ^ it's bad decision...

    if selected_dataset is None:
        selected_dataset = request.args.get("dataset")
        if selected_dataset is not None:
            last_dataset = selected_dataset
            return redirect(url_for(".index"))

    header = None
    if session.get("current_data") is not None:
        header = get_header(session["current_data"])

    graph_settings_form = GraphSettingsForm(header)
    anomalies_settings_form = AnomaliesForm(header)
    dataoverview_form = DataOverviewForm(header)
    upload_form = UploadFileForm()

    kwargs = dict(
        upload_form=upload_form,
        graph_settings_form=graph_settings_form,
        anomalies_settings_form=anomalies_settings_form,
        dataoverview_form=dataoverview_form,
        header=header,
    )

    def _get_axes():
        """
        Return selected columns to draw plots with.
        :return: (axis_x, axis_y)

        """
        return (
            dict(graph_settings_form.axis_x.choices)[graph_settings_form.axis_x.data],
            dict(graph_settings_form.axis_y.choices)[graph_settings_form.axis_y.data],
        )

    def _filesize(path):
        fs = os.path.getsize(path)
        m = "B"
        if fs > 1025:
            fs /= 1024
            m = "KB"
        if fs > 1025:
            fs /= 1024
            m = "MB"
        if fs > 1025:
            fs /= 1024
            m = "GB"
        fs = round(fs)
        res = "{} {}".format(str(fs), m)
        return res

    # Display content of dataset.
    if upload_form.validate_on_submit() or selected_dataset is not None:
        if selected_dataset is not None:
            uploaded_file = os.path.join("uploads", selected_dataset)
            session["current_data"] = get_json_data(uploaded_file)
        else:
            uploaded_file = upload_form.uploaded_file.data
            session["current_data"] = get_json_data(uploaded_file)

        header = get_header(session["current_data"])
        values = get_values(session["current_data"])

        graph_settings_form.change_choices(header)
        anomalies_settings_form.change_choices(header)

        kwargs.update(
            graph_settings_form=graph_settings_form,
            anomalies_settings_form=anomalies_settings_form,
            header=header,
            data=values,
            dim=len(header) - 2,
        )

        if selected_dataset is not None:
            session["current_file_id"] = save_uploaded_file(uploaded_file, skip=True)
            kwargs.update(dataset=selected_dataset)
            selected_dataset = None
        else:
            session["current_file_id"] = save_uploaded_file(uploaded_file)
            kwargs.update(dataset=upload_form.uploaded_file.data.filename)

        return render_template("showcsv.html", **kwargs)

    # Simple plots.
    if graph_settings_form.submit_graph.data:
        axis_x, axis_y = _get_axes()

        filename = plot_df.naive_plot_df(session["current_file_id"], axis_x, axis_y)
        kwargs.update(filename=filename, axis_x=axis_x, axis_y=axis_y)

        return render_template("showgraph.html", **kwargs)

    # Anomaly Detection.
    if anomalies_settings_form.submit_anomalies.data:
        axis_x, axis_y = _get_axes()

        filename_simple_plot = plot_anomalies.simple_plot(
            session["current_file_id"], axis_x, axis_y
        )
        filename_simple_anomalies = plot_anomalies.simple_anomalies(
            session["current_file_id"], axis_x, axis_y
        )
        filename_data_overview = plot_anomalies.data_overview(
            session["current_file_id"], dataset_title=last_dataset
        )

        kwargs.update(
            axis_x=axis_x,
            axis_y=axis_y,
            filename_simple_plot=filename_simple_plot,
            filename_simple_anomalies=filename_simple_anomalies,
            filename_data_overview=filename_data_overview,
        )

        return render_template("showanomalies.html", **kwargs)

    # Data Overview.
    if dataoverview_form.validate_on_submit():
        axis_x, axis_y = _get_axes()

        filename_data_overview = plot_anomalies.data_overview(
            session["current_file_id"], dataset_title=last_dataset
        )

        kwargs.update(
            filename_data_overview=filename_data_overview, axis_x=axis_x, axis_y=axis_y
        )

        return render_template("showdataoverview.html", **kwargs)

    datasets = sorted(os.listdir("uploads/"), key=str.lower)
    datasets = list(filter(lambda x: x.startswith(".") is False, datasets))

    datasets = list(map(lambda x: (x, _filesize(os.path.join("uploads", x))), datasets))
    kwargs.update(datasets=datasets)

    return render_template("showdatasets.html", **kwargs)


@app.route("/images/<filename>")
def get_image_file(filename):
    return send_from_directory(app.config["IMAGE_FOLDER"], filename)


def save_uploaded_file(uploaded_file, skip=False):
    if skip:
        file_id = file_processing.upload(uploaded_file)
    else:
        filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        uploaded_file.stream.seek(0)
        uploaded_file.save(filepath)
        file_id = file_processing.upload(filepath)
    return file_id
