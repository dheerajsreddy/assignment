from flask import Blueprint, jsonify
from flask_restful import Resource, Api
from models import db, Product, Category

category_bp = Blueprint('category', __name__)
api = Api(category_bp)  # Create an Api instance for the blueprint

class CategoryAPI(Resource):
    def get(self):
        categories = Category.query.all()
        categories_data = [{'category_name': category.category_name, 'parent_name': category.parent_name} for category in categories]
        return categories_data, 200

class ProductByCategoryAPI(Resource):
    def get(self, parent_name):
        products = Product.query.join(Category, Product.category_id == Category.category_id) \
                               .filter(Category.parent_name == parent_name) \
                               .all()
        products_data = [{
            'name': product.name,
            'price': float(product.price) if product.price is not None else 0.0,
            'image_url': product.image_url or ''
        } for product in products]

        return products_data, 200

class ProductBySubcategoryAPI(Resource):
    def get(self, parent_name, category_name):
        products = Product.query.join(Category, Product.category_id == Category.category_id) \
                               .filter(Category.parent_name == parent_name, Category.category_name == category_name) \
                               .all()
        products_data = [{
            'name': product.name,
            'price': float(product.price) if product.price is not None else 0.0,
            'image_url': product.image_url or ''
        } for product in products]

        return products_data, 200

# Add the resources to the Api instance
api.add_resource(CategoryAPI, '/category')
api.add_resource(ProductByCategoryAPI, '/category/<string:parent_name>')
api.add_resource(ProductBySubcategoryAPI, '/category/<string:parent_name>/<string:category_name>')
