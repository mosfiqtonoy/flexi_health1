from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from utils.security import login_required
from services.user_service import get_user_profile, update_user_profile, add_recharge, get_recharge_history
from services.dashboard_service import add_health_record, get_health_records, submit_service_request, get_service_requests, get_dashboard_summary

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@login_required
def home():
    user_id = session.get("user_id")
    user = get_user_profile(user_id)
    summary = get_dashboard_summary(user_id)
    recent_records = get_health_records(user_id, limit=5)
    return render_template("dashboard/index.html", user=user, summary=summary, records=recent_records)

@dashboard_bp.route("/health", methods=["GET", "POST"])
@login_required
def health():
    user_id = session.get("user_id")
    if request.method == "POST":
        weight = request.form.get("weight") or None
        height = request.form.get("height") or None
        bp_sys = request.form.get("bp_systolic") or None
        bp_dia = request.form.get("bp_diastolic") or None
        blood_type = request.form.get("blood_type") or None
        notes = request.form.get("notes") or None
        try:
            add_health_record(user_id, weight, height, bp_sys, bp_dia, blood_type, notes)
            flash("Health record saved successfully.", "success")
        except Exception:
            flash("Failed to save health record.", "danger")
        return redirect(url_for("dashboard.health"))
    
    user = get_user_profile(user_id)
    records = get_health_records(user_id)
    return render_template("dashboard/health.html", user=user, records=records)

@dashboard_bp.route("/requests", methods=["GET", "POST"])
@login_required
def requests_view():
    user_id = session.get("user_id")
    if request.method == "POST":
        service_type = request.form.get("service_type", "").strip()
        description = request.form.get("description", "").strip()
        try:
            amount_used = float(request.form.get("amount_used") or 0)
        except (ValueError, TypeError):
            amount_used = 0.0
            
        if not service_type:
            flash("Please select a service type.", "danger")
            return redirect(url_for("dashboard.requests_view"))
            
        try:
            success, message = submit_service_request(user_id, service_type, description, amount_used)
            flash(message, "success" if success else "danger")
        except Exception:
            flash("Failed to submit request.", "danger")
        return redirect(url_for("dashboard.requests_view"))
        
    reqs = get_service_requests(user_id)
    user = get_user_profile(user_id)
    return render_template("dashboard/requests.html", user=user, requests=reqs)

@dashboard_bp.route("/recharge", methods=["POST"])
@login_required
def recharge():
    user_id = session.get("user_id")
    try:
        amount = float(request.form.get("amount") or 0)
    except (ValueError, TypeError):
        flash("Invalid recharge amount.", "danger")
        return redirect(url_for("dashboard.home"))
        
    operator = request.form.get("operator", "Unknown").strip()
    if amount <= 0:
        flash("Amount must be greater than 0.", "danger")
        return redirect(url_for("dashboard.home"))
        
    try:
        saved = add_recharge(user_id, amount, operator)
        flash(f"Recharge successful! {saved:.2f} BDT saved.", "success")
    except Exception:
        flash("Recharge failed.", "danger")
    return redirect(url_for("dashboard.home"))

@dashboard_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session.get("user_id")
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        if not full_name or not phone:
            flash("Name and phone are required.", "danger")
            return redirect(url_for("dashboard.profile"))
            
        try:
            success, message = update_user_profile(user_id, full_name, phone)
            if success:
                session["full_name"] = full_name
                flash(message, "success")
            else:
                flash(message, "danger")
        except Exception:
            flash("Profile update failed.", "danger")
        return redirect(url_for("dashboard.profile"))
        
    user = get_user_profile(user_id)
    return render_template("dashboard/profile.html", user=user, summary=get_dashboard_summary(user_id), records=get_health_records(user_id, limit=5), recharge_history=get_recharge_history(user_id))
