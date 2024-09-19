import datetime
import logging
from flask import Flask, jsonify, request
import json

app = Flask(__name__)
books = [{'id': 1, 'title': 'Python Essentials', 'author': 'Jane Doe'}]


class Tracker:
    def __init__(self) -> None:
        self.tracker = {}
    
    def is_zone_occupied(self, zone):
        first, second = self.tracker.get(zone, (None, None))
        return first != None
    
    def set_zone_empty(self, zone):
        self.tracker[zone] = (None, None)
    
    def set_zone_occupied(self, zone, first_event):
        self.tracker[zone] = (first_event, None)
    
    def update_zone_last_event(self, zone, last_event):
        self.tracker[zone] = (self.tracker[zone][0], last_event)


tracker = Tracker()


timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

file = open(f'{timestr}.txt', 'w')

def print_status():
    print("Zone statuses:")
    for zone in tracker.tracker:
        print(f'{zone}: {tracker.is_zone_occupied(zone)}')

def ok():
    return {}, 200

@app.route('/', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/', methods=['POST'])
def post_data():
    data = request.get_json()
    if data == None or "Events" not in data or "event" not in data["Events"]:
        print("data or events or events-event was none!")
        return ok()
    
    if data["Events"]["event"]["@type"] != "alarm":
        print("event wasnt an alarm")
        return ok()
    
    zone = data["Events"]["event"]["spy-name"]
    print(zone + " event")

    return {}, 200

if __name__ == '__main__':
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(debug=True, port=5050)
    file.close()