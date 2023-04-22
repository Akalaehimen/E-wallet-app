from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from Blocklist import BLOCKLIST
from utils import db
from flask import request, jsonify
from datetime import timedelta
import random
from api.models.user import UserModel
from schema import UserSchema
from schema import UsersSchema



blp = Blueprint("Users", "users", description="Operations on Users")

# Register a user


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter_by(email=user_data["email"]).first():
            abort(409, message="This Email already exists")

        user = UserModel(
            surname=user_data["surname"],
            firstname=user_data["firstname"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        # generate a random user ID with digits only
        user_id = ''.join(str(random.randint(0, 9)) for _ in range(4))

        user.user_id = user_id  # store the generated user ID in the database

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully",
                "Your User_id is": user_id}, 201


# Login a user
@blp.route("/login", methods=['POST'])
class Login(MethodView):
    @blp.arguments(UsersSchema)
    def post(self, user_data):
        user_data = request.get_json()
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return jsonify({"message": "User successfully logged in",
                            "access_token": access_token,
                            "refresh_token": refresh_token})

        return jsonify({"message": "Invalid credentials"}), 401


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user, fresh=False, expires_delta=timedelta(days=5)
        )

        return {"access_token": new_token}

# Logout a user


@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        try:
            BLOCKLIST.add(jti)

        except IntegrityError:
            abort(400, message="you need to be logged in to have access")

        return ({"message": "Successfully logged out"})


# Delete a user by is user id
@blp.route('/users/<string:user_id>')
class UserDeleteById(MethodView):
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"message": "User not founds"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200
