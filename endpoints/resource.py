from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Resource, Category, User

resource_bp = Blueprint('resource_bp', __name__)

# Create a Resource
@resource_bp.route('', methods=["POST"])
@jwt_required()
def create_resource():
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ['title', 'link', 'category_id']):
        return jsonify({"error": "Title, link, and category_id are required"}), 400
    
    # Verify category ownership
    category = Category.query.filter_by(
        id=data['category_id'],
        user_id=user.id
    ).first_or_404(description="Category not found or access denied")
    
    # Create resource
    new_resource = Resource(
        title=data['title'],
        link=data['link'],
        description=data.get('description', ''),
        cat_id=category.id
    )
    
    db.session.add(new_resource)
    db.session.commit()
    
    return jsonify({
        "message": "Resource created successfully",
        "data": new_resource.to_dict()
    }), 201
"""
# Get All Resources in a Category
@resource_bp.route('/category/<int:category_id>', methods=["GET"])
@jwt_required()
def get_resources_by_category(category_id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    
    # Verify category ownership
    category = Category.query.filter_by(
        id=category_id,
        user_id=user.id
    ).first_or_404(description="Category not found or access denied")
    
    resources = Resource.query.filter_by(category_id=category.id).all()
    return jsonify([resource.to_dict() for resource in resources])"""

# Get a Specific Resource
@resource_bp.route('/<int:resource_id>', methods=["GET"])
@jwt_required()
def get_resource(resource_id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    
    resource = Resource.query.filter_by(id=resource_id).first_or_404()
    
    # Verify indirect ownership through category
    if resource.category.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403
    
    return jsonify(resource.to_dict())

# Update a Resource
@resource_bp.route('/<int:resource_id>', methods=["PUT"])
@jwt_required()
def update_resource(resource_id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    data = request.get_json()
    
    resource = Resource.query.filter_by(id=resource_id).first_or_404()
    
    # Verify ownership
    if resource.category.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403
    
    # Update fields if provided
    if 'title' in data:
        if not data['title'] or not isinstance(data['title'], str):
            return jsonify({"error": "Title must be a non-empty string"}), 400
        resource.title = data['title']
    
    if 'link' in data:
        resource.link = data['link']
    
    if 'description' in data:
        resource.description = data.get('description', '')
    
    if 'category_id' in data:
        new_category = Category.query.filter_by(
            id=data['category_id'],
            user_id=user.id
        ).first_or_404(description="New category not found or access denied")
        resource.cat_id = new_category.id
    
    db.session.commit()
    
    return jsonify({
        "message": "Resource updated successfully",
        "data": resource.to_dict()
    })

# Delete a Resource
@resource_bp.route('/<int:resource_id>', methods=["DELETE"])
@jwt_required()
def delete_resource(resource_id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    
    resource = Resource.query.filter_by(id=resource_id).first_or_404()
    
    # Verify ownership
    if resource.category.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403
    
    db.session.delete(resource)
    db.session.commit()
    
    return jsonify({
        "message": "Resource deleted successfully",
        "deleted_data": resource.to_dict()
    }), 200