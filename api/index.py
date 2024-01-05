from flask import Flask, jsonify, request
from openai import OpenAI
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
client = OpenAI(api_key="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")


@app.route("/")
def main():
    return "ay yo motherfucker"


@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({'error': 'Missing prompt parameter'}), 400

        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return jsonify({'image_url': image_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_image_bytes_from_url(image_url):
    try:
        response = requests.get(image_url)

        # Kiểm tra xem request có thành công không (status code 200)
        if response.status_code == 200:
            # Lấy bytes của ảnh từ content của response
            image_bytes = response.content
            return image_bytes
        else:
            print(
                f"Failed to retrieve image from {image_url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


@app.route('/generate_image_with_image', methods=['POST'])
def generate_image_with_image():
    try:
        data = request.json
        image_url = data.get('image_url')
        n = data.get('n')
        size = data.get('size')
        if not image_url:
            return jsonify({'error': 'Missing parameter'}), 400
        image_bytes = get_image_bytes_from_url(image_url)
        response = client.images.create_variation(
            image=image_bytes,
            size=size,
            n=n,
        )
        generated_image_urls = []
        for variation in response.data:
            generated_image_urls.append(variation.url)
        return jsonify({"data": generated_image_urls}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/edit_image', methods=['POST'])
def edit_image():
    try:
        data = request.json
        image_url = data.get('image_url')
        mask = data.get("mask")
        prompt = data.get("prompt")
        n = data.get('n')
        size = data.get('size')
        if not image_url:
            return jsonify({'error': 'Missing parameter'}), 400
        image_bytes = get_image_bytes_from_url(image_url)
        mask_byte = get_image_bytes_from_url(mask)
        response = client.images.edit(
            image=image_bytes,
            mask=mask_byte,
            prompt=prompt,
            size=size,
            n=n,
        )
        generated_image_urls = []
        for variation in response.data:
            generated_image_urls.append(variation.url)
        return jsonify({"data": generated_image_urls}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
