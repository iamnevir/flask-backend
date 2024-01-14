from flask import Blueprint
from flask import jsonify, request
from convex import ConvexClient
user = Blueprint('user', __name__)
client = ConvexClient("https://whimsical-lyrebird-215.convex.cloud")


@user.route('/', methods=['GET'])
def get():
    try:
        users = client.query("user:getUsers")
        return jsonify({'users': users}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user.route('/by_user', methods=['POST'])
def by_user():
    try:
        data = request.json
        userId = data.get('userId')
        user = client.query("user:getUserByUser", {"userId": userId})
        return jsonify({'user': user}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user.route('/create', methods=['POST'])
def create():
    try:
        data = request.json
        userId = data.get('userId')

        if not userId:
            return jsonify({'error': 'Missing userId parameter'}), 400
        client.mutation("user:create", dict(
            userId=userId,
            like=[],
            upload=[],
            coin=150,
            isPro=False,
        ))
        return 'Created', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user.route('/update', methods=['POST'])
def update():
    try:
        data = request.json
        userId = data.get('userId')
        if not userId:
            return jsonify({'error': 'Missing userId parameter'}), 400
        username = data.get('username')
        favorite = data.get('favorite')
        like = data.get('like')
        upload = data.get('upload')
        coin = data.get('coin')
        isPro = data.get('isPro')
        isAdmin = data.get('isAdmin')
        mutation_args = {
            "id": userId,
            "username": username,
            "favorite": favorite,
            "like": like,
            "upload": upload,
            "coin": int(coin) if coin is not None else None,
            "isPro": isPro,
            "isAdmin": isAdmin,
        }
        filtered_args = {key: value for key,
                         value in mutation_args.items() if value is not None}
        client.mutation("user:update", dict(filtered_args))
        return 'Updated', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user.route('/remove', methods=['POST'])
def remove():
    try:
        data = request.json
        userId = data.get('userId')
        if not userId:
            return jsonify({'error': 'Missing userId parameter'}), 400
        client.mutation("user:remove", dict(id=userId))
        return 'Removed', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
