
from flask import Flask
import json

app = Flask("DroneBackend")

global_backend = None


class RestApi():

    def __init__(self, backend):
        if backend is not None:
            global  global_backend
            global_backend = backend
            app.run(global_backend.ip, global_backend.port)
        else:
            print("REST API not able to start correctly (backend is NoneType)")


@app.route('/link/transitmap')
def transitmap_api():
    data = json.loads(open('carlinks.json').read())
    return json.dumps(data)


@app.route('/link/flagtransitmap')
def flagtransitmap_api():
    pass


@app.route('/addDrone/<unique_msg>')
def add_drone(unique_msg):
    global global_backend
    reply = global_backend.add_drone(int(unique_msg))
    return json.dumps(reply)


@app.route('/removeDrone/<drone_id>')
def remove_drone(drone_id):
    global global_backend
    reply = global_backend.remove_drone(drone_id)
    return json.dumps(reply)


@app.route('/getMarkers/')
def get_markers():
    global global_backend
    markers = {}
    for marker in global_backend.markers:
        markers[marker] = global_backend.markers[marker].get_dict()
    reply = { "markers": markers }
    return json.dumps(reply)


@app.route('/<pidstart>/<pidend>')
def calculate_cost(pidstart, pidend):
    global global_backend
    try: cost = global_backend.flightplanner.calculate_cost(int(pidstart), int(pidend))
    except: cost = 9999999
    return json.dumps({ "cost": cost })


@app.route('/job/execute/<pidstart>/<pidend>/<jobid>')
def add_job(pidstart, pidend, jobid):
    try:
        global global_backend
        job = {
            "point1": int(pidstart),
            "point2": int(pidend),
            "job_id": int(jobid)
        }
        global_backend.jobs[int(jobid)] = job
        return json.dumps({"status": "success"})
    except: return json.dumps({"status": "false"})
