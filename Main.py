
              main.py


import multiprocessing
from itertools import permutations
import time
import os

def perm_worker_to_file(args):
    fixed_elem, rest, filename = args
    with open(filename, 'w') as f:
        for p in permutations(rest):
            perm = [fixed_elem] + list(p)
            f.write(str(perm) + '\n')
    return filename

def parallel_permutations_to_file(arr, output_dir="perm_output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    tasks = []
    for i in range(len(arr)):
        fixed = arr[i]
        rest = arr[:i] + arr[i+1:]
        filename = os.path.join(output_dir, f"perm_{fixed}.txt")
        tasks.append((fixed, rest, filename))
    with multiprocessing.Pool(processes=min(len(tasks), multiprocessing.cpu_count())) as pool:
        return pool.map(perm_worker_to_file, tasks)

def combine_files_to_single_output(file_list, output_file="combined_permutations.txt"):
    with open(output_file, 'w') as outfile:
        for fname in file_list:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

if __name__ == "__main__":
    arr = [1,2,3,4,5,6,7,8,9,10]
    start_time = time.time()
    files = parallel_permutations_to_file(arr)
    combine_files_to_single_output(files)
    end_time = time.time()
    print(f"Total Time Taken: {end_time - start_time:.2f} seconds")
