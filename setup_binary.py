from setuptools import setup, find_packages

# This is a simplified setup.py that only packages compiled files
setup(
    name="secretpackage",
    version="0.2.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="A secret package with hidden source code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/guochen2011gc/secretpackage",
    packages=find_packages(),
    package_data={
        'secretpackage': ['*.so', '*.pyd'],
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