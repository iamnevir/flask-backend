from flask import Flask
from flask_cors import CORS
from generation.endpoint import generation
from user.endpoint import user
from order.endpoint import order
from image.endpoint import image
app = Flask(__name__)
app.register_blueprint(generation, url_prefix='/generation')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(order, url_prefix='/order')
app.register_blueprint(image, url_prefix='/image')
CORS(app)


@app.route("/")
def main():
    return "ay yo heartsteal"


if __name__ == '__main__':
    app.run(debug=True)
