
import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
    print("Please provide a file name as an argument.")
    sys.exit(1)

file_name = sys.argv[1]
print("File name:", file_name)

# Define the regular expressions for matching the desired patterns
energy_regex = r"SCF Done:  E\((.*?)\) =\s+(-?\d+\.\d+)\s+A\.U\.\safter\s+\d+\scycles"
path_number_regex = r"Path Number:\s+(\d+)"
net_reaction_regex = r"NET REACTION COORDINATE UP TO THIS POINT =\s+(-?\d+\.\d+)"

# Initialize lists to store the parsed data for each path
path1_energies = []
path1_net_coordinates = []
path2_energies = []
path2_net_coordinates = []

# Open and read the file
with open(file_name, "r") as file:
    contents = file.read()

# Find all matches for energy, path number, and net reaction coordinate
energy_matches = re.findall(energy_regex, contents)
path_number_matches = re.findall(path_number_regex, contents)
net_reaction_matches = re.findall(net_reaction_regex, contents)

# Assign the first energy_match to net coordinate 0.0
if energy_matches:
    method, energy = energy_matches[0]
    path1_energies.append(float(energy))
    path1_net_coordinates.append(0.0)

# Iterate over the remaining matches and store the data for each path
for energy_match, path_number_match, net_reaction_match in zip(energy_matches[1:], path_number_matches, net_reaction_matches):
    method, energy = energy_match
    net_reaction = float(net_reaction_match)

    if path_number_match == '1':
        path1_energies.append(float(energy))
        path1_net_coordinates.append(net_reaction)
    elif path_number_match == '2':
        path2_energies.append(float(energy))
        path2_net_coordinates.append(-net_reaction)  # Change the sign for path 2

# Convert the lists to numpy arrays
path1_energies = np.array(path1_energies)
path1_net_coordinates = np.array(path1_net_coordinates)
path2_energies = np.array(path2_energies)
path2_net_coordinates = np.array(path2_net_coordinates)

# Remove duplicates from path 1 data
path1_energies, unique_indices = np.unique(path1_energies, return_index=True)
path1_net_coordinates = path1_net_coordinates[unique_indices]

# Remove duplicates from path 2 data
path2_energies, unique_indices = np.unique(path2_energies, return_index=True)
path2_net_coordinates = path2_net_coordinates[unique_indices]
# Plot both paths together
plt.scatter(path1_net_coordinates, path1_energies, marker="o", label="Forward")
plt.scatter(path2_net_coordinates, path2_energies, marker="o", label="Reverse")
plt.xlabel("Net Reaction Coordinate")
plt.ylabel("Energy (a.u.)")
plt.title("Energy vs Net Reaction Coordinate")
plt.legend()
plt.grid(True)
plt.show()
