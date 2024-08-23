from flask import Flask, jsonify, request
import requests
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def main():
    return "ay yo"


@app.route("/generate_imagine", methods=["POST"])
def generate_imagine():
    try:
        data = request.json
        prompt = data.get("prompt")
        style_id = data.get("style_id")
        negative_prompt = data.get("negative_prompt")
        if not prompt or not style_id:
            return jsonify({"error": "Missing parameter"}), 400

        url = "https://api.vyro.ai/v1/imagine/api/generations"

        headers = {
            "Authorization": "Bearer vk-3OwHbdqCSGISorOpEf0nD4N0oq80oO1fgcZZlpi3nnc58"
        }

        # Using None here allows us to treat the parameters as string
        payload = {
            "prompt": (None, prompt),
            "style_id": (None, style_id),
            "negative_prompt": (None, negative_prompt),
        }
        response = requests.post(url, headers=headers, files=payload)
        image_base64 = base64.b64encode(response.content).decode("utf-8")
        return jsonify({"image_base64": image_base64}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/img_gen", methods=["POST"])
def img_gen():
    try:
        data = request.json
        prompt = data.get("prompt")
        model = data.get("model")
        if not prompt:
            return jsonify({"error": "Missing parameter"}), 400
        urls = [
            "https://api-inference.huggingface.co/models/Norod78/SDXL-YarnArtStyle-LoRA",
            "https://api-inference.huggingface.co/models/segmind/SSD-1B",
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
        ]
        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            res = requests.post(urls[model], headers=headers, json=payload)
            return res.content

        image_bytes = query({"inputs": prompt})
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        return jsonify({"image_base64": image_base64}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/animagine", methods=["POST"])
def animagine():
    try:
        data = request.json
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "Missing parameter"}), 400
        url = (
            "https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.0"
        )

        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            res = requests.post(url=url, headers=headers, json=payload)
            return res.content

        image_bytes = query({"inputs": prompt})
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        return jsonify({"image_base64": image_base64}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/rm_bg", methods=["POST"])
def rm_bg():
    try:
        data = request.json
        url = data.get("url")

        if not url:
            return jsonify({"error": "Missing url parameter"}), 400
        response = requests.get(url)
        r = requests.post(
            "https://clipdrop-api.co/remove-background/v1",
            files={
                "image_file": response.content,
            },
            headers={
                "x-api-key": "af6537c64a511dcc5090e9c192e391f1b46eba0212e7705f52d4bc3f5d35e32546735c16703d982b4daff96f23507e7e"
            },
        )
        image_base64 = base64.b64encode(r.content).decode("utf-8")
        return jsonify({"image_base64": image_base64}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/imagine_upscale", methods=["POST"])
def imagine_upscale():
    try:
        data = request.json
        url = data.get("url")

        if not url:
            return jsonify({"error": "Missing url parameter"}), 400
        response = requests.get(url)
        url = "https://api.vyro.ai/v1/imagine/api/upscale"
        payload = {"image": ("filename.png", response.content, "image/png")}
        headers = {
            "Authorization": "Bearer vk-3OwHbdqCSGISorOpEf0nD4N0oq80oO1fgcZZlpi3nnc58"
        }

        response = requests.post(url, headers=headers, files=payload)
        image_base64 = base64.b64encode(response.content).decode("utf-8")
        return jsonify({"image_base64": image_base64}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
                f"Failed to retrieve image from {image_url}. Status code: {response.status_code}"
            )
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8051)
