from flask import Blueprint, jsonify, current_app
import json

# Create a Blueprint for the product module
monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/monitor', methods=['GET'])
def get_monitor():
    """
    Retrieve product details based on the provided product_id.

    Args:
        product_id (str): The product ID to retrieve details for.

    Returns:
        JSON response: JSON object containing product details.
    """
    return {'message': 'alive'}, 200