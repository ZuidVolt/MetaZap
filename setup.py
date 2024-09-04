from setuptools import setup, find_packages  # type: ignore

with open("README.md", "r") as f:  # noqa
    long_description = f.read()

setup(
    name="metazap",
    version="0.3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pillow-avif-plugin", "pillow", "piexif", "pathlib", "typing"],
    author="zuidvolt",
    description="A library for manipulating metadata in image files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZuidVolt/MetaZap",
    project_urls={
        "Issue Tracker": "https://github.com/ZuidVolt/MetaZap/issues",
        "Source Code": "https://github.com/ZuidVolt/MetaZap",
        "Documentation": "https://github.com/ZuidVolt/MetaZap#readme",
        "changelog": "https://github.com/ZuidVolt/MetaZap/releases",
    },
    license="Apache Software License",
    keywords="metadata exif image processing",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={"": ["*.txt", "*.md", "py.typed"]},  # Include README, other text files, and py.typed
    include_package_data=True,
    zip_safe=False,  # Required for mypy to work
    test_suite="tests",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "metazap=metazap.cli:main",
        ],
    },
)
