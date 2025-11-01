from flask import jsonify, request
from config.database import get_db
from models.cart_model import Cart
from sqlalchemy.orm import Session
from datetime import datetime

def get_all_cart():
    db: Session = next(get_db())
    data = db.query(Cart).all()
    return jsonify([{
        "id_cart": k.id_cart,
        "id_menu": k.id_menu,
        "quantity": k.quantity,
        "added_at": k.added_at,
        "updated_at": k.updated_at
    } for k in data])

def add_cart():  
    db: Session = next(get_db())
    body = request.json

    new_data = Cart(
        id_menu=body["id_menu"],
        quantity=body["quantity"]
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "id_cart": new_data.id_cart,
        "id_menu": new_data.id_menu,
        "quantity": new_data.quantity,
        "added_at": new_data.added_at,
        "updated_at": new_data.updated_at
    })

def update_cart(id_cart):
    db: Session = next(get_db())
    body = request.json

    cart = db.query(Cart).filter(Cart.id_cart == id_cart).first()
    if not cart:
        return jsonify({"message": "Cart tidak ditemukan"}), 404

    # Update field sesuai data yang dikirim
    cart.id_menu = body.get("id_menu", cart.id_menu)
    cart.quantity = body.get("quantity", cart.quantity)

    db.commit()
    db.refresh(cart)

    return jsonify({
        "message": "Data berhasil diperbarui",
        "data": {
            "id_cart": cart.id_cart,
            "id_menu": cart.id_menu,
            "quantity": cart.quantity,
            "added_at": cart.added_at,
            "updated_at": cart.updated_at
        }
    }), 200

def delete_cart(id_cart):
    db: Session = next(get_db())
    cart = db.query(Cart).filter(Cart.id_cart == id_cart).first()
    if not cart:
        return jsonify({"message": "Cart tidak ditemukan"}), 404

    db.delete(cart)
    db.commit()

    return jsonify({"message": f"Data cart dengan id {id_cart} berhasil dihapus"}), 200