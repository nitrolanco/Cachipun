from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
import hashlib
import random
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from db.database import db
from db import models
from db.database import app
import datetime
import os

jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)


@app.route("/api/v1/game/get_next_move", methods=["GET"])
def get_next_move():
    choice = random.randint(1, 3)
    return jsonify({"choice": choice})


@app.route("/api/v1/auth/register", methods=["POST"])
def create_user():
    new_user_data = request.get_json()
    print(new_user_data)
    new_user_data["password"] = hashlib.sha256(
        new_user_data["password"].encode("utf-8")
    ).hexdigest()
    try:
        user_to_add = models.User(
            username=new_user_data["username"],
            password=new_user_data["password"],
            kind=new_user_data["kind"],
            highscore=new_user_data["highscore"],
        )
        db.session.add(user_to_add)
        db.session.commit()
        print("user added")
        return (
            jsonify(
                {"message": "User created successfully", "user_id": user_to_add.id},
            ),
            200,
        )
    except Exception as e:
        # Rollback the transaction in case of any errors
        db.session.rollback()
        # Return an error message
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    login_data = request.get_json()
    if login_data["username"] and login_data["password"]:
        user = (
            db.session.query(models.User)
            .filter_by(username=login_data["username"])
            .first()
        )
        if (
            user.username == login_data["username"]
            and user.password
            == hashlib.sha256(login_data["password"].encode("utf-8")).hexdigest()
        ):
            access_token = create_access_token(identity=user.username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Credenciales incorrectas"}), 401

    return jsonify({"msg": "Ingrese credenciales"}), 401


@app.route("/api/v1/users", methods=["GET"])
def get_users():
    users = db.session.query(models.User).all()
    users_dict = [user.to_dict() for user in users]
    return jsonify(users_dict), 200


if __name__ == "__main__":
    app.run(debug=True)
