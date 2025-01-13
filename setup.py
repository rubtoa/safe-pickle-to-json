from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="safe-pickle-to-json",
    version="0.1.0",
    author="Ronen Atias",
    author_email="ronen.atias@gmail.com",
    description="A secure utility for converting pickle files to JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rubtoa/safe-pickle-to-json",
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'p2j=src.p2j:main',
        ],
    },
) 