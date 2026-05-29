# routes/dashboard.py
from flask import Blueprint, render_template, session
from utils.security import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required  # Restricts route access solely to authenticated active users
def user_dashboard():
    """Serves the regular client dashboard workspace metrics interface."""
    return render_template("dashboard/index.html", name=session['user_name'])
