#!/usr/bin/env bash

if [ -z ${1+x} ]; then echo "Enter port as parameter.";
else
python ./DroneSim/DroneSimulator.py $1 & python ./DroneCore/Controller.py $1;
fi

