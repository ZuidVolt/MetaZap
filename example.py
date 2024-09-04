import metazap as mz

INPUT_DIR = "images"
OUTPUT_DIR = "cleaned_images"


# List of only the most highly sensitive fields to remove
SANITIES_FIELDS = [
    "GPSInfo",
    "SerialNumber",
    "CameraSerialNumber",
    "LensSerialNumber",
    "BodySerialNumber",
    "ImageDescription",
    "CameraOwnerName",
    "FlashPixVersion",
    "CameraOwnerAddress",
]

DATE_YEAR = "2024:01:01 00:00:00"

# Default settings for metadata fields
DEFAULT_SETTINGS = {
    "Artist": "me",
    "Creator": "me",
    "Copyright": "All Rights Reserved",
    "License": "CC BY-NC-ND 4.0",
    "DateTime": DATE_YEAR,
    "DateTimeOriginal": DATE_YEAR,
    "DateTimeDigitized": DATE_YEAR,
}


def main():
    # Remove and replace sensitive fields in the input directory
    mz.remove_and_replace_fields_in_dir(INPUT_DIR, SANITIES_FIELDS, DEFAULT_SETTINGS, OUTPUT_DIR)


if __name__ == "__main__":
    main()
