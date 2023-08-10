from flask import Blueprint

# Create a Blueprint for the monitor module
monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/monitor', methods=['GET'])
def get_monitor():
    return {'message': 'alive'}, 200