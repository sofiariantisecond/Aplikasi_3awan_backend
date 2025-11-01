from flask import jsonify, request
from config.database import get_db
from models.order_detail_model import OrderDetail
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

def get_all_order_detail():
    db: Session = next(get_db())
    data = db.query(OrderDetail).all()
    return jsonify([{
        "id_detail": k.id_detail,
        "id_order": k.id_order,
        "id_menu": k.id_menu,
        "quantity": k.quantity,
        "price": k.price,
        "subtotal": k.subtotal
    } for k in data])

def add_order_detail():  
    db: Session = next(get_db())
    body = request.json

    # Calculate subtotal and use Decimal for price/subtotal
    quantity = int(body["quantity"])
    price = Decimal(str(body["price"]))
    subtotal = price * Decimal(quantity)

    new_data = OrderDetail(
        id_order=body["id_order"],
        id_menu=body["id_menu"],
        quantity=quantity,
        price=price,
        subtotal=subtotal
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "id_detail": new_data.id_detail,
        "id_order": new_data.id_order,
        "id_menu": new_data.id_menu,
        "quantity": new_data.quantity,
        "price": new_data.price,
        "subtotal": new_data.subtotal
    })

def update_order_detail(id_detail):
    db: Session = next(get_db())
    body = request.json

    order_detail = db.query(OrderDetail).filter(OrderDetail.id_detail == id_detail).first()
    if not order_detail:
        return jsonify({"message": "Order detail tidak ditemukan"}), 404

    # Update field sesuai data yang dikirim
    if "quantity" in body:
        order_detail.quantity = int(body["quantity"])
    if "price" in body:
        order_detail.price = Decimal(str(body["price"]))
    if "id_menu" in body:
        order_detail.id_menu = body["id_menu"]
    
    # Recalculate subtotal if quantity or price changed
    if "quantity" in body or "price" in body:
        # use Decimal conversions to avoid float precision issues
        order_detail.subtotal = Decimal(order_detail.quantity) * Decimal(str(order_detail.price))

    db.commit()
    db.refresh(order_detail)

    return jsonify({
        "message": "Data berhasil diperbarui",
        "data": {
            "id_detail": order_detail.id_detail,
            "id_order": order_detail.id_order,
            "id_menu": order_detail.id_menu,
            "quantity": order_detail.quantity,
            "price": order_detail.price,
            "subtotal": order_detail.subtotal
        }
    }), 200

def delete_order_detail(id_detail):
    db: Session = next(get_db())
    order_detail = db.query(OrderDetail).filter(OrderDetail.id_detail == id_detail).first()
    if not order_detail:
        return jsonify({"message": "Order detail tidak ditemukan"}), 404

    db.delete(order_detail)
    db.commit()

    return jsonify({"message": f"Data order detail dengan id {id_detail} berhasil dihapus"}), 200
