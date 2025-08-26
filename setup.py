from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import sys
import os

# Define extensions
extensions = [
    Extension("secretpackage.math_utils", ["secretpackage/math_utils.py"]),
    Extension("secretpackage.string_utils", ["secretpackage/string_utils.py"]),
    Extension("secretpackage.data_utils", ["secretpackage/data_utils.py"]),
]

# Platform-specific settings
if sys.platform == 'win32':
    # Windows specific flags if needed
    extra_compile_args = ['/O2']
    extra_link_args = []
else:
    # Unix-like systems (Linux, macOS)
    extra_compile_args = ['-O3', '-Wall']
    extra_link_args = []

# Apply platform-specific settings to all extensions
for ext in extensions:
    ext.extra_compile_args = extra_compile_args
    ext.extra_link_args = extra_link_args

setup(
    name="secretpackage",
    version="0.2.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="A secret package with hidden source code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/guochen2011gc/secretpackage",
    packages=find_packages(),
    ext_modules=cythonize(extensions, compiler_directives={
        'language_level': "3",
        'boundscheck': False,
        'wraparound': False,
    }),
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