from flask import jsonify, request
from config.database import get_db
from models.order_model import Order
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

def get_all_orders():
    db: Session = next(get_db())
    data = db.query(Order).all()
    return jsonify([{
        "id_order": k.id_order,
        "id_user": k.id_user,
        "order_code": k.order_code,
        "total_price": k.total_price,
        "status": k.status,
        "created_at": k.created_at,
        "expired_at": k.expired_at,
        "qr_code": k.qr_code
    } for k in data])

def add_order():  
    db: Session = next(get_db())
    body = request.json

    # Generate unique order code
    order_code = str(uuid.uuid4())[:8].upper()
    
    # Set expiry time (e.g., 24 hours from creation)
    expired_at = datetime.utcnow() + timedelta(hours=24)

    total_price = Decimal(str(body["total_price"]))

    new_data = Order(
        id_user=body["id_user"],
        order_code=order_code,
        total_price=total_price,
        expired_at=expired_at,
        qr_code=body.get("qr_code")  # Optional
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "id_order": new_data.id_order,
        "id_user": new_data.id_user,
        "order_code": new_data.order_code,
        "total_price": new_data.total_price,
        "status": new_data.status,
        "created_at": new_data.created_at,
        "expired_at": new_data.expired_at,
        "qr_code": new_data.qr_code
    })

def update_order(id_order):
    db: Session = next(get_db())
    body = request.json

    order = db.query(Order).filter(Order.id_order == id_order).first()
    if not order:
        return jsonify({"message": "Order tidak ditemukan"}), 404

    # Update field sesuai data yang dikirim
    if "status" in body:
        order.status = body["status"]
    if "total_price" in body:
        order.total_price = body["total_price"]
    if "expired_at" in body:
        order.expired_at = body["expired_at"]
    if "qr_code" in body:
        order.qr_code = body["qr_code"]

    db.commit()
    db.refresh(order)

    return jsonify({
        "message": "Data berhasil diperbarui",
        "data": {
            "id_order": order.id_order,
            "id_user": order.id_user,
            "order_code": order.order_code,
            "total_price": order.total_price,
            "status": order.status,
            "created_at": order.created_at,
            "expired_at": order.expired_at,
            "qr_code": order.qr_code
        }
    }), 200

def delete_order(id_order):
    db: Session = next(get_db())
    order = db.query(Order).filter(Order.id_order == id_order).first()
    if not order:
        return jsonify({"message": "Order tidak ditemukan"}), 404

    db.delete(order)
    db.commit()

    return jsonify({"message": f"Data order dengan id {id_order} berhasil dihapus"}), 200
