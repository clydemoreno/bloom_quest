import subprocess
import multiprocessing

def run_huffman_compression(_):  # Added an underscore to indicate no arguments
    subprocess.run(["python3", "huffman_test.py"])

def run_rle_compression(_):  # Added an underscore to indicate no arguments
    subprocess.run(["python3", "./ext/gzip_compression.py"])

if __name__ == "__main__":
    num_processes = 2
    
    with multiprocessing.Pool(num_processes) as pool:
        pool.map(run_huffman_compression, range(num_processes))
        pool.map(run_rle_compression, range(num_processes))
