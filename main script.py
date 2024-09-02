import subprocess
from time import time

start_time = time()  #script start time
print("Starting main script...")

def main():
    try:
        # Run the ASYNC_serversideimagescrape.js script
        print("Running ASYNC_serversideimagescrape.js...")
        result = subprocess.run(['node', 'ASYNC_serversideimagescrape.js'], check=True)
        print("ASYNC_serversideimagescrape.js run completed successfully.")
        
        # Run the pixel_processing.py script
        print("Running pixel_processing.py...")
        result = subprocess.run(['python', 'pixel_processing.py'], check=True)
        print("pixel_processing.py run completed successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the scripts: {e}")
        return

if __name__ == "__main__":
    main()

end_time = time()
run_time = end_time - start_time
print("main script.py completed sucessfully!")
print(f"Total Run time: {run_time} seconds")