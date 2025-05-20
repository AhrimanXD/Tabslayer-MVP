from flask import request, jsonify, Blueprint
from models import db, User
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity


login_bp = Blueprint("login_bp",__name__)
register_bp = Blueprint("register_bp", __name__)
user_bp = Blueprint("user_bp", __name__)


@register_bp.route('', methods = ["POST"])
def register():
  username = request.json.get('username')
  email = request.json.get('email')
  password = request.json.get('password')
  if User.query.filter_by(username = username).first() or User.query.filter_by(email = email).first():
    return jsonify(Message = "User Already Exists")
  new_user = User(username = username, email = email)
  new_user.set_password(password=password)
  db.session.add(new_user)
  db.session.commit()
  return jsonify(
    {"Message":"Successfully registered user","user":new_user.to_dict()}
  ),201

  
@login_bp.route('', methods = ["POST"])
def login():
  username = request.json.get('username')
  password = request.json.get('password')
  user = User.query.filter_by(username = username).first()
  if user and user.check_password(password):
    token = create_access_token(identity=username)
    return jsonify({"Message" : f"Welcome {user.username}","Access-Token":token})
  return jsonify(Error = "Incorrect Password Or User Not Found")
  
@user_bp.route('/me', methods = ['GET'])
@jwt_required()
def get_user():
  user = User.query.filter_by(username = get_jwt_identity()).first()
  return jsonify(message = user.to_dict()), 200