#!/usr/bin/env python3
"""
Build script to create a wheel package with only compiled extensions
"""
import os
import shutil
import subprocess
import sys
import tempfile

def build_package():
    print("Building compiled package without source...")
    
    # Install required packages
    print("Installing build dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "build", "cython", "wheel", "setuptools"])
    
    # Clean previous builds
    for dir in ["build", "dist", "*.egg-info"]:
        if os.path.exists(dir):
            shutil.rmtree(dir)
    
    # First, build the extensions
    print("Building Cython extensions...")
    subprocess.check_call([sys.executable, "setup.py", "build_ext", "--inplace"])
    
    # Create a temporary directory for building
    with tempfile.TemporaryDirectory() as temp_dir:
        print("Creating temporary build directory...")
        
        # Copy entire project to temp directory
        temp_project = os.path.join(temp_dir, "secretpackage_build")
        shutil.copytree(".", temp_project, ignore=shutil.ignore_patterns('*.pyc', '__pycache__', 'build', 'dist', '*.egg-info'))
        
        # Remove .py files (except __init__.py) from the package directory
        package_dir = os.path.join(temp_project, "secretpackage")
        for file in os.listdir(package_dir):
            if file.endswith('.py') and file != '__init__.py':
                os.remove(os.path.join(package_dir, file))
                print(f"Removed source file: {file}")
        
        # Build the wheel in the temp directory
        print("Building wheel...")
        original_dir = os.getcwd()
        os.chdir(temp_project)
        subprocess.check_call([sys.executable, "-m", "build", "--wheel", "--outdir", original_dir + "/dist"])
        os.chdir(original_dir)
    
    print("\nBuild complete!")
    print("Wheel file created in 'dist' directory")
    
    # List the created files
    if os.path.exists("dist"):
        files = os.listdir("dist")
        print("\nCreated files:")
        for file in files:
            print(f"  - {file}")
            
    print("\nTo upload to PyPI:")
    print("  python -m twine upload dist/*")
    
    print("\nTo test locally:")
    print("  pip install dist/*.whl")

if __name__ == "__main__":
    build_package()