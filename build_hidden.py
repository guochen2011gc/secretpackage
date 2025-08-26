#!/usr/bin/env python3
"""
Build script to create a wheel package with compiled Cython extensions only
"""
import os
import shutil
import subprocess
import sys

def build_package():
    print("Building compiled package...")
    
    # Install required packages
    print("Installing build dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "build", "cython", "wheel"])
    
    # Clean previous builds
    for dir in ["build", "dist", "*.egg-info"]:
        if os.path.exists(dir):
            shutil.rmtree(dir)
    
    # Build the extensions
    print("Building Cython extensions...")
    subprocess.check_call([sys.executable, "setup.py", "build_ext", "--inplace"])
    
    # Create a temporary copy of the package without .py files
    print("Creating distribution package...")
    temp_dir = "temp_secretpackage"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    shutil.copytree("secretpackage", temp_dir)
    
    # Remove .py files except __init__.py
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                os.remove(os.path.join(root, file))
    
    # Move compiled files to temp directory
    for file in os.listdir("secretpackage"):
        if file.endswith(('.so', '.pyd')):
            shutil.copy2(os.path.join("secretpackage", file), 
                        os.path.join(temp_dir, file))
    
    # Replace original with temp
    shutil.rmtree("secretpackage")
    shutil.move(temp_dir, "secretpackage")
    
    # Build the wheel
    print("Building wheel...")
    subprocess.check_call([sys.executable, "-m", "build", "--wheel"])
    
    print("\nBuild complete! Check the 'dist' directory for your wheel file.")
    print("You can now upload it to PyPI using: python -m twine upload dist/*")

if __name__ == "__main__":
    build_package()