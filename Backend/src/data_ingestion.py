import json
import uuid
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError
import logging
from models import db, Product, Category  # Import 'db' object from models.py

logging.basicConfig(level=logging.DEBUG)

data_ingestion_bp = Blueprint('data_ingestion', __name__)
api = Api(data_ingestion_bp)  # Create an Api instance for the blueprint

class DataIngestion(Resource):
    
    REQUIRED_KEYS = {'productImage', 'catlevel1Name', 'price', 'name', 'productDescription', 'catlevel2Name', 'sku'}

    def post(self) :
        if 'file' not in request.files:
            return {'message': 'No file part in the request'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400

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
            return {'message': 'Invalid JSON format'}, 400

        except IntegrityError as e:
            logging.error(f"IntegrityError: {e}")
            db.session.rollback()
            return {'message': 'Integrity Error: Duplicate product_id or category_id'}, 400

        except Exception as e:
            logging.error(f"An unhandled exception occurred: {e}")
            db.session.rollback()
            return {'message': 'Internal Server Error'}, 500

        # Return a valid JSON response using the 'jsonify' function
        return {'message': 'Data ingestion successful'}, 201

# Register the DataIngestion resource with the data_ingestion_bp blueprint
api.add_resource(DataIngestion, '/data_ingestion')