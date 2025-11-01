from flask import jsonify, request
from config.database import get_db
from models.user_model import User
from sqlalchemy.orm import Session
from datetime import datetime
from werkzeug.security import generate_password_hash


def get_all_users():
    db: Session = next(get_db())
    data = db.query(User).all()
    return jsonify([{
        "id_user": u.id_user,
        "name": u.name,
        "email": u.email,
        "role": u.role,
        "created_at": u.created_at
    } for u in data])


def add_user():
    db: Session = next(get_db())
    body = request.json

    name = body.get("name")
    email = body.get("email")
    password = body.get("password")
    role = body.get("role", "customer")

    if not name or not email or not password:
        return jsonify({"message": "`name`, `email`, dan `password` wajib diisi"}), 400

    # check email uniqueness
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return jsonify({"message": "Email sudah terdaftar"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name,
        email=email,
        password=hashed_password,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "id_user": new_user.id_user,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
        "created_at": new_user.created_at
    })


def update_user(id_user):
    db: Session = next(get_db())
    body = request.json

    user = db.query(User).filter(User.id_user == id_user).first()
    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 404

    # update fields
    if "name" in body:
        user.name = body["name"]

    if "email" in body and body["email"] != user.email:
        # check uniqueness
        if db.query(User).filter(User.email == body["email"]).first():
            return jsonify({"message": "Email sudah terdaftar"}), 400
        user.email = body["email"]

    if "password" in body and body["password"]:
        user.password = generate_password_hash(body["password"])

    if "role" in body:
        user.role = body["role"]

    db.commit()
    db.refresh(user)

    return jsonify({
        "message": "Data berhasil diperbarui",
        "data": {
            "id_user": user.id_user,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }
    }), 200


def delete_user(id_user):
    db: Session = next(get_db())
    user = db.query(User).filter(User.id_user == id_user).first()
    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 404

    db.delete(user)
    db.commit()

    return jsonify({"message": f"Data user dengan id {id_user} berhasil dihapus"}), 200
