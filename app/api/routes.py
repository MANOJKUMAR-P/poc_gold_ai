from flask import Blueprint, jsonify

bp = Blueprint('api', __name__)

@bp.route('/ping')
def ping():
    return jsonify({'status': 'ok'})
