from flask import (
    Blueprint, request, redirect,
    url_for, flash, session, current_app
)
from utils.db import get_db
from utils.security import login_required
import hashlib


payment_bp = Blueprint("payment", __name__)


# =========================
# SSL VERIFY
# =========================
def verify_sslcommerz(data):
    try:
        store_passwd = current_app.config.get(
            "SSLCOMMERZ_STORE_PASSWORD", ""
        )

        received_hash = data.get("verify_hash", "")

        hash_string = store_passwd

        for key in sorted(data.keys()):
            if key != "verify_hash":
                hash_string += str(data[key])

        generated_hash = hashlib.md5(
            hash_string.encode()
        ).hexdigest()

        return generated_hash == received_hash

    except Exception:
        return False


# =========================
# INITIATE PAYMENT
# =========================
@payment_bp.route("/recharge", methods=["POST"])
@login_required
def initiate_payment():

    try:
        amount = float(request.form.get("amount") or 0)

        if amount <= 0:
            flash("Invalid recharge amount.", "danger")
            return redirect(url_for("dashboard.home"))

    except (ValueError, TypeError):
        flash("Invalid amount format.", "danger")
        return redirect(url_for("dashboard.home"))

    user_id = session.get("user_id")

    store_id = current_app.config.get("SSLCOMMERZ_STORE_ID")

    # DO NOT expose store password in URL (SECURITY FIX)
    gateway_url = (
        "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
        f"?store_id={store_id}"
        f"&total_amount={amount}"
        f"&currency=BDT"
        f"&tran_id=FH_{user_id}_{amount}"
        f"&success_url={url_for('payment.payment_success', _external=True)}"
        f"&fail_url={url_for('payment.payment_fail', _external=True)}"
        f"&cancel_url={url_for('payment.payment_cancel', _external=True)}"
        f"&cus_name={session.get('full_name', 'User')}"
        f"&cus_email={session.get('email', 'test@flexihealth.com')}"
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


# =========================
# SUCCESS
# =========================
@payment_bp.route("/success", methods=["GET", "POST"])
def payment_success():

    try:
        amount = float(request.values.get("amount") or 0)
        tran_id = request.values.get("tran_id", "")

        if not tran_id or "_" not in tran_id:
            flash("Invalid transaction.", "danger")
            return redirect(url_for("dashboard.home"))

        user_id = int(tran_id.split("_")[1])

        savings = round(amount * 0.10, 2)

        db = get_db()

        # update wallet safely
        db.execute(
            """
            UPDATE savings_accounts
            SET balance = balance + ?
            WHERE user_id = ?
            """,
            (savings, user_id)
        )

        db.execute(
            """
            INSERT INTO transactions
            (user_id, amount, transaction_type)
            VALUES (?, ?, ?)
            """,
            (user_id, amount, "recharge")
        )

        db.commit()

        flash(
            f"Payment successful! {savings} BDT saved.",
            "success"
        )

    except Exception as e:
        current_app.logger.error(
            f"PAYMENT SUCCESS ERROR: {e}"
        )
        flash(
            "Payment received but processing failed.",
            "danger"
        )

    return redirect(url_for("dashboard.home"))


# =========================
# FAIL
# =========================
@payment_bp.route("/fail", methods=["GET", "POST"])
def payment_fail():
    flash("Payment failed. Try again.", "danger")
    return redirect(url_for("dashboard.home"))


# =========================
# CANCEL
# =========================
@payment_bp.route("/cancel", methods=["GET", "POST"])
def payment_cancel():
    flash("Payment cancelled.", "warning")
    return redirect(url_for("dashboard.home"))
