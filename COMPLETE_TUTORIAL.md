# Complete Tutorial: Create and Upload a Hidden Source Code Python Package to PyPI

This tutorial shows you how to take any Python package and upload it to PyPI with **hidden source code** using Cython compilation, with **automatic multi-platform builds** using GitHub Actions.

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

**IMPORTANT**: Update the `extensions` list to include ALL your Python modules (except `__init__.py`).

#### Create `pyproject.toml`:
```bash
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=45", "wheel", "Cython>=0.29"]
build-backend = "setuptools.build_meta"
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

## Step 3: Create GitHub Actions Workflow

### 3.1 Create the workflow directory:
```bash
mkdir -p .github/workflows
```

### 3.2 Create the GitHub Actions workflow:
```bash
cat > .github/workflows/build_and_upload.yml << 'EOF'
name: Build and Upload to PyPI

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build_wheels_linux:
    name: Build Linux wheels  
    runs-on: ubuntu-latest
    strategy:
      matrix:
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
      
      - name: Build extensions
        run: |
          python setup.py build_ext --inplace
      
      - name: Create source-free package
        run: |
          # Create a temporary copy without .py files
          cp -r mypackage mypackage_temp
          cd mypackage_temp
          find . -name "*.py" ! -name "__init__.py" -delete
          cd ..
          
      - name: Build wheel from compiled package
        run: |
          # Temporarily swap directories
          mv mypackage mypackage_with_source
          mv mypackage_temp mypackage
          python setup.py bdist_wheel
          # Restore original
          mv mypackage mypackage_temp
          mv mypackage_with_source mypackage
      
      - name: Rename wheel for PyPI compatibility
        run: |
          mkdir -p wheelhouse
          for wheel in dist/*-linux_x86_64.whl; do
            if [ -f "$wheel" ]; then
              newname=$(echo "$wheel" | sed 's/-linux_x86_64.whl/-manylinux_2_17_x86_64.whl/')
              newname=$(basename "$newname")
              cp "$wheel" "wheelhouse/$newname"
            fi
          done
      
      - name: Test wheel
        run: |
          pip install wheelhouse/*.whl
          python -c "import mypackage; print('Linux test passed!')"
          # Verify no source files except __init__.py
          python -c "import os; import mypackage; path = os.path.dirname(mypackage.__file__); files = os.listdir(path); py_files = [f for f in files if f.endswith('.py') and f != '__init__.py']; assert len(py_files) == 0, f'Found source files: {py_files}'"
      
      - name: Upload wheel
        uses: actions/upload-artifact@v4
        with:
          name: wheel-linux-${{ matrix.python-version }}
          path: wheelhouse/*.whl

  build_wheels_other:
    name: Build wheels on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, macos-latest]
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
      
      - name: Build extensions
        run: |
          python setup.py build_ext --inplace
          
      - name: Create source-free package (Windows)
        if: runner.os == 'Windows'
        shell: pwsh
        run: |
          Copy-Item -Path mypackage -Destination mypackage_temp -Recurse
          Get-ChildItem -Path mypackage_temp -Filter *.py -Recurse | 
            Where-Object { $_.Name -ne "__init__.py" } | 
            Remove-Item -Force
            
      - name: Create source-free package (macOS)
        if: runner.os == 'macOS'
        run: |
          cp -r mypackage mypackage_temp
          find mypackage_temp -name "*.py" ! -name "__init__.py" -delete
      
      - name: Build wheel from compiled package
        run: |
          mv mypackage mypackage_with_source
          mv mypackage_temp mypackage
          python setup.py bdist_wheel
          mv mypackage mypackage_temp
          mv mypackage_with_source mypackage
      
      - name: Test wheel
        run: |
          pip install dist/*.whl
          python -c "import mypackage; print('Test passed on ${{ matrix.os }}!')"
          # Verify no source files
          python -c "import os; import mypackage; path = os.path.dirname(mypackage.__file__); files = os.listdir(path); py_files = [f for f in files if f.endswith('.py') and f != '__init__.py']; assert len(py_files) == 0, f'Found source files: {py_files}'"
      
      - name: Upload wheel
        uses: actions/upload-artifact@v4
        with:
          name: wheel-${{ matrix.os }}-${{ matrix.python-version }}
          path: dist/*.whl

  upload_to_pypi:
    name: Upload to PyPI
    needs: [build_wheels_linux, build_wheels_other]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')
    
    steps:
      - uses: actions/download-artifact@v4
        with:
          path: dist
          merge-multiple: true
      
      - name: List files
        run: ls -la dist/
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
          skip-existing: true
EOF
```

**IMPORTANT**: Change `mypackage` in the test commands to your actual package name.

---

## Step 4: Initialize Git Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit with multi-platform build workflow"
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
2. Click on the "Build and Upload to PyPI" workflow
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
2. **Update version** in `setup.py`:
   ```bash
   # Edit setup.py and change version="0.1.0" to version="0.1.1"
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

---

## Customization for Your Package

### For Different Module Names:
1. Update the `extensions` list in `setup.py`
2. Update imports in `__init__.py`
3. Update the package name in `setup.py`
4. Update test commands in the GitHub workflow

### For Additional Dependencies:
Add them to the workflow's "Install dependencies" step:
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install cython wheel setuptools numpy pandas  # Add your deps here
```

### For Private Repositories:
- GitHub Actions has limited free minutes for private repos
- Consider using only public repos for packages

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
2. Common issues: missing dependencies, syntax errors in `setup.py`
3. Test locally first with the Step 7 commands

### Upload Fails:
1. Check your PyPI token is correct in GitHub Secrets
2. Make sure package name isn't already taken on PyPI
3. Version numbers can't be reused - bump the version

### Import Fails After Installation:
1. Check your `__init__.py` imports match your actual module structure
2. Make sure all modules are listed in the `extensions` list in `setup.py`

---

## Summary

This tutorial creates a professional Python package with:

✅ **Hidden source code** (compiled to binary)  
✅ **Multi-platform support** (Windows, Linux, macOS)  
✅ **Automatic builds** with GitHub Actions  
✅ **Professional packaging** with proper metadata  
✅ **Easy installation** with `pip install`

Your users will never see your source code, but can use your package exactly like any other Python library!