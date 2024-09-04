
# metazap

A Python library for removing and replacing metadata from image files.

## Table of Contents

1. [Installation](#installation)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Usage](#usage)
5. [API Documentation](#api-documentation)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)
8. [Attribution](#attribution)
9. [License](#license)

## Installation

Install the library using pip:

```bash
pip install metazap
```

## Features

- Remove specified metadata fields from image files
- Replace specified metadata fields with new values
- Process individual image files or entire directories
- Supports JPEG, PNG, HEIF, AVIF, and JXL image formats

## Requirements

- Python 3.x
- Pillow (PIL) library with metadata support
- piexif library for EXIF metadata support
- pillow-avif library for AVIF image support

## Usage

The library provides several functions for removing and replacing metadata from image files:

1. `remove_fields_from_file`: Remove specified metadata fields from an image file.
2. `replace_fields_in_file`: Replace specified metadata fields in an image file.
3. `remove_fields_from_dir`: Remove specified metadata fields from all image files in a directory.
4. `replace_fields_in_dir`: Replace specified metadata fields in all image files in a directory.
5. `process_image`: Process an individual image file.
6. `process_directory`: Process all image files in a directory.

### Example Usage

```python
from metazap import remove_fields_from_file, replace_fields_in_file

# Remove metadata fields from an image file
remove_fields_from_file("input.jpg", ["Artist", "Copyright"], "output.jpg")

# Replace metadata fields in an image file
replace_fields_in_file("input.jpg", {"Artist": "John Doe", "Copyright": "2022"}, "output.jpg")
```

## API Documentation

### Functions

- `remove_fields_from_file(input_file, fields_to_remove, output_file)`: Remove specified metadata fields from an image file.
- `replace_fields_in_file(input_file, fields_to_replace, output_file)`: Replace specified metadata fields in an image file.
- `remove_fields_from_dir(input_dir, fields_to_remove, output_dir)`: Remove specified metadata fields from all image files in a directory.
- `replace_fields_in_dir(input_dir, fields_to_replace, output_dir)`: Replace specified metadata fields in all image files in a directory.
- `process_image(input_path, output_path, fields_to_remove, fields_to_replace)`: Process an individual image file.
- `process_directory(input_dir, output_dir, fields_to_remove, fields_to_replace)`: Process all image files in a directory.

### Parameters

- `input_file`: The path to the input image file.
- `fields_to_remove`: A list of metadata fields to remove.
- `fields_to_replace`: A dictionary of metadata fields to replace and their corresponding values.
- `output_file`: The path to the output image file.
- `input_dir`: The path to the input directory.
- `output_dir`: The path to the output directory.

## Troubleshooting

If you encounter issues with metadata support, ensure that the required libraries are installed and up-to-date.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## Attribution

This library uses the following libraries:

- Pillow: A Python imaging library
- piexif: A Python library for reading and writing EXIF metadata
- pillow-avif: A Pillow plugin for reading and writing AVIF images

We would like to thank the authors of these libraries for their hard work and contributions to the Python community.

## License

This project is licensed under the Apache License, Version 2.0 with important additional terms, including specific commercial use conditions. Users are strongly advised to read the full [LICENSE](LICENSE) file carefully before using, modifying, or distributing this work. The additional terms contain crucial information about liability, data collection, indemnification, and commercial usage requirements that may significantly affect your rights and obligations.
