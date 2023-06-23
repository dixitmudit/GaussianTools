#!/usr/bin/env python3
# Author: Mudit Dixit
# CompCELL
# Organization: CSIR-CLRI
# Year: 2023


################################################################################
# Extract SCF energies and Free energies from Gaussian output files in the current directory #
################################################################################

import sys
import os
import argparse

#--------------------------------------------------------------------------------------------------------#
### parse commandline options ###
parser = argparse.ArgumentParser(description='Extract SCF energies and Free energies from Gaussian output in this dir')
parser.add_argument(
        '-f', metavar='<string>', dest='filename',
        default='scf_free_energies.txt', help='filename for storing SCF energies and Free energies')

args = parser.parse_args()
#--------------------------------------------------------------------------------------------------------#

all_files = os.listdir(".")
g09_files = []
# create list with Gaussian 09 output files
for file in all_files:
    if file.endswith(".log"):
        g09_files.append(file)

# open file for writing energies
output = open(args.filename, "w")

# loop over Gaussian 09 output files and extract energies
energies = {}
for entry in g09_files:
    scf_energy = None
    free_energy = None
    basis_set = None
    functional = None
    normal_termination = False
    with open(entry, "r") as file:
        for line in file:
            if line.strip().startswith("SCF Done"):
                scf_energy = float(line.strip().split()[4])
            if line.strip().startswith("Sum of electronic and thermal Free Energies"):
                free_energy = float(line.strip().split()[6])
            if line.strip().startswith("SCF Done:"):
                functional = line.strip().split()[2]
            if line.strip().startswith("NBasis="):
                basis_set = line.strip().split()[1]
            if line.strip().startswith("normal termination"):
                normal_termination = True
    if scf_energy is not None:
        if free_energy is None:
            print("Warning: Could not find Free energy for " + entry + " - Perform a frequency calculation.")
            energies[entry] = (scf_energy, None, basis_set, functional)
        else:
            energies[entry] = (scf_energy, free_energy, basis_set, functional)
    if not normal_termination:
        print("Warning: " + entry + " did not terminate properly!")

# sort entries according to scf energy
sorted_entries = sorted(energies.keys(), key=lambda x: energies[x][0])

# write to file
output.write("{:<20s} {:<18s} {:<18s} {:<18s} {:<18s}\n".format("File", "SCF Energy", "Free Energy", "NBasis", "Energy for Functional"))
for entry in sorted_entries:
    scf_energy, free_energy, basis_set, functional = energies[entry]
    output.write("{:<20s} {:<18.6f} ".format(entry[:-4], scf_energy))
    if free_energy is not None:
        output.write("{:<18.6f} ".format(free_energy))
    else:
        output.write("{:<18s} ".format("N/A"))
    output.write("{:<18s} {:<18s}\n".format(basis_set if basis_set is not None else "N/A",
                                           functional if functional is not None else "N/A"))

# close the output file
output.close()
