# SmartDrone
Folder structure:
* DroneSim - simulator
* dronefw - drone driver
* DroneCore - drone core

##Dependencies
* numpy
* networkx
* matplotlib: to plot the map graph
* pygame - for visualizing the simulator

##JSON commands
{
            "command": ex. "move" or "turn",
            "goal": (x,y,z),
            "velocity": velocity,
            "angle": angle,          # angle not always necessary, only if the command is turn
            "height": height
}

