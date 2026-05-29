# routes/dashboard.py
from flask import Blueprint, render_template, session, current_app, flash, redirect, url_for
from utils.security import login_required
from utils.db import get_db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required  # Restricts route access solely to authenticated active users
def user_dashboard():
    """
    Serves the regular client dashboard workspace metrics interface.
    Fetches the user's micro-savings balance matrix from the database, 
    calculates progress towards the 500 BDT activation threshold, and 
    displays emergency service dispatch triggers.
    """
    try:
        db = get_db()
        user_id = session.get('user_id')

        # 1. Database Query: Pulling the user's specific 10% phone recharge savings balance
        # Fetches transaction-ready funds linked to the registered SIM identifier
        savings_data = db.execute(
            "SELECT balance, min_threshold FROM savings_accounts WHERE user_id = ?", 
            (user_id,)
        ).fetchone()

        # Fallback handler if a savings profile hasn't been instantiated yet
        current_balance = savings_data['balance'] if savings_data else 0.0
        threshold_limit = savings_data['min_threshold'] if savings_data else 500.0

        # 2. Business Logic Evaluation: Checking the strict 500 BDT unlocking parameter
        # Flags true if the user is authorized to order medicines, call doctors, or request ambulances
        is_eligible = current_balance >= threshold_limit

        # 3. UI Matrix Calculation: Computes percentage metrics for the frontend progress bar
        progress_percentage = min(int((current_balance / threshold_limit) * 100), 100)

        # Rendering the layout component payload directly to the Jinja2 engine
        return render_template(
            "dashboard/index.html", 
            name=session.get('user_name'),
            balance=current_balance,
            eligible=is_eligible,
            progress=progress_percentage
        )

    except Exception as e:
        # Encapsulated application-level diagnostic logger to prevent system tracing on client side
        current_app.logger.error(f"Dashboard Pipeline Processing Execution Failure: {str(e)}")
        flash("Failed to securely stream user financial dashboard telemetry.", "danger")
        return redirect(url_for('auth.login'))
