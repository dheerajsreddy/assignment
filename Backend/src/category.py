import redis
from flask import Blueprint, jsonify,current_app
from flask_restful import Resource, Api
from models import db, Product, Category
import json
category_bp = Blueprint('category', __name__)
api = Api(category_bp)  # Create an Api instance for the blueprint


class CategoryAPI(Resource):
    def get(self):
        # Check if the categories are already in the Redis cache
        cached_result = current_app.redis_client.get('categories')
        if cached_result:
            # If found in cache, return the cached result
            categories_data = json.loads(cached_result)
            print("Cache Hit")
            return categories_data, 200

        categories = Category.query.all()
        categories_data = [{'category_name': category.category_name, 'parent_name': category.parent_name} for category in categories]

        # Update Redis cache with the new categories
        current_app.redis_client.set('categories', json.dumps(categories_data))
        print("Cache Miss")

        return categories_data, 200

class ProductByCategoryAPI(Resource):
    def get(self, parent_name):
        # Check if the products by category are already in the Redis cache
        cached_result = current_app.redis_client.get(f'products_by_category:{parent_name}')
        if cached_result:
            # If found in cache, return the cached result
            products_data = json.loads(cached_result)
            print("Cache Hit")
            return products_data, 200

        # Category exists, fetch the products
        products = Product.query.join(Category, Product.category_id == Category.category_id) \
                               .filter(Category.parent_name == parent_name) \
                               .all()
        products_data = [{
            'name': product.name,
            'price': float(product.price) if product.price is not None else 0.0,
            'image_url': product.image_url or ''
        } for product in products]

        # Update Redis cache with the new products by category
        current_app.redis_client.set(f'products_by_category:{parent_name}', json.dumps(products_data))
        print("Cache Miss")
        return products_data, 200

class ProductBySubcategoryAPI(Resource):
    def get(self, parent_name, category_name):
        # Check if the products by subcategory are already in the Redis cache
        cached_result = current_app.redis_client.get(f'products_by_subcategory:{parent_name}:{category_name}')
        if cached_result:
            # If found in cache, return the cached result
            products_data = json.loads(cached_result)
            print("Cache Hit")
            return products_data, 200

        products = Product.query.join(Category, Product.category_id == Category.category_id) \
                               .filter(Category.parent_name == parent_name, Category.category_name == category_name) \
                               .all()
        products_data = [{
            'name': product.name,
            'price': float(product.price) if product.price is not None else 0.0,
            'image_url': product.image_url or ''
        } for product in products]

        # Update Redis cache with the new products by subcategory
        current_app.redis_client.set(f'products_by_subcategory:{parent_name}:{category_name}', json.dumps(products_data))
        print("Cache Miss")
        return products_data, 200

# Add the resources to the Api instance
api.add_resource(CategoryAPI, '/category')
api.add_resource(ProductByCategoryAPI, '/category/<string:parent_name>')
api.add_resource(ProductBySubcategoryAPI, '/category/<string:parent_name>/<string:category_name>')
