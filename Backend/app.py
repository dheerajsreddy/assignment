import os
from flask import Flask
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'postgresql://dheeraj:123@localhost/apparel')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the SQLAlchemy db object with the app
    db.init_app(app)

    # Import blueprints here to avoid circular imports
    from data_ingestion import data_ingestion_bp
    from product import product_bp
    from category import category_bp
    from search import create_search_bp

    # Register blueprints with the app
    app.register_blueprint(data_ingestion_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(create_search_bp())

    # Function to create tables before each request
    @app.before_request
    def create_tables():
        db.create_all()

    return app

# If this file is being executed as the main module, run the app
if __name__ == '__main__':
    app = create_app()
    app.run()
