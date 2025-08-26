# Complete Guide: Creating and Uploading a Python Package with Hidden Source Code to PyPI

This guide documents the complete process of creating a Python package with Cython-compiled source code and uploading it to PyPI.

## Prerequisites

- Python 3.6+ installed
- pip installed
- macOS (this guide creates macOS-only binaries)
- PyPI account (create at https://pypi.org/account/register/)

## Initial Setup

### Starting Directory Structure

We begin in a terminal with the following directory structure:

```
start_folder/
└── secretpackage/
    ├── secretpackage/
    │   ├── __init__.py
    │   ├── math_utils.py
    │   ├── string_utils.py
    │   └── data_utils.py
    ├── setup.py
    ├── pyproject.toml
    ├── README.md
    ├── LICENSE
    └── MANIFEST.in
```

## Step 1: Create the Package Structure

```bash
# Create main package directory
mkdir -p secretpackage/secretpackage

# Navigate to the package directory
cd secretpackage
```

## Step 2: Create Python Module Files

### Create `secretpackage/__init__.py`:
```python
from .math_utils import add, multiply, power
from .string_utils import reverse_string, capitalize_words, remove_spaces
from .data_utils import process_list, find_max_min, calculate_average

__version__ = "0.1.0"
__all__ = [
    'add', 'multiply', 'power',
    'reverse_string', 'capitalize_words', 'remove_spaces',
    'process_list', 'find_max_min', 'calculate_average'
]
```

### Create `secretpackage/math_utils.py`:
```python
def add(a, b):
    """Add two numbers together"""
    return a + b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def power(base, exponent):
    """Calculate base raised to the power of exponent"""
    return base ** exponent
```

### Create `secretpackage/string_utils.py`:
```python
def reverse_string(text):
    """Reverse a string"""
    return text[::-1]

def capitalize_words(text):
    """Capitalize first letter of each word"""
    return ' '.join(word.capitalize() for word in text.split())

def remove_spaces(text):
    """Remove all spaces from a string"""
    return text.replace(' ', '')
```

### Create `secretpackage/data_utils.py`:
```python
def process_list(data):
    """Process a list by removing duplicates and sorting"""
    return sorted(list(set(data)))

def find_max_min(data):
    """Find maximum and minimum values in a list"""
    if not data:
        return None, None
    return max(data), min(data)

def calculate_average(data):
    """Calculate average of a list of numbers"""
    if not data:
        return 0
    return sum(data) / len(data)
```

## Step 3: Create Package Configuration Files

### Create `setup.py`:
```python
from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import shutil

ext_modules = [
    Extension("secretpackage.math_utils", ["secretpackage/math_utils.py"]),
    Extension("secretpackage.string_utils", ["secretpackage/string_utils.py"]),
    Extension("secretpackage.data_utils", ["secretpackage/data_utils.py"]),
]

setup(
    name="secretpackage",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A secret package with hidden source code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/secretpackage",
    packages=["secretpackage"],
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': "3"}),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```

### Create `pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=45", "wheel", "Cython>=0.29"]
build-backend = "setuptools.build_meta"
```

### Create `README.md`:
```markdown
# SecretPackage

A demonstration package with compiled source code.

## Installation

```bash
pip install secretpackage
```

## Usage

```python
import secretpackage

# Math utilities
result = secretpackage.add(5, 3)
product = secretpackage.multiply(4, 7)
power = secretpackage.power(2, 8)

# String utilities
reversed_text = secretpackage.reverse_string("hello")
capitalized = secretpackage.capitalize_words("hello world")
no_spaces = secretpackage.remove_spaces("hello world")

# Data utilities
cleaned_list = secretpackage.process_list([3, 1, 4, 1, 5, 9])
max_val, min_val = secretpackage.find_max_min([1, 2, 3, 4, 5])
avg = secretpackage.calculate_average([1, 2, 3, 4, 5])
```

## License

MIT License
```

### Create `LICENSE`:
```
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Create `MANIFEST.in`:
```
include README.md
include LICENSE
exclude secretpackage/*.py
exclude secretpackage/*.pyc
include secretpackage/__init__.py
```

## Step 4: Install Build Dependencies

```bash
pip install build cython wheel twine
```

## Step 5: Compile Python Files to Binary Extensions

```bash
# Build Cython extensions in place
python setup.py build_ext --inplace
```

This creates `.so` files (on macOS) alongside your `.py` files:
- `secretpackage/math_utils.cpython-312-darwin.so`
- `secretpackage/string_utils.cpython-312-darwin.so`
- `secretpackage/data_utils.cpython-312-darwin.so`

## Step 6: Create a Modified Setup for Binary-Only Distribution

### Create `setup_simple.py`:
```python
from setuptools import setup, Extension, find_packages
import os

# Check if we're building from source or from compiled files
has_source = os.path.exists("secretpackage/math_utils.py")

if has_source:
    # Building from source - use Cython
    from Cython.Build import cythonize
    ext_modules = cythonize([
        Extension("secretpackage.math_utils", ["secretpackage/math_utils.py"]),
        Extension("secretpackage.string_utils", ["secretpackage/string_utils.py"]),
        Extension("secretpackage.data_utils", ["secretpackage/data_utils.py"]),
    ], compiler_directives={'language_level': "3"})
else:
    # Building from compiled files - just package them
    ext_modules = []

setup(
    name="secretpackage",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A secret package with hidden source code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/secretpackage",
    packages=find_packages(),
    ext_modules=ext_modules,
    package_data={
        'secretpackage': ['*.so', '*.pyd'],  # Include compiled extensions
    },
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```

## Step 7: Create Temporary Build Directory

```bash
# Create a temporary directory for building the wheel
mkdir -p secretpackage_temp/secretpackage

# Copy only necessary files (no .py source files except __init__.py)
cp secretpackage/__init__.py secretpackage_temp/secretpackage/
cp secretpackage/*.so secretpackage_temp/secretpackage/
cp README.md LICENSE pyproject.toml secretpackage_temp/
cp setup_simple.py secretpackage_temp/setup.py
```

## Step 8: Build the Wheel Distribution

```bash
# Navigate to the temporary directory
cd secretpackage_temp

# Build the wheel
python -m build --wheel
```

This creates a wheel file in `dist/`:
- `secretpackage-0.1.0-py3-none-any.whl`

## Step 9: Create PyPI Configuration

### Create `~/.pypirc`:
```bash
cat > ~/.pypirc << EOF
[pypi]
  username = __token__
  password = pypi-YOUR-API-TOKEN-HERE
EOF

# Set secure permissions
chmod 600 ~/.pypirc
```

**Important**: Replace `pypi-YOUR-API-TOKEN-HERE` with your actual PyPI API token obtained from:
1. Log in to https://pypi.org
2. Go to Account Settings → API tokens
3. Create new token
4. Copy the token (starts with `pypi-`)

## Step 10: Upload to PyPI

```bash
# Upload the wheel to PyPI
python -m twine upload dist/*
```

You should see output like:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading secretpackage-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View at:
https://pypi.org/project/secretpackage/0.1.0/
```

## Step 11: Test the Installation

```bash
# Uninstall any local version
pip uninstall -y secretpackage

# Install from PyPI
pip install secretpackage

# Test the package
python -c "import secretpackage; print(secretpackage.add(10, 20))"
# Output: 30
```

## Complete File Structure After Upload

```
secretpackage_temp/
├── secretpackage/
│   ├── __init__.py
│   ├── data_utils.cpython-312-darwin.so
│   ├── math_utils.cpython-312-darwin.so
│   └── string_utils.cpython-312-darwin.so
├── dist/
│   └── secretpackage-0.1.0-py3-none-any.whl
├── setup.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## Important Notes

1. **Platform Specific**: This creates a macOS-only package. The `.so` files only work on macOS.
2. **Python Version**: The compiled files are specific to Python 3.12 (noted by `cp312` in filename).
3. **Source Code**: The original `.py` files are not included in the distribution, making the source code hidden.
4. **Cross-Platform**: To support other platforms, you need to build on each platform separately or use CI/CD tools like GitHub Actions.

## Troubleshooting

### Authentication Error
If you get a 403 error when uploading:
- Check that your token is correctly pasted in `~/.pypirc`
- Ensure the token starts with `pypi-`
- Make sure there are no extra spaces or newlines

### Import Error on Other Platforms
If users on Windows or Linux get import errors:
- This is expected - the package only works on macOS
- You need to build platform-specific wheels for each OS

### Package Name Already Taken
If the package name is already taken on PyPI:
- Choose a different name in `setup.py`
- Update all references to the new name

## Next Steps

To make your package work on all platforms:
1. Set up GitHub Actions for automated multi-platform builds
2. Use `cibuildwheel` to build for all Python versions and platforms
3. Upload all platform-specific wheels to PyPI

Users will still just run `pip install secretpackage` and pip will automatically download the correct wheel for their platform.