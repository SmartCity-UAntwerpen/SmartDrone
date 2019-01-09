# SmartDrone
Folder structure:
* Common
* DroneBackend - backend
* DroneCore - drone core
* DroneSim - simulator
* DroneSimCore - abstraction level above real simulator
* dronefw - drone driver


## Dependencies
* pymysql
* networkx
* flask
* pygame
* paho.mqtt.client
* uuid
* numpy

## JSON commands
{
            "command": ex. "move" or "turn",
            "goal": (x,y,z),
            "velocity": velocity,
            "angle": angle,          # angle not always necessary, only if the command is turn
            "height": height
}

Job:\
{ \
    "action": job,  
    "point1": marker_id,\
    "point2": marker_id,\
    //"priority": priority\
    }
