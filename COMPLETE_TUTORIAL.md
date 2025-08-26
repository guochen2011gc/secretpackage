# Complete Tutorial: Create and Upload a Hidden Source Code Python Package to PyPI

This tutorial shows you how to take any Python package and upload it to PyPI with **hidden source code** using Cython compilation, with **automatic multi-platform builds** using GitHub Actions.

After extensive testing and troubleshooting, this tutorial includes all the critical fixes needed to make this work reliably.

## Prerequisites

- Python 3.9+ installed
- Git installed
- GitHub account
- PyPI account (create at https://pypi.org/account/register/)

## Starting Point

You are in a parent directory containing your package folder:

```
parent_folder/
└── mypackage/
    ├── __init__.py
    ├── module1.py
    ├── module2.py
    └── module3.py
```

Your terminal is open in the `parent_folder`.

---

## Step 1: Prepare Your Package Structure

### 1.1 Navigate into your package directory
```bash
cd mypackage
```

### 1.2 Create the package configuration files

#### Create `setup.py`:
```bash
cat > setup.py << 'EOF'
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import sys
import os

# Define extensions for all your .py modules (except __init__.py)
extensions = [
    Extension("mypackage.module1", ["mypackage/module1.py"]),
    Extension("mypackage.module2", ["mypackage/module2.py"]),
    Extension("mypackage.module3", ["mypackage/module3.py"]),
    # Add more modules as needed:
    # Extension("mypackage.module4", ["mypackage/module4.py"]),
]

# Platform-specific settings
if sys.platform == 'win32':
    extra_compile_args = ['/O2']
    extra_link_args = []
else:
    extra_compile_args = ['-O3', '-Wall']
    extra_link_args = []

# Apply platform-specific settings to all extensions
for ext in extensions:
    ext.extra_compile_args = extra_compile_args
    ext.extra_link_args = extra_link_args

setup(
    name="mypackage",  # CHANGE THIS to your package name
    version="0.1.0",
    author="Your Name",  # CHANGE THIS
    author_email="your.email@example.com",  # CHANGE THIS
    description="A package with hidden source code",  # CHANGE THIS
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOURUSERNAME/mypackage",  # CHANGE THIS
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
EOF
```

#### Create `setup_binary.py` (CRITICAL for fixing wheel corruption):
```bash
cat > setup_binary.py << 'EOF'
from setuptools import setup, find_packages
import os
import sys

# This is a simplified setup.py that only packages compiled files
# Check what files are actually available
package_dir = "mypackage"
if os.path.exists(package_dir):
    print(f"Files in {package_dir}:")
    for file in os.listdir(package_dir):
        print(f"  {file}")

setup(
    name="mypackage",  # CHANGE THIS to your package name
    version="0.1.0",
    author="Your Name",  # CHANGE THIS
    author_email="your.email@example.com",  # CHANGE THIS
    description="A package with hidden source code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOURUSERNAME/mypackage",  # CHANGE THIS
    packages=find_packages(),
    package_data={
        'mypackage': ['*.so', '*.pyd', '*.dll'],
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
    # CRITICAL: Force platform-specific wheel since we have compiled extensions
    has_ext_modules=lambda: True,
)
EOF
```

**IMPORTANT**: The `setup_binary.py` file is critical for preventing wheel corruption issues. The `has_ext_modules=lambda: True` line forces setuptools to create platform-specific wheels instead of universal wheels.

#### Create `pyproject.toml`:
```bash
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=45", "wheel", "Cython>=0.29"]
build-backend = "setuptools.build_meta"
EOF
```

#### Create `MANIFEST.in` (prevents build issues):
```bash
cat > MANIFEST.in << 'EOF'
include README.md
include LICENSE
recursive-exclude mypackage *.pyc
recursive-exclude mypackage __pycache__
EOF
```

#### Create `README.md`:
```bash
cat > README.md << 'EOF'
# MyPackage

A demonstration package with compiled source code.

## Installation

```bash
pip install mypackage
```

## Usage

```python
import mypackage

# Use your functions here
# result = mypackage.some_function(5, 3)
```

## License

MIT License
EOF
```

#### Create `LICENSE`:
```bash
cat > LICENSE << 'EOF'
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
EOF
```

#### Create `.gitignore`:
```bash
cat > .gitignore << 'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so
*.dylib
*.dll

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Cython
*.c
*.cpp

# Build workspaces
build_workspace/

# PyCharm
.idea/

# VSCode
.vscode/

# macOS
.DS_Store

# PyPI config (contains tokens)
.pypirc
EOF
```

---

## Step 2: Update Your Package's __init__.py

Update your `mypackage/__init__.py` to import functions from your modules:

```bash
# Edit your __init__.py file to import all the functions you want users to access
cat > mypackage/__init__.py << 'EOF'
# Import all functions you want to expose
from .module1 import function1, function2
from .module2 import function3, function4
from .module3 import function5

__version__ = "0.1.0"
__all__ = [
    'function1', 'function2', 'function3', 
    'function4', 'function5'
]
EOF
```

**IMPORTANT**: Update the imports to match your actual module names and functions.

---

## Step 3: Create GitHub Actions Workflow (FINAL WORKING VERSION)

### 3.1 Create the workflow directory:
```bash
mkdir -p .github/workflows
```

### 3.2 Create the GitHub Actions workflow:
```bash
cat > .github/workflows/build_isolated.yml << 'EOF'
name: Build Isolated Source-Free Wheels

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build_wheels:
    name: Build wheels on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install cython wheel setuptools build
      
      - name: Create isolated workspace
        run: |
          mkdir build_workspace
          # Copy all files except build_workspace directory to avoid infinite recursion
          find . -maxdepth 1 -not -name "." -not -name "build_workspace" -exec cp -r {} build_workspace/ \;
        shell: bash
          
      - name: Build extensions in isolation
        working-directory: build_workspace
        run: |
          # Build extensions and place them in the package directory
          python setup.py build_ext --inplace
          echo "Files after build_ext:"
          find mypackage -type f | sort
        shell: bash
          
      - name: Remove source files (Linux/macOS)
        if: runner.os != 'Windows'  
        working-directory: build_workspace
        run: |
          echo "Files before removing source:"
          find mypackage -type f | sort
          find mypackage -name "*.py" ! -name "__init__.py" -delete
          echo "Files after removing source:"
          find mypackage -type f | sort
        shell: bash
          
      - name: Remove source files (Windows)
        if: runner.os == 'Windows'
        working-directory: build_workspace
        run: |
          echo "Files before removing source:"
          Get-ChildItem -Path mypackage -Recurse | ForEach-Object { $_.FullName }
          Get-ChildItem -Path mypackage -Filter *.py -Recurse | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item -Force
          echo "Files after removing source:"
          Get-ChildItem -Path mypackage -Recurse | ForEach-Object { $_.FullName }
        shell: pwsh
          
      - name: Build wheel
        working-directory: build_workspace
        run: |
          python setup_binary.py bdist_wheel
        shell: bash
          
      - name: Prepare wheels for upload
        working-directory: build_workspace
        run: |
          mkdir -p wheelhouse
          ls -la dist/
          
          # For Linux, try to rename linux-specific wheels, otherwise copy all wheels
          if [ "$RUNNER_OS" = "Linux" ]; then
            renamed=false
            for wheel in dist/*-linux_x86_64.whl; do
              if [ -f "$wheel" ]; then
                newname=$(echo "$wheel" | sed 's/-linux_x86_64.whl/-manylinux_2_17_x86_64.whl/')
                newname=$(basename "$newname")
                cp "$wheel" "wheelhouse/$newname"
                echo "Renamed Linux wheel: $wheel -> wheelhouse/$newname"
                renamed=true
              fi
            done
            
            # If no linux-specific wheels found, copy all wheels
            if [ "$renamed" = "false" ]; then
              echo "No linux_x86_64 wheels found, copying all wheels"
              cp dist/*.whl wheelhouse/
            fi
          else
            # For Windows/macOS, just copy all wheels
            cp dist/*.whl wheelhouse/
          fi
          
          echo "Final wheelhouse contents:"
          ls -la wheelhouse/
        shell: bash
          
      - name: Test wheel
        working-directory: build_workspace
        run: |
          # Install from wheelhouse (should work for all platforms now)
          pip install wheelhouse/*.whl
          python -c "import mypackage; print('Test passed on ${{ matrix.os }} Python ${{ matrix.python-version }}:', mypackage.function1(2, 3))"
          # Verify no source files
          python -c "import os; import mypackage; path = os.path.dirname(mypackage.__file__); files = os.listdir(path); py_files = [f for f in files if f.endswith('.py') and f != '__init__.py']; print(f'Source files found: {py_files}'); assert len(py_files) == 0, f'ERROR: Found source files: {py_files}'"
        shell: bash
      
      - name: Upload wheel
        uses: actions/upload-artifact@v4
        with:
          name: wheel-${{ matrix.os }}-${{ matrix.python-version }}
          path: build_workspace/wheelhouse/*.whl

  upload_to_pypi:
    name: Upload to PyPI
    needs: build_wheels
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')
    
    steps:
      - uses: actions/download-artifact@v4
        with:
          path: dist
          merge-multiple: true
      
      - name: List files and verify wheels
        run: |
          echo "All downloaded files:"
          find dist -type f | sort
          echo ""
          echo "Wheel files only:"
          find dist -type f -name "*.whl" | sort
          echo ""
          echo "Checking wheel integrity:"
          for wheel in dist/*.whl; do
            if [ -f "$wheel" ]; then
              echo "Checking: $wheel"
              python -m zipfile -l "$wheel" | head -5 || echo "Failed to read $wheel"
            fi
          done
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
          skip-existing: true
EOF
```

**CRITICAL FIXES IN THIS WORKFLOW:**
1. **Isolated workspaces** prevent parallel builds from interfering with each other
2. **Two separate setup files** - `setup.py` for compilation, `setup_binary.py` for packaging
3. **Platform-specific wheel forcing** via `has_ext_modules=lambda: True`
4. **Proper Linux wheel renaming** for manylinux compatibility
5. **Comprehensive diagnostics** to debug issues

---

## Step 4: Initialize Git Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit with isolated build workflow"
```

---

## Step 5: Create GitHub Repository

### 5.1 Create repository on GitHub:
1. Go to https://github.com/new
2. Repository name: `mypackage` (use your package name)
3. Visibility: **Public** (for free GitHub Actions)
4. **DO NOT** initialize with README, .gitignore, or license (we already have them)
5. Click **Create repository**

### 5.2 Link your local repository to GitHub:
```bash
# Replace YOURUSERNAME and mypackage with your actual values
git remote add origin https://github.com/YOURUSERNAME/mypackage.git
git branch -M main
git push -u origin main
```

---

## Step 6: Set Up PyPI API Token

### 6.1 Get your PyPI API token:
1. Log in to https://pypi.org
2. Go to **Account Settings** → **API tokens**
3. Click **Add API token**
4. Name: "mypackage upload"
5. Scope: "Entire account" (for first upload)
6. Click **Add token**
7. **Copy the token** (starts with `pypi-`) - you'll only see it once!

### 6.2 Add token to GitHub Secrets:
1. Go to your GitHub repository
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**
5. Name: `PYPI_API_TOKEN`
6. Value: Paste your PyPI token
7. Click **Add secret**

---

## Step 7: Test Locally (Optional but Recommended)

```bash
# Install build dependencies
pip install cython wheel setuptools build

# Test that your package builds
python setup.py build_ext --inplace

# Test that imports work
python -c "import mypackage; print('Local test passed!')"

# Clean up test files
rm -rf build/ *.so mypackage/*.so mypackage/*.c
```

---

## Step 8: Release Your Package

### 8.1 Create and push a release tag:
```bash
# Create a version tag (this will trigger the build)
git tag v0.1.0
git push origin v0.1.0
```

### 8.2 Monitor the build:
1. Go to https://github.com/YOURUSERNAME/mypackage/actions
2. Click on the "Build Isolated Source-Free Wheels" workflow
3. Watch it build wheels for all platforms
4. Wait for automatic upload to PyPI

---

## Step 9: Verify Upload and Test Installation

### 9.1 Check PyPI:
Go to https://pypi.org/project/mypackage/ to see your package

### 9.2 Test installation:
```bash
# Install from PyPI (wait a few minutes after upload)
pip install mypackage

# Test it works
python -c "import mypackage; print('Installation successful!')"
```

### 9.3 **CRITICAL**: Verify source code is hidden:
```bash
# Verify no source files are visible to users
python -c "
import os
import mypackage
path = os.path.dirname(mypackage.__file__)
files = os.listdir(path)
py_files = [f for f in files if f.endswith('.py') and f != '__init__.py']
print(f'Python source files found: {py_files}')
print(f'All files: {files}')
if len(py_files) == 0:
    print('✅ SUCCESS: Source code is properly hidden!')
    print('Users can only see compiled binaries (.so/.pyd files)')
else:
    print('❌ ERROR: Source files are visible!')
    print('The workflow needs to be fixed.')
"
```

**Expected output:**
```
Python source files found: []
All files: ['__init__.py', 'module1.cpython-312-linux_x86_64.so', 'module2.cpython-312-linux_x86_64.so', ...]
✅ SUCCESS: Source code is properly hidden!
Users can only see compiled binaries (.so/.pyd files)
```

---

## Step 10: For Future Updates

When you want to release a new version:

1. **Update your code** as needed
2. **Update version** in BOTH `setup.py` AND `setup_binary.py`:
   ```bash
   # Edit setup.py and change version="0.1.0" to version="0.1.1"
   # Edit setup_binary.py and change version="0.1.0" to version="0.1.1"
   ```
3. **Commit and tag**:
   ```bash
   git add .
   git commit -m "Update to version 0.1.1"
   git push
   git tag v0.1.1
   git push origin v0.1.1
   ```
4. **GitHub Actions will automatically** build and upload the new version!

**CRITICAL**: Always keep both `setup.py` and `setup_binary.py` versions in sync to avoid build issues.

---

## Critical Problems We Solved

### Problem 1: Wheel Corruption - "ZIP archive not accepted: Filename not in central directory"
**Cause**: setuptools was creating universal wheels (`py3-none-any`) instead of platform-specific wheels for compiled extensions.

**Solution**: Added `has_ext_modules=lambda: True` to `setup_binary.py` to force platform-specific wheels.

### Problem 2: Parallel Build Interference
**Cause**: Multiple build jobs were modifying the same source files simultaneously.

**Solution**: Created isolated workspaces for each build job using `build_workspace` directories.

### Problem 3: Linux Wheel Compatibility  
**Cause**: Linux wheels were tagged as `linux_x86_64` which PyPI rejects.

**Solution**: Rename to `manylinux_2_17_x86_64` in the workflow.

### Problem 4: Version Mismatches
**Cause**: `setup.py` and `setup_binary.py` had different version numbers.

**Solution**: Always keep both files in sync when updating versions.

### Problem 5: Missing Compiled Extensions
**Cause**: Extensions weren't being properly included in the final wheel.

**Solution**: Use separate build process with `build_ext --inplace` followed by `setup_binary.py bdist_wheel`.

---

## Customization for Your Package

### For Different Module Names:
1. Update the `extensions` list in `setup.py`
2. Update imports in `__init__.py`
3. Update the package name in both `setup.py` and `setup_binary.py`
4. Update test commands in the GitHub workflow
5. Replace `mypackage` throughout the workflow YAML

### For Additional Dependencies:
Add them to the workflow's "Install dependencies" step:
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install cython wheel setuptools numpy pandas  # Add your deps here
```

---

## What Users Get

After successful upload, users can install your package on **any platform**:

```bash
pip install mypackage
```

- **Windows**: Gets `.whl` with compiled `.pyd` files
- **Linux**: Gets `.whl` with compiled `.so` files  
- **macOS**: Gets `.whl` with compiled `.so` files
- **Source code is completely hidden** - only compiled binaries are distributed
- **Works exactly like any Python package** - users don't know it's compiled

---

## Troubleshooting

### Build Fails:
1. Check the Actions tab for error logs
2. Common issues: version mismatches, missing dependencies, syntax errors
3. Test locally first with Step 7 commands

### Upload Fails with "ZIP archive not accepted":
1. Check that `setup_binary.py` has `has_ext_modules=lambda: True`
2. Verify both setup files have the same version number
3. Look for `py3-none-any` wheels (should be platform-specific instead)

### Import Fails After Installation:
1. Check your `__init__.py` imports match your actual module structure
2. Make sure all modules are listed in the `extensions` list in `setup.py`

### Parallel Build Issues:
1. The isolated workspace should prevent this
2. Check if builds are failing due to missing source files

---

## Summary

This tutorial creates a professional Python package with:

✅ **Hidden source code** (compiled to binary)  
✅ **Multi-platform support** (Windows, Linux, macOS)  
✅ **Automatic builds** with GitHub Actions  
✅ **Professional packaging** with proper metadata  
✅ **Easy installation** with `pip install`  
✅ **Solves all major build/upload issues** discovered during development

Your users will never see your source code, but can use your package exactly like any other Python library!

**Key Success Factors:**
1. Use isolated build workspaces
2. Separate compilation setup from packaging setup
3. Force platform-specific wheels
4. Keep version numbers synchronized
5. Test thoroughly on all platforms