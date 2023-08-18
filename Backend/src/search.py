import requests
from flask import Blueprint, request
import json

search_bp = Blueprint('search', __name__)

class NotAlphanumericError(Exception):
    def __init__(self, message="The input must be alphanumeric"):
        self.message = message
        super().__init__(self.message)
        
unbxd_api_url = f'https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search'

@search_bp.route('/search', methods=['GET'])
def search_products():
    search_query = request.args.get('q', '').strip()

    if not search_query:
        return {'message': 'Search query is missing or empty'}, 400

    try:
        search_query_copy=search_query.replace(" ","")
        if search_query_copy.isalpha() or search_query.isdigit():
            # Perform an exact match search for SKU
            params = {'q': search_query}

            # Make the request to the Unbxd API for SKU search
            response = requests.get(unbxd_api_url, params=params)
            response.raise_for_status()

            # Process the response and extract relevant product information
            unbxd_data = response.json()
            search_results = unbxd_data.get('response', {}).get('products', [])

            if not search_results:
                return {'message': 'No products found with the given query'}, 404

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

            return formatted_results, 200
        else:
            raise NotAlphanumericError("The input should not be alphanumeric")
            
    except NotAlphanumericError as e:
        return {'message': f'Query string is alphanumeric: {str(e)}'}, 500
                
    except requests.RequestException as e:
        return {'message': f'Error connecting to Unbxd API: {str(e)}'}, 500

    except json.JSONDecodeError as e:
        return {'message': 'Error parsing Unbxd API response'}, 500
