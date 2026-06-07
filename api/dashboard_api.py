from flask import Blueprint, request, jsonify, session
from utils.security import api_login_required, api_admin_required
from services.dashboard_service import (
    add_health_record, get_health_records, get_latest_health_record,
    submit_service_request, get_service_requests, get_dashboard_summary,
    get_all_service_requests, update_service_request_status
)

dashboard_api_bp = Blueprint('dashboard_api', __name__)

@dashboard_api_bp.route('/summary', methods=['GET'])
@api_login_required
def api_summary():
    summary = get_dashboard_summary(session['user_id'])
    return jsonify({'success': True, 'summary': summary}), 200

@dashboard_api_bp.route('/health', methods=['GET'])
@api_login_required
def api_get_health():
    limit = request.args.get('limit', 20, type=int)
    records = get_health_records(session['user_id'], limit)
    return jsonify({'success': True, 'records': records}), 200

@dashboard_api_bp.route('/health', methods=['POST'])
@api_login_required
def api_add_health():
    data = request.get_json(silent=True) or {}
    weight = data.get('weight')
    height = data.get('height')
    bp_sys = data.get('blood_pressure_systolic')
    bp_dia = data.get('blood_pressure_diastolic')
    blood_type = data.get('blood_type')
    notes = data.get('notes')
    add_health_record(session['user_id'], weight, height, bp_sys, bp_dia, blood_type, notes)
    return jsonify({'success': True, 'message': 'Health record saved.'}), 201

@dashboard_api_bp.route('/health/latest', methods=['GET'])
@api_login_required
def api_latest_health():
    record = get_latest_health_record(session['user_id'])
    return jsonify({'success': True, 'record': record}), 200

@dashboard_api_bp.route('/requests', methods=['GET'])
@api_login_required
def api_get_requests():
    reqs = get_service_requests(session['user_id'])
    return jsonify({'success': True, 'requests': reqs}), 200

@dashboard_api_bp.route('/requests', methods=['POST'])
@api_login_required
def api_submit_request():
    data = request.get_json(silent=True) or {}
    service_type = data.get('service_type', '')
    description = data.get('description', '')
    try:
        amount_used = float(data.get('amount_used', 0))
    except (ValueError, TypeError):
        amount_used = 0.0
    if not service_type:
        return jsonify({'success': False, 'message': 'Service type required.'}), 400
    success, message = submit_service_request(session['user_id'], service_type, description, amount_used)
    if success:
        return jsonify({'success': True, 'message': message}), 201
    return jsonify({'success': False, 'message': message}), 400

@dashboard_api_bp.route('/requests/all', methods=['GET'])
@api_admin_required
def api_all_requests():
    reqs = get_all_service_requests()
    return jsonify({'success': True, 'requests': reqs}), 200

@dashboard_api_bp.route('/requests/<int:req_id>/status', methods=['PUT'])
@api_admin_required
def api_update_request_status(req_id):
    data = request.get_json(silent=True) or {}
    status = data.get('status', '')
    if status not in ('pending', 'in_progress', 'completed', 'rejected'):
        return jsonify({'success': False, 'message': 'Invalid status.'}), 400
    update_service_request_status(req_id, status)
    return jsonify({'success': True, 'message': 'Status updated.'}), 200
