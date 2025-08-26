# Complete Guide: Using GitHub Actions to Build Multi-Platform Wheels

This guide shows you how to automatically build wheels for Windows, Linux, and macOS using GitHub Actions.

## Prerequisites

1. GitHub account
2. Git installed on your machine
3. Your package ready to upload

## Step-by-Step Process

### Step 1: Create a GitHub Repository

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit your code
git commit -m "Initial commit"

# Create a new repository on GitHub (via web interface)
# Then add the remote
git remote add origin https://github.com/YOUR_USERNAME/secretpackage.git

# Push your code
git push -u origin main
```

### Step 2: Add Your PyPI Token to GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI token (the same one from ~/.pypirc)
6. Click **Add secret**

### Step 3: Update Your Package for Cross-Platform

Replace your `setup.py` with the cross-platform version:

```bash
# Backup original setup.py
mv setup.py setup_original.py

# Use the cross-platform setup
cp setup_cross_platform.py setup.py
```

### Step 4: Push the GitHub Actions Workflow

```bash
# Add the workflow files
git add .github/workflows/build_wheels.yml
git add setup.py

# Commit
git commit -m "Add GitHub Actions workflow for multi-platform builds"

# Push to GitHub
git push
```

### Step 5: Create a Release to Trigger the Build

```bash
# Update version in setup.py to 0.1.1 (or next version)
# Edit setup.py and change version="0.1.1"

# Commit the version bump
git add setup.py
git commit -m "Bump version to 0.1.1"

# Create and push a tag
git tag v0.1.1
git push origin v0.1.1
```

### Step 6: Monitor the Build

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You'll see your workflow running
4. Click on it to see the progress

The workflow will:
- Build wheels for Windows (32-bit and 64-bit)
- Build wheels for Linux (x86_64, aarch64)
- Build wheels for macOS (x86_64, arm64)
- Build for Python 3.8, 3.9, 3.10, 3.11, and 3.12
- Upload everything to PyPI automatically

### Step 7: Verify the Upload

Once complete, check PyPI:
https://pypi.org/project/secretpackage/

You should see multiple wheel files like:
- `secretpackage-0.1.1-cp312-cp312-win_amd64.whl`
- `secretpackage-0.1.1-cp312-cp312-macosx_10_9_x86_64.whl`
- `secretpackage-0.1.1-cp312-cp312-linux_x86_64.whl`
- And many more...

## What Each Platform Gets

### Windows Users
```bash
pip install secretpackage
# Downloads: secretpackage-0.1.1-cp312-cp312-win_amd64.whl
```

### Linux Users
```bash
pip install secretpackage
# Downloads: secretpackage-0.1.1-cp312-cp312-linux_x86_64.whl
```

### macOS Users
```bash
pip install secretpackage
# Downloads: secretpackage-0.1.1-cp312-cp312-macosx_11_0_arm64.whl (Apple Silicon)
# or: secretpackage-0.1.1-cp312-cp312-macosx_10_9_x86_64.whl (Intel)
```

## Testing Your Multi-Platform Package

After the upload completes, test on different platforms:

```bash
# Uninstall any local version
pip uninstall -y secretpackage

# Install from PyPI
pip install secretpackage

# Test it works
python -c "import secretpackage; print(secretpackage.add(5, 3))"
```

## Troubleshooting

### Build Failed
- Check the Actions tab for error messages
- Common issues:
  - Missing dependencies in `CIBW_BEFORE_BUILD`
  - Syntax errors in setup.py
  - C compilation errors on certain platforms

### PyPI Upload Failed
- Check your `PYPI_API_TOKEN` secret is set correctly
- Ensure the version number is unique (can't overwrite existing versions)

### Platform-Specific Issues
- Windows: May need Visual C++ compiler
- Linux: Different versions (manylinux) for compatibility
- macOS: Universal builds for Intel and Apple Silicon

## Advanced Configuration

### Building for Specific Platforms Only

In `.github/workflows/build_wheels.yml`, modify the matrix:

```yaml
matrix:
  os: [ubuntu-latest, macos-latest]  # Skip Windows
```

### Building for Specific Python Versions

Modify `CIBW_BUILD`:
```yaml
CIBW_BUILD: cp310-* cp311-* cp312-*  # Only Python 3.10+
```

### Adding Binary Dependencies

If your package needs libraries like numpy:
```yaml
CIBW_BEFORE_BUILD: pip install cython numpy
```

## Next Steps

1. Every time you want to release a new version:
   - Update version in setup.py
   - Commit and push
   - Create a new tag: `git tag v0.1.2 && git push origin v0.1.2`
   - GitHub Actions automatically builds and uploads

2. Monitor your package:
   - Check download stats on PyPI
   - Watch for issues reported by users
   - Keep dependencies updated

## Benefits of This Approach

✅ **Fully Automated**: Push a tag, get wheels for all platforms
✅ **No Local Builds**: Don't need Windows/Linux machines
✅ **Consistent**: Same build environment every time
✅ **Free**: GitHub Actions is free for public repositories
✅ **Professional**: Same process used by NumPy, Pandas, etc.

Your users can now simply run `pip install secretpackage` on any platform and it will work!