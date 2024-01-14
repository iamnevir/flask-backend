from flask import Blueprint
from flask import jsonify, request
from convex import ConvexClient
order = Blueprint('order', __name__)
client = ConvexClient("https://whimsical-lyrebird-215.convex.cloud")


@order.route('/', methods=['GET'])
def get():
    try:

        orders = client.query("order:getorders")
        return jsonify({'orders': orders}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@order.route('/by_user', methods=['GET'])
def by_user():
    try:
        data = request.json
        userId = data.get('userId')
        orders = client.query("order:getorderByorder", {"userId": userId})
        return jsonify({'orders': orders}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@order.route('/create', methods=['POST'])
def create():
    try:
        data = request.json
        userId = data.get('userId')
        isPay = data.get('isPay')

        if not userId:
            return jsonify({'error': 'Missing userId parameter'}), 400
        client.mutation("order:create", dict(
            userId=userId,
            isPay=isPay,
        ))
        return 'Created', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
