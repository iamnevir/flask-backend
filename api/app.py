from flask import Flask, jsonify, request
from openai import OpenAI
import requests
import base64
from BingImageCreator import ImageGen
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
client = OpenAI(api_key="")


@app.route("/")
def main():
    return "ay yo"


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


@app.route('/bing_gen', methods=['POST'])
def bing_gen():
    try:
        data = request.json
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({'error': 'Missing prompt parameter'}), 400

        image_generator = ImageGen(
            "1OM-hdpkbvySzbwXS6aD1N2n7WbUhp_y2wpwPDNUyViQB2VIRHNqsycXXdFTWXY2bEkHmh8Y8PySVj06cDOObi_BGR7SaCNAa_-wIom58v17U4WP9eY6P3NuQQwDQ0YETZBODKK8gCdHXsfySddgV5l86N-DG2bsLPifmjfKuoPiZPD9u7KIJK27Eq7YLuquRY7xco-roj8_B01c9aCy-8w", "")
        imgs = image_generator.get_images(prompt)
        return jsonify({'images': imgs}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate_imagine', methods=['POST'])
def generate_imagine():
    try:
        data = request.json
        prompt = data.get('prompt')
        style_id = data.get('style_id')
        negative_prompt = data.get('negative_prompt')
        if not prompt or not style_id:
            return jsonify({'error': 'Missing parameter'}), 400

        url = 'https://api.vyro.ai/v1/imagine/api/generations'

        headers = {
            'Authorization': 'Bearer vk-3OwHbdqCSGISorOpEf0nD4N0oq80oO1fgcZZlpi3nnc58'
        }

        # Using None here allows us to treat the parameters as string
        payload = {
            'prompt': (None, prompt),
            'style_id': (None, style_id),
            'negative_prompt': (None, negative_prompt)
        }
        response = requests.post(url, headers=headers, files=payload)
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return jsonify({'image_base64': image_base64}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/img_gen', methods=['POST'])
def img_gen():
    try:
        data = request.json
        prompt = data.get('prompt')
        model = data.get('model')
        if not prompt:
            return jsonify({'error': 'Missing parameter'}), 400
        urls = [
            "https://api-inference.huggingface.co/models/openskyml/dalle-3-xl",
            "https://api-inference.huggingface.co/models/dataautogpt3/OpenDalleV1.1",
            "https://api-inference.huggingface.co/models/Norod78/SDXL-YarnArtStyle-LoRA",
            "https://api-inference.huggingface.co/models/segmind/SSD-1B",
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
        ]
        headers = {
            "Authorization": "Bearer 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"}

        def query(payload):
            res = requests.post(urls[model], headers=headers, json=payload)
            return res.content
        image_bytes = query({
            "inputs": prompt
        })
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        return jsonify({'image_base64': image_base64}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/rm_bg', methods=['POST'])
def rm_bg():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'Missing url parameter'}), 400
        response = requests.get(url)
        r = requests.post('https://clipdrop-api.co/remove-background/v1',
                          files={
                              'image_file':  response.content,
                          },
                          headers={
                              'x-api-key': 'af6537c64a511dcc5090e9c192e391f1b46eba0212e7705f52d4bc3f5d35e32546735c16703d982b4daff96f23507e7e'}
                          )
        image_base64 = base64.b64encode(r.content).decode('utf-8')
        return jsonify({'image_base64': image_base64}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/imagine_upscale', methods=['POST'])
def imagine_upscale():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'Missing url parameter'}), 400
        response = requests.get(url)
        url = 'https://api.vyro.ai/v1/imagine/api/upscale'
        payload = {
            'image': ('filename.png', response.content, 'image/png')
        }
        headers = {
            'Authorization': 'Bearer vk-3OwHbdqCSGISorOpEf0nD4N0oq80oO1fgcZZlpi3nnc58'
        }

        response = requests.post(url, headers=headers, files=payload)
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return jsonify({'image_base64': image_base64}), 200
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


# if __name__ == '__main__':
#     app.run(debug=True)
