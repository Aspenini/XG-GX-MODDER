#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Check your Python installation or requirements.txt."
    exit 1
fi
echo "Starting Opera GX Mod Maker..."
python src/main.py
if [ $? -ne 0 ]; then
    echo "Failed to launch the app. Ensure src/main.py exists and Python is installed."
    exit 1
fi