from functools import wraps
from datetime import datetime, timedelta
import jwt

from flask import g, request, jsonify
from flask import current_app as app
from flask import jsonify

from app.config import Config
from app.models import Admin


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if " " in auth_header else None
        
        print("token", token)
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({"message": "Invalid or expired token!"}), 401

        decoded_data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data["sub"]

        g.user = Admin.query.get(user_id)
        return f(*args, **kwargs)

    return decorated_function


def generate_jwt_token(user_id):
    """
    Generate a JWT token with user_id payload.
    """
    print("generate_jwt_token Config.SECRET_KEY", Config.SECRET_KEY)

    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=10),  # Token expires in 1 hour
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


def verify_jwt_token(token):
    """
    Verify JWT token and return the payload if valid.
    """
    try:
        print("verify Config.SECRET_KEY", Config.SECRET_KEY)
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
