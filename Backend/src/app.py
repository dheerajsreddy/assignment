import os
import logging
from flask import Flask
from models import db
import redis
    
def create_app():
    app = Flask(__name__)
    
    # Set the logging level to INFO
    app.logger.setLevel(logging.INFO)
    
    # Modify the database URI to use the service name as the host in the connection URL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://unbxd:unbxd@postgres-service:5432/unbxddatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the SQLAlchemy db object with the app
    db.init_app(app)

    # Modify the Redis URL to use the service name as the host in the connection URL
    redis_url = os.environ.get('REDIS_URL', 'redis://redis-service:6379')
    app.redis_client = redis.StrictRedis.from_url(redis_url)

    # Import blueprints here to avoid circular imports
    from data_ingestion import data_ingestion_bp
    from product import product_bp
    from category import category_bp
    from search import search_bp
    from monitor import monitor_bp

    # Register blueprints with the app
    app.register_blueprint(monitor_bp)
    app.register_blueprint(data_ingestion_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(search_bp)

    @app.before_request
    def create_tables():
        db.create_all()

    return app

# If this file is being executed as the main module, run the app
if __name__ == '__main__':
    app = create_app()

    # Run the app in debug mode
    app.run(debug=True, host="0.0.0.0", port=5000)