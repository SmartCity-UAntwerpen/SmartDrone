# SmartDrone
Folder structure:
* DroneSim - simulator
* dronefw - drone driver
* DroneCore - drone core

## Dependencies
* numpy
* networkx
* matplotlib: to plot the map graph
* pygame - for visualizing the simulator
* flask - REST

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
