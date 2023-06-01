import os
import sys
import traci
import random

def is_emergency_vehicle(vid):
    return traci.vehicle.getVehicleClass(vid) == "emergency"

def run():
    intersection_approach_distance = 30  # Distance to check for vehicles approaching intersection
    handled_vehicles = set()  # Keep track of vehicles that have been managed
    resumed_vehicles = set()  # Keep track of vehicles that have resumed movement

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehicles_at_intersection = set()
        vehicle_ids = traci.vehicle.getIDList()

        for vid in vehicle_ids:
            if is_emergency_vehicle(vid):
                # Emergency vehicles are given immediate priority
                traci.vehicle.setSpeed(vid, traci.vehicle.getMaxSpeed(vid))
            else:
                # For non-emergency vehicles
                random_accel = random.uniform(1.5, 2.5)  # Random acceleration
                random_speed = random.uniform(10, 15)    # Random maximum speed
                traci.vehicle.setAccel(vid, random_accel)
                traci.vehicle.setMaxSpeed(vid, random_speed)
                
        for lane in traci.lane.getIDList():
            vehicles = traci.lane.getLastStepVehicleIDs(lane)
            for vid in vehicles:
                pos = traci.vehicle.getLanePosition(vid)
                lane_length = traci.lane.getLength(lane)
                # Check if vehicle is close to the end of the lane, thus approaching an intersection
                if lane_length - pos < intersection_approach_distance and vid not in resumed_vehicles:
                    vehicles_at_intersection.add(vid)

        # Handle vehicles at the intersection
        for vid in vehicles_at_intersection:
            if vid not in handled_vehicles and not is_emergency_vehicle(vid):
                # Stop non-emergency vehicles temporarily
                traci.vehicle.setSpeed(vid, 0)
                handled_vehicles.add(vid)

        # Allow the first vehicle in FIFO to proceed
        if len(handled_vehicles) > 0:
            first_vehicle = min(handled_vehicles, key=lambda v: traci.vehicle.getLanePosition(v))
            traci.vehicle.setSpeed(first_vehicle, traci.vehicle.getMaxSpeed(first_vehicle))
            handled_vehicles.remove(first_vehicle)
            resumed_vehicles.add(first_vehicle)

    traci.close()

if __name__ == "__main__":
    sumoCmd = ["sumo-gui", "-c", "sumoconfig.sumo.cfg"]
    traci.start(sumoCmd)
    run()
