#!/usr/bin/env python3

import itertools
import os

def read_xyz(file_path):
    frames = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        frame_start = 0
        while frame_start < len(lines):
            num_atoms = int(lines[frame_start].strip())
            comment_line = lines[frame_start + 1].strip()
            frame = {
                "num_atoms": num_atoms,
                "comment_line": comment_line,
                "atom_info": []
            }
            for i in range(frame_start + 2, frame_start + num_atoms + 2):
                line = lines[i].strip().split()
                atom_info = {
                    "atom_name": line[0],
                    "x": float(line[1]),
                    "y": float(line[2]),
                    "z": float(line[3])
                }
                frame["atom_info"].append(atom_info)
            frames.append(frame)
            frame_start += num_atoms + 2
    return frames

def get_atom_mass(element_symbol):
    atomic_masses = {
    'H': 1.00794,
    'O': 15.999,
    'C': 12.0107,
    'N': 14.0067,
    # Add more elements and their masses here
}
    return atomic_masses.get(element_symbol, 0.0)  # Default to 0.0 if element not found

def calculate_center_of_mass(molecule):
    total_mass = 0.0
    center_of_mass = [0.0, 0.0, 0.0]
    for atom in molecule:
        mass = get_atom_mass(atom["atom_name"])  # You'll need to implement get_atom_mass function
        total_mass += mass
        for i, coord in enumerate(["x", "y", "z"]):
            center_of_mass[i] += atom[coord] * mass
    for i in range(3):
        center_of_mass[i] /= total_mass
    return center_of_mass

def distance_between_points(point1, point2):
    return ((point1[0] - point2[0])**2 +
            (point1[1] - point2[1])**2 +
            (point1[2] - point2[2])**2) ** 0.5

if __name__ == "__main__":
    added_name = "DCOM"
    # Get a list of all files in the current directory
    current_directory = os.getcwd()
    files_in_directory = os.listdir(current_directory)
    # Filter only the XYZ files
    input_files = [filename for filename in files_in_directory if filename.endswith(".xyz") and added_name not in filename]
    combined_frames = {}
    for xyz_file in input_files:
        # Replace 'filename.xyz' with the actual filename
        frames = read_xyz(xyz_file)
        # Calculate distances between water molecules' centers of mass and the entire frame
        for frame_index, frame in enumerate(frames):
            num_atoms = frame["num_atoms"]
            comment_line = frame["comment_line"]
            atom_info_list = frame["atom_info"]
            center_of_mass_frame = calculate_center_of_mass(atom_info_list)
            water_molecules = [atom_info_list[i:i + 3] for i in range(0, num_atoms, 3)]
            dist_list = []
            for molecule in water_molecules:
                center_of_mass_molecule = calculate_center_of_mass(molecule)
                dist = distance_between_points(center_of_mass_frame, center_of_mass_molecule)
                dist_list.append(f"{round(dist, 0):.0f}")
            dist_list.sort()  # Sort the list of distances in-place

            frame_filename = f"{os.path.splitext(xyz_file)[0]}_frame_{frame_index + 1}.xyz"
            frame["comment_line"] = f"{comment_line} frame_filename= {frame_filename}"

            dist_key = "_".join(dist_list)
            if dist_key in combined_frames:
                combined_frames[dist_key]["frames"].append(frame)
            else:
                combined_frames[dist_key] = {"frames": [frame]}

    # Save combined frames for each dist_key
    for dist_key, data in combined_frames.items():
        combined_filename = f"DCOM_{dist_key}.xyz"
        with open(combined_filename, 'w') as out_f:
            for combined_frame in data["frames"]:
                num_atoms = combined_frame["num_atoms"]
                comment_line = combined_frame["comment_line"]
                atom_info_list = combined_frame["atom_info"]
                out_f.write(f"{num_atoms}\n{comment_line}\n")
                for atom_info in atom_info_list:
                    out_f.write(f"{atom_info['atom_name']} {atom_info['x']:.6f} {atom_info['y']:.6f} {atom_info['z']:.6f}\n")
        print(f"Combined frames saved to '{combined_filename}'")                                                                                                             
