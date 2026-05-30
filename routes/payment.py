from flask import Blueprint, request, redirect, url_for, flash, session, current_app
from utils.db import get_db
from utils.security import login_required
import hashlib

payment_bp = Blueprint('payment', __name__)

def verify_sslcommerz(post_data):
    """SSLCommerz IPN verification."""
    store_passwd = current_app.config.get('SSLCOMMERZ_STORE_PASSWORD', 'testpass')
    received_hash = post_data.get('verify_hash', '')
    hash_string = store_passwd
    for key in sorted(post_data.keys()):
        if key != 'verify_hash':
            hash_string += post_data[key]
    generated_hash = hashlib.md5(hash_string.encode()).hexdigest()
    return generated_hash == received_hash

@payment_bp.route('/recharge', methods=['POST'])
@login_required
def initiate_payment():
    amount = request.form.get('amount', '').strip()
    if not amount or float(amount) <= 0:
        flash("Invalid recharge amount.", "danger")
        return redirect(url_for('dashboard.user_dashboard'))

    user_id = session.get('user_id')
    store_id = current_app.config.get('SSLCOMMERZ_STORE_ID', 'teststore')
    store_passwd = current_app.config.get('SSLCOMMERZ_STORE_PASSWORD', 'testpass')

    # SSLCommerz payment gateway URL
    gateway_url = (
        f"https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
        f"?store_id={store_id}"
        f"&store_passwd={store_passwd}"
        f"&total_amount={amount}"
        f"&currency=BDT"
        f"&tran_id=FH_{user_id}_{amount}"
        f"&success_url={url_for('payment.payment_success', _external=True)}"
        f"&fail_url={url_for('payment.payment_fail', _external=True)}"
        f"&cancel_url={url_for('payment.payment_cancel', _external=True)}"
        f"&cus_name={session.get('user_name', 'User')}"
        f"&cus_email=customer@flexihealth.com"
        f"&cus_phone=01700000000"
        f"&cus_add1=Bangladesh"
        f"&cus_city=Dhaka"
        f"&cus_country=Bangladesh"
        f"&shipping_method=NO"
        f"&product_name=Flexi+Health+Recharge"
        f"&product_category=Healthcare"
        f"&product_profile=general"
    )
    return redirect(gateway_url)

@payment_bp.route('/success', methods=['POST'])
def payment_success():
    try:
        amount = float(request.form.get('amount', 0))
        tran_id = request.form.get('tran_id', '')
        user_id = int(tran_id.split('_')[1])

        # 10% savings calculation
        savings = round(amount * 0.10, 2)

        db = get_db()
        db.execute(
            "UPDATE savings_accounts SET balance = balance + ? WHERE user_id = ?",
            (savings, user_id)
        )
        db.execute(
            "INSERT INTO transactions (user_id, amount, transaction_type) VALUES (?, ?, ?)",
            (user_id, amount, 'recharge')
        )
        db.commit()

        flash(f"Recharge successful! {savings} BDT saved to your Flexi Health account.", "success")
    except Exception as e:
        current_app.logger.error(f"Payment Success Processing Failure: {str(e)}")
        flash("Payment received but savings update failed.", "danger")

    return redirect(url_for('dashboard.user_dashboard'))

@payment_bp.route('/fail', methods=['POST'])
def payment_fail():
    flash("Payment failed. Please try again.", "danger")
    return redirect(url_for('dashboard.user_dashboard'))

@payment_bp.route('/cancel', methods=['POST'])
def payment_cancel():
    flash("Payment cancelled.", "warning")
    return redirect(url_for('dashboard.user_dashboard'))
