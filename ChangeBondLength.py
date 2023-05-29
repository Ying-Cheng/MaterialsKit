#!/usr/bin/env python3
from ase.io import read
import numpy as np

atoms = read("4-body_95739.xyz", index=":")

for i in range(20):
    random_array = np.random.uniform(low=0.957/0.96, high=1/0.96, size=12*3).reshape(12, 3)
    print(f'rnd{random_array}')
    print(f'coord{atoms[0].positions}')
    atoms[0].positions = atoms[0].positions * random_array
    atoms[0].write(f'4-body_95739_{i+1}.xyz')
