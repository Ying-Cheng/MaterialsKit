#!/usr/bin/env python3

import itertools
import os

def read_xyz_file(filename):
    frames = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        frame_start = 0
        while frame_start < len(lines):
            num_atoms = int(lines[frame_start].strip())
            frame = []
            for i in range(frame_start + 2, frame_start + num_atoms + 2):
                line = lines[i].strip().split()
                atom_info = [line[0], float(line[1]), float(line[2]), float(line[3])]
                frame.append(atom_info)
            frames.append(frame)
            frame_start += num_atoms + 2
    return frames

def find_duplicated_frames(frames):
    # This function finds frames with duplicate atoms (overlapping coordinates) and keeps track of the indices of the duplicated atoms within each frame.
    duplicated_frames = {}
    not_duplicated_atom = []
    for frame_idx, frame in enumerate(frames):
        duplicated_atom_idx = []
#        print(f'frmae: {frame}\n')
        for atom_idx, atom in enumerate(frame):
            if atom in not_duplicated_atom:
                duplicated_atom_idx.append(atom_idx)
            else:
                not_duplicated_atom.append(atom)
        if duplicated_atom_idx:
#            print(f'duplicated_atom_idx: {duplicated_atom_idx}\n')
#            print(f'frame_idx: {frame_idx}\n')
            duplicated_frames[frame_idx] = duplicated_atom_idx
#            print(f'duplicated_frames: {duplicated_frames}\n')
    return duplicated_frames

def find_duplicated_coordinates(filename):
    # This function takes the results from find_duplicated_frames and finds coordinates that are duplicated across different frames. It keeps track of which frames contain those duplicated coordinates.
    frames = read_xyz_file(filename)
    duplicated_frames = find_duplicated_frames(frames)
    duplicated_coordinates = {}
    for frame_idx, duplicate_indices in duplicated_frames.items():
        for coord_idx in duplicate_indices:
            coord = frames[frame_idx][coord_idx]
            coord_tuple = tuple(coord)  # Convert the list to a tuple
            if coord_tuple in duplicated_coordinates:
                duplicated_coordinates[coord_tuple].append(frame_idx)
            else:
                duplicated_coordinates[coord_tuple] = [frame_idx]
#    print(f'duplicated_coordinates: {duplicated_coordinates}\n')
    return duplicated_coordinates

def combine_frames(frames, duplicated_coordinates):
    unique_frames = []
    for frame_idx, frame in enumerate(frames):
        for idx, other_frame in enumerate(frames):
            if frame_idx >= idx:
                continue
            merged_frame = set(tuple(atom) for atom in frame)
            other_frame = set(tuple(atom) for atom in other_frame)
            if merged_frame.intersection(other_frame):
                merged_frame = merged_frame.union(other_frame)
                unique_frames.append((merged_frame, frame_idx, idx))
    return unique_frames

if __name__ == "__main__":
    added_name = "overlapped_frame_pairs"
    # Get a list of all files in the current directory
    current_directory = os.getcwd()
    files_in_directory = os.listdir(current_directory)
    # Filter only the XYZ files
    input_files = [filename for filename in files_in_directory if filename.endswith(".xyz") and added_name not in filename]
    for xyz_file in input_files:
        duplicated_coordinates = find_duplicated_coordinates(xyz_file)
        frames = read_xyz_file(xyz_file)
        unique_frame_pairs = combine_frames(frames, duplicated_coordinates)
        # Get the base name of the input file (excluding directory and extension)
        base_name = os.path.splitext(os.path.basename(xyz_file))[0]
        output_file = f"{base_name}_{added_name}.xyz"
        with open(output_file, 'w') as f:
            for i, (frame, frame_idx, other_frame_idx) in enumerate(unique_frame_pairs, start=1):
                num_atoms = len(frame)
                f.write(f"{num_atoms:4d}\n")  # Use 4 bytes for the number of atoms
                f.write(f"The union of {base_name}.xyz's frames: {frame_idx + 1:2d} and {other_frame_idx + 1:2d}\n")  # Use 2 bytes for frame indices
                for atom_info in frame:
                    atom, x, y, z = atom_info
                    f.write(f"{atom:2s} {x:12.6f} {y:12.6f} {z:12.6f}\n")  # Use 12 bytes for each coordinate (including spaces)
        print(f"Unions of overlapped frame pairs written to {output_file}")
