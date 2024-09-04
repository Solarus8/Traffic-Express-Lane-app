import subprocess
from time import time

from logger import logger
from pixel_processing import process_pixels
from target_config import target_route

logger.info(f"\033[96mTarget Route: {target_route}\033[0m")
start_time = time()  # script start time
logger.info(f"Starting main script.........")


def main():
    try:
        # Run the serversideimagescrape.js script
        logger.info("Running serversideimagescrape.js...")
        result = subprocess.run(["node", "serversideimagescrape.js"], check=True)
        logger.info(
            f"\033[96mserversideimagescrape.js run completed successfully.\033[0m"
        )

        # Run the pixel_processing.py script
        logger.info("Running pixel_processing.py...")

        result = process_pixels()
        logger.info(f"\033[94mpixel_processing.py run completed successfully.\033[0m")

    except subprocess.CalledProcessError as e:
        logger.info(f"\033[91mAn error occurred while running the scripts: {e}\033[0m")
        return


if __name__ == "__main__":
    main()

end_time = time()
run_time = end_time - start_time
logger.info("\033[92mmain script.py completed sucessfully!\033[0m")
logger.info(f"main script.py run time: {run_time} seconds")
