import os
import json
import requests
from flask import Blueprint, request, jsonify

search_bp = Blueprint('search', __name__)

# Function to create and return the 'search_bp' object
def create_search_bp():
    # Prepare the request URL for the Unbxd API
    unbxd_api_url = f'https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search'

    @search_bp.route('/search', methods=['GET'])
    def search_products():
        # Get the search query from the request parameters
        search_query = request.args.get('q', '').strip()

        if not search_query:
            return jsonify({'message': 'Search query is missing or empty'}), 400

        try:
            # Prepare the request URL for the Unbxd API
            params = {'q': search_query}

            # Make the request to the Unbxd API
            response = requests.get(unbxd_api_url, params=params)
            response.raise_for_status()  # Raise an exception if the request fails

            # Process the response and extract relevant product information
            unbxd_data = response.json()
            search_results = unbxd_data.get('response', {}).get('products', [])

            # Format the search results with the required fields
            formatted_results = []
            for product in search_results:
                product_id = product.get('productId', '')
                name = product.get('name', '')
                price = float(product.get('price', 0.0))
                product_description = product.get('productDescription', '')
                product_image = product.get('productImage', '')

                formatted_product = {
                    'product_id': product_id,
                    'name': name,
                    'price': price,
                    'product_description': product_description,
                    'product_image': product_image,
                }
                formatted_results.append(formatted_product)

            return jsonify(formatted_results), 200

        except requests.RequestException as e:
            return jsonify({'message': f'Error connecting to Unbxd API: {str(e)}'}), 500

        except json.JSONDecodeError as e:
            return jsonify({'message': 'Error parsing Unbxd API response'}), 500

    return search_bp
