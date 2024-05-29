import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
