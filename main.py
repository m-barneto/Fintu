import logging
from flask import Flask, jsonify, request
import json

app = Flask(__name__)
books = [{'id': 1, 'title': 'Python Essentials', 'author': 'Jane Doe'}]

ongoing = set()

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
    
    for event in data["Events"]["event"]:
        if (event["status"] != "new"):
            pass #continue
        #event["frame"]["attribute"] = []
        event["attribute"] = []
        print(event["@id"])
        #print(json.dumps(event, indent=2))
        ongoing.add(event["status"])
        print(ongoing)

    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= data), 200

if __name__ == '__main__':
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(debug=True, port=5050)