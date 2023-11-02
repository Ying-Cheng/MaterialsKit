#!/usr/bin/env python3

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

if __name__ == "__main__":
    certain_frame_index = [20, 30]
    added_name = "Frame"
    current_directory = os.getcwd()
    files_in_directory = os.listdir(current_directory)
    input_files = [filename for filename in files_in_directory if filename.endswith(".xyz") and added_name not in filename]
    for xyz_file in input_files:
        frames = read_xyz(xyz_file)
        for frame_index in certain_frame_index:
            xyz_filename = xyz_file.split('.')[0]
            certain_frame_filename = f"{xyz_filename}_Frame_{frame_index}.xyz"
            with open(certain_frame_filename, 'w') as out_f:
                num_atoms = frames[frame_index+1]["num_atoms"]
                comment_line = frames[frame_index+1]["comment_line"]
                atom_info_list = frames[frame_index+1]["atom_info"]
                out_f.write(f"{num_atoms}\n{comment_line}\n")
                for atom_info in atom_info_list:
                    out_f.write(f"{atom_info['atom_name']} {atom_info['x']:.6f} {atom_info['y']:.6f} {atom_info['z']:.6f}\n")
            print(f"Frame {frame_index} of {xyz_filename}.xyz saved to '{certain_frame_filename}'")
