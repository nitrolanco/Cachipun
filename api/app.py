from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
import hashlib
import random
from db.database import db
from db import models
from db.database import app


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


if __name__ == "__main__":
    app.run(debug=True)
