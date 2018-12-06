#!/usr/bin/env bash

if [ -z ${1+x} ]; then echo "Enter port as parameter.";
else
cd DroneSim
python DroneSimulator.py $1 &
cd ../DroneCore
python Controller.py $1;
fi

