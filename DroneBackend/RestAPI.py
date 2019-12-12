
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


@app.route('/addDrone/<unique_msg>')
def add_drone(unique_msg):
    global global_backend
    reply = global_backend.add_drone(int(unique_msg))
    return json.dumps(reply)

@app.route('/removeDrone/<drone_id>')
def remove_drone(drone_id):
    global global_backend
    result = "true" if global_backend.remove_drone(drone_id) else "false"
    return json.dumps({"result": result})


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
    cost = global_backend.flightplanner.calculate_cost_time(int(pidstart), int(pidend))
    return json.dumps({"cost": int(cost)})


@app.route('/job/execute/<pidstart>/<pidend>/<jobid>', methods=['POST', 'GET'])
def add_job(pidstart, pidend, jobid):
    try:
        global global_backend
        job = {
            "point1": int(pidstart),
            "point2": int(pidend),
            "job_id": int(jobid)
        }
        global_backend.jobs[int(jobid)] = job
        global_backend.db.add_job(job)
        return json.dumps({"status": "success"})
    except: return json.dumps({"status": "false"})


@app.route('/job/getprogress/<job_id>')
def get_progress(job_id):
    global global_backend
    if int(job_id) in global_backend.jobs.keys():
        progress = 0
    elif global_backend.job_in_active_jobs(int(job_id)):
        progress = 50
    else:
        progress = 100
    return json.dumps({ "progress": progress })


@app.route('/getlocation/<drone_id>')
def get_location(drone_id):
    global global_backend
    location = "invalid drone id"
    if int(drone_id) in global_backend.drones.keys():
        location = global_backend.db.get_location(int(drone_id))
    return json.dumps({"location": location})

@app.route('/getlocations/')
def get_locations():
    global global_backend
    locations = {
            "locations": [],
        }

    for drone_id in global_backend.drones.keys():
        location = global_backend.db.get_location(int(drone_id))
        locations["locations"].append(location)
    return json.dumps(locations)



@app.route('/job/cancel/<job_id>')
def cancel_job(job_id):
    global global_backend
    result = "false"
    if job_id in global_backend.jobs.keys():
        del global_backend.jobs[job_id]
        result = "true"
    #TODO: if job is active, maybe land drone at first possible marker and remove job from active job list
    return json.dumps({"success": result})
