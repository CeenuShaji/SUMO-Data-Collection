import xml.etree.ElementTree as ET
import csv

# Parse the FCD output file
tree = ET.parse('fcd_output.xml')
root = tree.getroot()

# Open a CSV file for writing
with open('fcd_output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(['time', 'id', 'x', 'y', 'angle', 'speed'])

    # Write data for each timestep and each vehicle
    for timestep in root.findall('timestep'):
        time = timestep.get('time')
        for vehicle in timestep.findall('vehicle'):
            writer.writerow([
                time,
                vehicle.get('id'),
                vehicle.get('x'),
                vehicle.get('y'),
                vehicle.get('angle'),
                vehicle.get('speed')
            ])