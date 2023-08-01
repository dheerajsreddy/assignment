import requests
from flask import Blueprint, request, jsonify
import urllib.parse
import json

search_bp = Blueprint('search', __name__)

def create_search_bp():
    unbxd_api_url = f'https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search'

    @search_bp.route('/search', methods=['GET'])
    def search_products():
        search_query = request.args.get('q', '').strip()

        if not search_query:
            return jsonify({'message': 'Search query is missing or empty'}), 400

        if search_query.isdigit():
            try:
                # Perform an exact match search for SKU
                params = {'q': search_query}

                # Make the request to the Unbxd API for SKU search
                response = requests.get(unbxd_api_url, params=params)
                response.raise_for_status()

                # Process the response and extract relevant product information
                unbxd_data = response.json()
                search_results = unbxd_data.get('response', {}).get('products', [])

                if not search_results:
                    return jsonify({'message': 'No products found with the given query'}), 404

                # Format the search results with the required fields
                formatted_results = []
                for product in search_results:
                    sku = product.get('sku', '')
                    name = product.get('name', '')
                    price = float(product.get('price', 0.0))
                    product_description = product.get('productDescription', '')
                    product_image = product.get('productImage', '')

                    formatted_product = {
                        'sku': sku,
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

        else:
            try:
                # Perform a full-text search for exact match in the name field
                encoded_query = urllib.parse.quote(search_query, safe=' ')
                params = {'q': f'name:{encoded_query}'}

                # Make the request to the Unbxd API for alphabetic search
                response = requests.get(unbxd_api_url, params=params)
                response.raise_for_status()

                # Process the response and extract relevant product information
                unbxd_data = response.json()
                search_results = unbxd_data.get('response', {}).get('products', [])

                # Filter the exact match based on the name field
                exact_match_product = None
                for product in search_results:
                    name = product.get('name', '')
                    if name.lower() == search_query.lower():
                        exact_match_product = product
                        break

                if not exact_match_product:
                    return jsonify({'message': 'No products found with the given query'}), 404

                # Format the exact matched product with the required fields
                formatted_product = {
                    'sku': exact_match_product.get('sku', ''),
                    'name': exact_match_product.get('name', ''),
                    'price': float(exact_match_product.get('price', 0.0)),
                    'product_description': exact_match_product.get('productDescription', ''),
                    'product_image': exact_match_product.get('productImage', ''),
                }

                return jsonify(formatted_product), 200

            except requests.RequestException as e:
                return jsonify({'message': f'Error connecting to Unbxd API: {str(e)}'}), 500

            except json.JSONDecodeError as e:
                return jsonify({'message': 'Error parsing Unbxd API response'}), 500

    return search_bp
