from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dheeraj:123@localhost/apparel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

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

api.add_resource(CategoryAPI, '/category')
api.add_resource(ProductByCategoryAPI, '/category/<string:parent_name>')
api.add_resource(ProductBySubcategoryAPI, '/category/<string:parent_name>/<string:category_name>')

if __name__ == '__main__':
    app.run()
