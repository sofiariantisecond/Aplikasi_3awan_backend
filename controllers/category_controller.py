from flask import jsonify, request
from config.database import get_db
from models.category_model import MenuCategory
from sqlalchemy.orm import Session
from datetime import datetime

def get_all_category():
    db: Session = next(get_db())
    data = db.query(MenuCategory).all()
    return jsonify([{
        "id_category": k.id_category,
        "category_name": k.category_name,
        "description": k.description
    } for k in data])

def add_category():  
    db: Session = next(get_db())
    body = request.json

    new_data = MenuCategory(
        category_name=body["category_name"],
        description=body.get("description")
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "id_category": new_data.id_category,
        "category_name": new_data.category_name,
        "description": new_data.description
    })

def update_category(id_category):
    db: Session = next(get_db())
    body = request.json

    category = db.query(MenuCategory).filter(MenuCategory.id_category == id_category).first()
    if not category:
        return jsonify({"message": "Category tidak ditemukan"}), 404

    # Update field sesuai data yang dikirim
    category.category_name = body.get("category_name", category.category_name)
    category.description = body.get("description", category.description)

    db.commit()
    db.refresh(category)

    return jsonify({
        "message": "Data berhasil diperbarui",
        "data": {
            "id_category": category.id_category,
            "category_name": category.category_name,
            "description": category.description
        }
    }), 200

def delete_category(id_category):
    db: Session = next(get_db())
    category = db.query(MenuCategory).filter(MenuCategory.id_category == id_category).first()
    if not category:
        return jsonify({"message": "Category tidak ditemukan"}), 404

    db.delete(category)
    db.commit()

    return jsonify({"message": f"Data category dengan id {id_category} berhasil dihapus"}), 200