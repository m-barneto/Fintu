from datetime import time
import logging
from flask import Flask, jsonify, request
import json

app = Flask(__name__)
books = [{'id': 1, 'title': 'Python Essentials', 'author': 'Jane Doe'}]

ongoing = {}

timestr = time.strftime("%Y%m%d-%H%M%S")

file = open(f'{timestr}.txt', 'w')

@app.route('/', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/', methods=['POST'])
def post_data():
    data = request.get_json()
    if data == None or data["Events"] == None:
        return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data = data), 200
    
    file.write(json.dumps(data, indent=4))

    # for event in data["Events"]["event"]:
    #     if (event["status"] != "new"):
    #         pass #continue
    #     #event["frame"]["attribute"] = []
    #     event["attribute"] = []

    
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= data), 200

if __name__ == '__main__':
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(debug=True, port=5050)
    file.close()