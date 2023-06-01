import os
import sys
import traci
import random
import csv

def is_emergency_vehicle(vid):
    # Determine if a vehicle is an emergency vehicle
    return traci.vehicle.getVehicleClass(vid) == "emergency"

def run():
    intersection_approach_distance = 30  # Distance to check for vehicles approaching intersection
    handled_vehicles = set()  # Keep track of vehicles that have been managed
    
    # Open a CSV file for writing the extended FCD output
    with open('extended_fcd_output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(['time', 'id', 'x', 'y', 'angle', 'speed', 'lane_id', 'acceleration'])

        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            vehicle_ids = traci.vehicle.getIDList()
            time = traci.simulation.getTime()

            for vid in vehicle_ids:
                # Fetch additional data
                x, y = traci.vehicle.getPosition(vid)
                angle = traci.vehicle.getAngle(vid)
                speed = traci.vehicle.getSpeed(vid)
                lane_id = traci.vehicle.getLaneID(vid)
                acceleration = traci.vehicle.getAcceleration(vid)

                # Check for null or undefined values and handle them
                lane_id = lane_id if lane_id else "unknown"  # Replace null lane_id with 'unknown'
                acceleration = acceleration if acceleration is not None else "0"  # Replace null acceleration with '0'

                # Write the extended FCD data to the CSV file
                writer.writerow([time, vid, x, y, angle, speed, lane_id, acceleration])

                # Additional logic for setting speed and acceleration...
                # ...

    traci.close()

if __name__ == "__main__":
    sumoCmd = ["sumo-gui", "-c", "sumoconfig.sumo.cfg"]
    traci.start(sumoCmd)
    run()
