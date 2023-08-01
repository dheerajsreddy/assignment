from flask import Blueprint, jsonify
from models import db,Product
# Create a Blueprint for the product module
product_bp = Blueprint('product', __name__)

@product_bp.route('/product/<string:product_id>', methods=['GET'])
def get_product(product_id: str) -> jsonify:
    """
    Retrieve product details based on the provided product_id.

    Args:
        product_id (str): The product ID to retrieve details for.

    Returns:
        JSON response: JSON object containing product details.
    """
    try:
        # Retrieve the product based on product_id, or return 404 if not found
        product = Product.query.get_or_404(product_id)

        # Construct the product data to be returned
        product_data = {
            'product_id': product.product_id,
            'name': product.name,
            'price': float(product.price) if product.price is not None else 0.0,
            'description': product.description or '',
            'image_url': product.image_url or ''
        }

        return jsonify(product_data), 200

    except Exception as e:
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500
