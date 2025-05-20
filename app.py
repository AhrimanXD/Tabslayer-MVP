from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from endpoints.auth import register_bp,login_bp,user_bp
from endpoints.category import category_bp
from endpoints.resource import resource_bp
from models import db

app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)
db.init_app(app)
app.register_blueprint(register_bp, url_prefix = "/register")
app.register_blueprint(login_bp, url_prefix = "/login")
app.register_blueprint(user_bp, url_prefix = "/users")
app.register_blueprint(category_bp, url_prefix = "/categories")
app.register_blueprint(resource_bp, url_prefix = "/resources")
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    