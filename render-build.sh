#!/bin/bash

# Install system dependencies for OpenCV
apt-get update && apt-get install -y libgl1-mesa-glx

# Install Python dependencies
pip install -r requirements.txt