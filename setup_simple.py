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