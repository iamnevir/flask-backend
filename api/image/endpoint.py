from flask import Blueprint
from flask import jsonify, request
from convex import ConvexClient
image = Blueprint('image', __name__)
client = ConvexClient("https://whimsical-lyrebird-215.convex.cloud")


@image.route('/', methods=['GET'])
def get():
    try:
        cursor = None
        done = False
        result = []
        while not done:
            images = client.query("image:getImages", {"paginationOpts": {
                "numItems": 20, "cursor": cursor}})
            cursor = images['continueCursor']
            done = images["isDone"]
            result.extend(images['page'])
        return jsonify({'images': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@image.route('/by_user', methods=['POST'])
def by_user():
    try:
        data = request.json
        userId = data.get('userId')
        cursor = None
        done = False
        result = []
        while not done:
            images = client.query("image:getImageByUser", {"paginationOpts": {
                "numItems": 20, "cursor": cursor, "userId": userId}})
            cursor = images['continueCursor']
            done = images["isDone"]
            result.extend(images['page'])
        return jsonify({'images': images}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@image.route('/create', methods=['POST'])
def create():
    try:
        data = request.json
        prompt = data.get('prompt')
        negativePrompt = data.get('negativePrompt')
        url = data.get('url')
        userId = data.get('userId')
        isPublish = data.get('isPublish')
        likes = data.get('likes')
        model = data.get('model')
        size = data.get('size')

        if not userId or not prompt or not url or not likes or not model or not size or not isPublish:
            return jsonify({'error': 'Missing userId parameter'}), 400
        mutation_args = {
            "prompt": prompt,
            "negativePrompt": negativePrompt,
            "url": url,
            "userId": userId,
            "isPublish": isPublish,
            "likes": int(likes) if likes is not None else None,
            "model": model,
            "size": size,
        }
        filtered_args = {key: value for key,
                         value in mutation_args.items() if value is not None}
        client.mutation("image:create", dict(filtered_args))
        return 'Created', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@image.route('/update', methods=['POST'])
def update():
    try:
        data = request.json
        id = data.get('id')
        if not id:
            return jsonify({'error': 'Missing id parameter'}), 400
        isPublish = data.get('isPublish')
        likes = data.get('likes')
        mutation_args = {
            "id": id,
            "isPublish": isPublish,
            "likes": int(likes) if likes is not None else None,
        }
        filtered_args = {key: value for key,
                         value in mutation_args.items() if value is not None}
        client.mutation("image:update", dict(filtered_args))
        return 'Updated', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@image.route('/remove', methods=['POST'])
def remove():
    try:
        data = request.json
        id = data.get('id')
        if not id:
            return jsonify({'error': 'Missing id parameter'}), 400
        client.mutation("image:remove", dict(id=id))
        return 'Removed', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
