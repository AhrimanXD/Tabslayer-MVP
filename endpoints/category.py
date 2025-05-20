from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Category, User
category_bp = Blueprint('category_bp', __name__)

@category_bp.route('', methods=["POST"])
@jwt_required()
def create_category():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first_or_404()
    
    data = request.get_json()  # Use get_json() instead of .json
    title = data.get("title")
    desc = data.get("description")
    
    # Safer empty check
    if not title or not isinstance(title, str) or not title.strip():
        return jsonify(error="Title is required and must be a non-empty string"), 400
    if not desc or not isinstance(desc, str):
        desc = ""  # Make description optional

    # Check for duplicate titles (per user)
    if Category.query.filter_by(title=title, user_id=user.id).first():
        return jsonify(error=f"Category '{title}' already exists"), 409

    new_category = Category(title=title, description=desc, user_id=user.id)
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify(
        message=f"Category '{title}' created",
        data=new_category.to_dict()
    ), 201

@category_bp.route('', methods=["GET"])
@jwt_required()
def fetch_all_categories():
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    return jsonify([cat.to_dict() for cat in user.categories])

@category_bp.route('/<int:cat_id>', methods=['GET'])
@jwt_required()
def fetch_category(cat_id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    
    # PROPER DATABASE QUERY WITH OWNERSHIP CHECK
    category = Category.query.filter_by(id=cat_id, user_id=user.id).first()
    
    if not category:
        return jsonify(error="Category not found"), 404
    return jsonify(data=category.to_dict())

@category_bp.route('/<int:cat_id>', methods=['PUT'])
@jwt_required()
def update_category(cat_id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    data = request.get_json()
    
    # PROPER OWNERSHIP CHECK
    category = Category.query.filter_by(id=cat_id, user_id=user.id).first()
    if not category:
        return jsonify(error="Category not found"), 404

    # Validate input
    title = data.get("title")
    desc = data.get("description")
    
    if title:
        if not isinstance(title, str) or not title.strip():
            return jsonify(error="Title must be a non-empty string"), 400
        category.title = title
    
    if desc:
        category.description = desc if isinstance(desc, str) else str(desc)
    
    db.session.commit()
    return jsonify(
        message="Category updated",
        data=category.to_dict()
    )

@category_bp.route('/<int:cat_id>', methods=['DELETE'])
@jwt_required()
def delete_category(cat_id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    
    # PROPER OWNERSHIP CHECK
    category = Category.query.filter_by(id=cat_id, user_id=user.id).first()
    if not category:
        return jsonify(error="Category not found"), 404
    for resource in category.resources:
        db.session.delete(resource)
    db.session.delete(category)
    
    db.session.commit()
    return jsonify(
        message="Category updated",
        data=category.to_dict()
    )
