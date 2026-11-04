#!/usr/bin/env python3

"""
Test script to verify the Python environment and virtual environment setup.
"""

import sys
import os

def main():
    print("Python version:", sys.version)
    print("Python executable:", sys.executable)
    print("Current working directory:", os.getcwd())
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("SUCCESS: Running in a virtual environment")
    else:
        print("WARNING: Not running in a virtual environment")

if __name__ == "__main__":
    main()