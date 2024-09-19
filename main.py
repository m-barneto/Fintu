import datetime
import logging
import time
from flask import Flask, jsonify, request
import json

app = Flask(__name__)
books = [{'id': 1, 'title': 'Python Essentials', 'author': 'Jane Doe'}]

global timeout
timeout = time.time() + 15

class ZoneState:
    def __init__(self, first_conf) -> None:
        self.conf = [ first_conf ]
    
    def get_min(self):
        return min(self.conf)
    
    def get_max(self):
        return max(self.conf)
    
    def get_mean(self):
        return round(sum(self.conf) / len(self.conf), 2)

    def get_median(self):
        self.conf.sort()
        return self.conf[int(len(self.conf) / 2)]

class Tracker:
    def __init__(self) -> None:
        self.tracker = {}

    def ensure_zone_exists(self, zone):
        if zone not in self.tracker:
            print(f"Created zone {zone}")
            self.tracker[zone] = (None, None, None)
    
    def is_zone_occupied(self, zone):
        first, second, third = self.tracker.get(zone, (None, None, None))
        return first != None
    
    def set_zone_empty(self, zone):
        self.tracker[zone] = (None, None, None)
    
    def set_zone_occupied(self, zone, first_event):
        self.tracker[zone] = (first_event, None, ZoneState(get_confidence(first_event["attribute"])))
    
    def update_zone_last_event(self, zone, last_event):
        state = self.tracker[zone][2]
        state.conf.append(get_confidence(last_event["attribute"]))
        self.tracker[zone] = (self.tracker[zone][0], last_event, state)


tracker = Tracker()


def print_status():
    print("Zone statuses:")
    for zone in tracker.tracker:
        print(f'{zone}: {tracker.is_zone_occupied(zone)}')

def get_confidence(attributes):
    for attribute in attributes:
        if ":occupancy-conf" in attribute["@name"]:
            return float(attribute["#text"])
    return None

def ok():
    return {}, 200

@app.route('/', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/', methods=['POST'])
def post_data():
    global timeout
    json_data = request.get_json(silent=True)
    if json_data == None or json_data["Events"] == None or json_data["Events"]["event"] == None:
        print("No data/events/events.event")
        return ok()
    
    for data in json_data["Events"]["event"]:
        #print(json.dumps(data, indent=4))
        if "@type" not in data or data["@type"] != "alarm":
            #print("not alarm???")
            return ok()
        
        if "spy-name" not in data:
            print(json.dumps(data, indent=4))
            return ok()

        zone = data["spy-name"]
        if zone == "Test Spy":
            return ok()
        
        tracker.ensure_zone_exists(zone)

        event_zone_occupied = True
        if "Empty" in data["subtitle"]:
            event_zone_occupied = False

        event = data

        if tracker.is_zone_occupied(zone):
            if event_zone_occupied:
                # if its occupied, we want to update the last_event with this event
                tracker.update_zone_last_event(zone, event)

            else:
                # was occupied, this event says its not, so we need to send out our notif!!!
                print("HOLY MOLY ItS HAPPENING!!!!!!")
                print(f"Event Conf Min: {tracker.tracker[zone][2].get_min()}")
                print(f"Event Conf Max: {tracker.tracker[zone][2].get_max()}")
                print(f"Event Conf Mean: {tracker.tracker[zone][2].get_mean()}")
                print(f"Event Conf Median: {tracker.tracker[zone][2].get_median()}")
                print(f"Event Conf Latest: {tracker.tracker[zone][2].conf[-1]}")
                tracker.set_zone_empty(zone)
                print(f"Set {zone} as empty.")
                pass
        elif event_zone_occupied:
            # zone is not occupied, but now this event says it is, set first_event up
            tracker.set_zone_occupied(zone, event)
            print(f"Set {zone} as occupied!")
        else:
            # zone not occupied
            pass

        if time.time() > timeout and event_zone_occupied:
            timeout = time.time() + 15
            print(f"Event Conf Min: {tracker.tracker[zone][2].get_min()}")
            print(f"Event Conf Max: {tracker.tracker[zone][2].get_max()}")
            print(f"Event Conf Mean: {tracker.tracker[zone][2].get_mean()}")
            print(f"Event Conf Median: {tracker.tracker[zone][2].get_median()}")
            print(f"Event Conf Latest: {tracker.tracker[zone][2].conf[-1]}")

    return {}, 200

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(debug=True, port=5050)