from tourbillon import tourbillon
from tourbillon.calibre import get_now
from flask import jsonify


@tourbillon.route('/now', methods=['GET'])
def get_current_time():
    now = get_now()
    return jsonify({'now': now})
