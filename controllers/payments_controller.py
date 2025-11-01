from flask import jsonify, request
from config.database import get_db
from models.payments_model import Payment
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal
import uuid


def get_all_payments():
    db: Session = next(get_db())
    data = db.query(Payment).all()
    return jsonify([{
        "id_payment": k.id_payment,
        "id_order": k.id_order,
        "payment_method": k.payment_method,
        "payment_status": k.payment_status,
        "payment_date": k.payment_date,
    } for k in data])


def add_payment():
    db: Session = next(get_db())
    body = request.json

    # Required
    id_order = body.get("id_order")
    amount_paid = body.get("amount_paid")
    if id_order is None or amount_paid is None:
        return jsonify({"message": "`id_order` dan `amount_paid` wajib diisi"}), 400

    payment_method = body.get("payment_method", "cash")
    payment_status = body.get("payment_status", "unpaid")

    # If marked as paid on creation, set payment_date to now
    payment_date = None
    if payment_status == "paid":
        payment_date = datetime.utcnow()
    else:
        # allow client to provide payment_date if present
        if body.get("payment_date"):
            try:
                # assume ISO format
                payment_date = datetime.fromisoformat(body.get("payment_date"))
            except Exception:
                payment_date = None


    new_data = Payment(
        id_order=id_order,
        payment_method=payment_method,
        payment_status=payment_status,
        payment_date=payment_date,
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "id_payment": new_data.id_payment,
        "id_order": new_data.id_order,
        "payment_method": new_data.payment_method,
        "payment_status": new_data.payment_status,
        "payment_date": new_data.payment_date,
    })


def update_payment(id_payment):
    db: Session = next(get_db())
    body = request.json

    payment = db.query(Payment).filter(Payment.id_payment == id_payment).first()
    if not payment:
        return jsonify({"message": "Payment tidak ditemukan"}), 404

    # Update allowed fields
    if "payment_method" in body:
        payment.payment_method = body["payment_method"]
    if "payment_status" in body:
        previous_status = payment.payment_status
        payment.payment_status = body["payment_status"]
        # if status changed to paid and no payment_date set, set it now
        if payment.payment_status == "paid" and not payment.payment_date:
            payment.payment_date = datetime.utcnow()
        # optionally if status changed from paid to unpaid, clear payment_date? keep as is
    if "payment_date" in body:
        try:
            payment.payment_date = datetime.fromisoformat(body["payment_date"]) if body["payment_date"] else None
        except Exception:
            pass

    db.commit()
    db.refresh(payment)

    return jsonify({
        "message": "Data berhasil diperbarui",
        "data": {
            "id_payment": payment.id_payment,
            "id_order": payment.id_order,
            "payment_method": payment.payment_method,
            "payment_status": payment.payment_status,
            "payment_date": payment.payment_date,
        }
    }), 200


def delete_payment(id_payment):
    db: Session = next(get_db())
    payment = db.query(Payment).filter(Payment.id_payment == id_payment).first()
    if not payment:
        return jsonify({"message": "Payment tidak ditemukan"}), 404

    db.delete(payment)
    db.commit()

    return jsonify({"message": f"Data payment dengan id {id_payment} berhasil dihapus"}), 200
