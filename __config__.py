# Description: Configuration file for the collector
import os

# Path to the configuration file, it should be in the same directory as this file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")

# check if the path is to a valid file
if not os.path.isfile(CONFIG_PATH):
    raise FileNotFoundError("Config file not found")
