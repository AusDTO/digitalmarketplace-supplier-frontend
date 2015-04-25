from flask_login import login_required
from app.main import main
from flask import render_template, session


@main.route('/dashboard')
@login_required
def dashboard():
    template_data = main.config['BASE_TEMPLATE_DATA']
    return render_template(
        "services/dashboard.html",
        **template_data), 200


@main.route('/services')
@login_required
def services():
    template_data = main.config['BASE_TEMPLATE_DATA']
    return render_template(
        "services/services.html",
        **template_data), 200
