from setuptools import setup, find_packages
import os
import sys

# This is a simplified setup.py that only packages compiled files
# Check what files are actually available
package_dir = "secretpackage"
if os.path.exists(package_dir):
    print(f"Files in {package_dir}:")
    for file in os.listdir(package_dir):
        print(f"  {file}")

setup(
    name="secretpackage",
    version="0.2.6",
    author="Your Name",
    author_email="your.email@example.com",
    description="A secret package with hidden source code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/guochen2011gc/secretpackage",
    packages=find_packages(),
    package_data={
        'secretpackage': ['*.so', '*.pyd', '*.dll'],
    },
    include_package_data=True,
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10", 
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
)