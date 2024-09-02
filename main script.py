import subprocess
from time import time
from target_config import target_route

print(f"\033[96mTarget Route: {target_route}\033[0m")
start_time = time()  #script start time
print(f"Starting main script.........")

def main():
    try:
        # Run the serversideimagescrape.js script
        print("Running serversideimagescrape.js...")
        result = subprocess.run(['node', 'serversideimagescrape.js'], check=True)
        print(f"\033[96mserversideimagescrape.js run completed successfully.\033[0m")
        
        # Run the pixel_processing.py script
        print("Running pixel_processing.py...")
        result = subprocess.run(['python', 'pixel_processing.py'], check=True)
        print(f"\033[94mpixel_processing.py run completed successfully.\033[0m")
        
    except subprocess.CalledProcessError as e:
        print(f"\033[91mAn error occurred while running the scripts: {e}\033[0m")
        return

if __name__ == "__main__":
    main()

end_time = time()
run_time = end_time - start_time
print("\033[92mmain script.py completed sucessfully!\033[0m")
print(f"main script.py run time: {run_time} seconds")