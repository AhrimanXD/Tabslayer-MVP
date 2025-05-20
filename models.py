from flask_sqlalchemy import SQLAlchemy
from datetime import timezone, datetime
from werkzeug.security import check_password_hash, generate_password_hash
db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  username = db.Column(db.String(50), nullable = False, unique = True)
  email = db.Column(db.String(100), nullable = False, unique = True)
  password_hash = db.Column(db.String(128), nullable = False)
  categories = db.relationship("Category", backref = "user", lazy = True)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def to_dict(self):
    return {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "categories": [category.to_dict() for category in self.categories]
    }

class Category(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(128), nullable = False)
  description = db.Column(db.String(500), nullable = False)
  created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  resources = db.relationship("Resource", backref = "category")
  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "description": self.description,
      "created_at": self.created_at.isoformat() if self.created_at else None,
      "user_id": self.user_id,
      "resources": [resource.to_dict() for resource in self.resources]
    }
  
class Resource(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(128), nullable = False)
  link = db.Column(db.String(500), nullable = False, unique = True)
  description = db.Column(db.String(500), nullable = False)
  date_added = db.Column(db.DateTime, default = datetime.now(timezone.utc))
  cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))

  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "description": self.description,
      "created_at": self.date_added.isoformat() if self.date_added else None,
      "cat_id": self.cat_id,
    }
  
