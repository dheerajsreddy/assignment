import os
import json
import uuid
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'postgresql://dheeraj:123@localhost/apparel')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)
logging.basicConfig(level=logging.DEBUG)

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.String, primary_key=True)
    category_name = db.Column(db.String)
    parent_name = db.Column(db.String)

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    image_url = db.Column(db.String)
    category_id = db.Column(db.String, db.ForeignKey('category.category_id'), nullable=False)
    category = db.relationship('Category')

class DataIngestion(Resource):
    REQUIRED_KEYS = {'productImage', 'catlevel1Name', 'price', 'name', 'productDescription', 'catlevel2Name', 'sku'}

    def post(self):
        if 'file' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        try:
            json_data = json.load(file)  # Load the entire JSON data into memory

            # Prepare the data for bulk insertion
            bulk_data = []
            for item in json_data:
                if self.REQUIRED_KEYS.issubset(item.keys()):
                    category_name = item['catlevel2Name']
                    parent_name = item['catlevel1Name']

                    category = Category.query.filter_by(category_name=category_name, parent_name=parent_name).first()

                    if not category:
                        category_id = str(uuid.uuid4())
                        category = Category(
                            category_id=category_id,
                            category_name=category_name,
                            parent_name=parent_name
                        )
                        db.session.add(category)
                        db.session.flush()  # Flush to get the primary key before bulk insertion

                    product_id = item['sku']
                    name = item['name']
                    price = item['price']
                    description = item.get('productDescription', '')
                    image_url = item.get('productImage', '')

                    product = Product(
                        product_id=product_id,
                        name=name,
                        price=price,
                        description=description,
                        image_url=image_url,
                        category_id=category.category_id
                    )
                    bulk_data.append(product)

            # Perform batch insertion
            db.session.bulk_save_objects(bulk_data)
            db.session.commit()

        except json.JSONDecodeError as e:
            logging.error(f"JSONDecodeError: {e}")
            return jsonify({'message': 'Invalid JSON format'}), 400

        except IntegrityError as e:
            logging.error(f"IntegrityError: {e}")
            db.session.rollback()
            return jsonify({'message': 'Integrity Error: Duplicate product_id or category_id'}), 400

        except Exception as e:
            logging.error(f"An unhandled exception occurred: {e}")
            db.session.rollback()
            return jsonify({'message': 'Internal Server Error'}), 500

        return {'message': 'Data ingestion successful'}, 201

# Create the database tables after setting up the application context
with app.app_context():
    db.create_all()

# Register the DataIngestion resource with the API
api.add_resource(DataIngestion, '/data_ingestion')

if __name__ == '__main__':
    app.run()
