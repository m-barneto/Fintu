from flask import Flask, jsonify, request
import json

app = Flask(__name__)
books = [{'id': 1, 'title': 'Python Essentials', 'author': 'Jane Doe'}]

@app.route('/', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/', methods=['POST'])
def post_data():
    data = request.form
    print(json.dumps(request.get_json(), indent=2))
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= data), 200

if __name__ == '__main__':
    app.run(debug=True, port=5050)