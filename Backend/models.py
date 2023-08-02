from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.String, primary_key=True)
    category_name = db.Column(db.String, nullable=False)
    parent_name = db.Column(db.String)

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    image_url = db.Column(db.String)
    category_id = db.Column(db.String, db.ForeignKey('category.category_id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
