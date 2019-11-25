# Run Backend

Command: `# python3 start_backed.py <options> ` 

Options | | Explaination 
 --- | --- | --- 
-h | --help | show help
-b BACKBONE | --backbone BACKBONE | Define backbone url. Default: http://smartcity.ddns.net:10000
-i IP | --ip IP | Define IP address of backend. Default:  0.0.0.0
-m MQTT | --mqtt MQTT | Define base mqtt topic. Default: smartcity/drones


# Start drone

Command: `# python3 start_drone.py <options> `

Options | | Explaination 
 --- | --- | --- 
-h | --help | show help
-s | --sim | Start a simulated drone.
-p PORT | --port PORT | Define port for drone executing process. Default: 5000
-m MARKER | --marker MARKER | Define the start position of the drone, by marker id.
-b BACKEND | --backend BACKEND | Set IP address of the backend to connect to. 
-a | --auto | Enable auto-arm functionality, works only for simulated drones.

# Start visualizer

Command: `# python3 DroneBackend/Visualizer.py`

# Start SimulationCore

Command: `# python3 DroneSimCore/SimulationCore.py <options>`

Options | | Explaination 
 --- | --- | --- 
-b BACKBONE | --backbone BACKBONE | Define backbone ip. Default: localhost
-i IP | --ip IP | Define IP address for communication. Default:  localhost
-p | --port | Define port for drone executing process. Default: 5000

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
* requests
