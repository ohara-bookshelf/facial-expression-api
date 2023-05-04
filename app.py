from expression import Expression
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def hello_geek():
    return '<h1>Ohara API</h2>'


@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.json:
        return jsonify({'error': 'no image found'})

    image_data = request.json['image']
    # remove image header
    image_data = image_data.replace(
        "data:image/webp;base64,", "")

    # process the image
    camera = Expression(image_data)
    result = camera.get_result()

    return jsonify(result[0])


@app.errorhandler(Exception)
def handle_error(error):
    print(error)
    return 'An error occurred: {}'.format(error), 500


if __name__ == '__main__':
    app.run(debug=True)
