from flask import jsonify, request
from config.database import get_db
from models.menu_model import Menu
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

def get_all_menu():
    db: Session = next(get_db())
    data = db.query(Menu).all()
    return jsonify([{
        "id_menu": k.id_menu,
        "name": k.name,
        "description": k.description,
        "price": k.price,
        "image": k.image,
        "id_category": k.id_category,
        "status": k.status,
        "created_at": k.created_at
    } for k in data])

def add_menu():  
    db: Session = next(get_db())
    body = request.json

    # convert price to Decimal to match DECIMAL column
    price = Decimal(str(body["price"]))

    new_data = Menu(
        name=body["name"],
        description=body.get("description"),
        price=price,
        image=body.get("image"),
        id_category=body["id_category"],
        status=body.get("status", "available")
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "id_menu": new_data.id_menu,
        "name": new_data.name,
        "description": new_data.description,
        "price": new_data.price,
        "image": new_data.image,
        "id_category": new_data.id_category,
        "status": new_data.status,
        "created_at": new_data.created_at
    })

def update_menu(id_menu):
    db: Session = next(get_db())
    body = request.json

    menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
    if not menu:
        return jsonify({"message": "Menu tidak ditemukan"}), 404

    # Update field sesuai data yang dikirim
    menu.name = body.get("name", menu.name)
    menu.description = body.get("description", menu.description)
    menu.price = body.get("price", menu.price)
    menu.image = body.get("image", menu.image)
    menu.id_category = body.get("id_category", menu.id_category)
    menu.status = body.get("status", menu.status)

    db.commit()
    db.refresh(menu)

    return jsonify({
        "message": "Data berhasil diperbarui",
        "data": {
            "id_menu": menu.id_menu,
            "name": menu.name,
            "description": menu.description,
            "price": menu.price,
            "image": menu.image,
            "id_category": menu.id_category,
            "status": menu.status,
            "created_at": menu.created_at
        }
    }), 200

def delete_menu(id_menu):
    db: Session = next(get_db())
    menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
    if not menu:
        return jsonify({"message": "Menu tidak ditemukan"}), 404

    db.delete(menu)
    db.commit()

    return jsonify({"message": f"Data menu dengan id {id_menu} berhasil dihapus"}), 200