import logging
from pathlib import Path
from typing import Any, List, Union, Dict
from PIL import Image
import pillow_avif  # noqa: F401 RUF100 # type: ignore # Imported for its side effects
import piexif  # type: ignore

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".heif", ".avif", ".jxl")


def clean_metadata(  # noqa: C901
    image: Image.Image, fields_to_remove: List[str], fields_to_replace: Dict[str, str]
) -> Dict[str, Any]:
    """
    Clean metadata from the image, removing specified fields and adding replacement fields.
    """
    exif_dict: Dict[str, Union[dict, None]] = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    if "exif" in image.info:
        try:  # noqa: SIM105
            exif_dict = piexif.load(image.info["exif"])
        except (piexif.InvalidImageDataError, ValueError):
            pass

    for ifd in ("0th", "Exif", "GPS", "1st"):
        if ifd in exif_dict:
            for field in fields_to_remove:
                field_id = None
                if hasattr(piexif.ExifIFD, field):
                    field_id = getattr(piexif.ExifIFD, field)
                elif hasattr(piexif.ImageIFD, field):
                    field_id = getattr(piexif.ImageIFD, field)
                elif hasattr(piexif.GPSIFD, field):
                    field_id = getattr(piexif.GPSIFD, field)

                if field_id is not None:
                    exif_dict[ifd].pop(field_id, None)  # type: ignore

    # Add replacement fields
    for key, value in fields_to_replace.items():
        if hasattr(piexif.ExifIFD, key):
            exif_dict["Exif"][getattr(piexif.ExifIFD, key)] = value.encode()  # type: ignore
        elif hasattr(piexif.ImageIFD, key):
            exif_dict["0th"][getattr(piexif.ImageIFD, key)] = value.encode()  # type: ignore

    return exif_dict


def process_image(
    input_path: Path, output_path: Path, fields_to_remove: List[str], fields_to_replace: Dict[str, str]
) -> None:
    """
    Process an image by cleaning its metadata and saving it.
    """
    try:
        with Image.open(input_path) as img:
            cleaned_exif = clean_metadata(img, fields_to_remove, fields_to_replace)
            exif_bytes = piexif.dump(cleaned_exif)
            icc_profile = img.info.get("icc_profile")

            if img.format == "AVIF":
                img.save(output_path, exif=exif_bytes, icc_profile=icc_profile, quality="pillow")
            else:
                img.save(output_path, exif=exif_bytes, format=img.format, icc_profile=icc_profile)

        logging.info(f"Successfully processed image: {input_path}")
    except Exception as e:
        logging.error(f"Failed to process image {input_path}: {e}")


def remove_fields_from_file(
    input_file: Union[str, Path], fields_to_remove: List[str], output_file: Union[str, Path]
) -> None:
    """
    Remove specified fields from a single image file.

    Args:
        input_file: The path to the input image file.
        fields_to_remove: A list of field names to remove from the image metadata.
        output_file: The path to the output image file.

    Returns:
        None
    """
    input_path = Path(input_file)
    output_path = Path(output_file)
    process_image(input_path, output_path, fields_to_remove, {})


def replace_fields_in_file(
    input_file: Union[str, Path], fields_to_replace: Dict[str, str], output_file: Union[str, Path]
) -> None:
    """
    Replace specified fields in a single image file.

    Args:
        input_file: The path to the input image file.
        fields_to_replace: A dictionary of field names to replace and their corresponding values.
        output_file: The path to the output image file.

    Returns:
        None
    """
    input_path = Path(input_file)
    output_path = Path(output_file)
    process_image(input_path, output_path, [], fields_to_replace)


def remove_and_replace_fields_in_file(
    input_file: Union[str, Path],
    fields_to_remove: List[str],
    fields_to_replace: Dict[str, str],
    output_file: Union[str, Path],
) -> None:
    """
    Remove and replace specified fields in a single image file.

    Args:
        input_file: The path to the input image file.
        fields_to_remove: A list of field names to remove from the image metadata.
        fields_to_replace: A dictionary of field names to replace and their corresponding values.
        output_file: The path to the output image file.

    Returns:
        None
    """
    input_path = Path(input_file)
    output_path = Path(output_file)
    process_image(input_path, output_path, fields_to_remove, fields_to_replace)


def process_directory(
    input_dir: Union[str, Path],
    output_dir: Union[str, Path],
    fields_to_remove: List[str],
    fields_to_replace: Dict[str, str],
) -> None:
    """
    Process all supported image files in a directory.

    Args:
        input_dir: The path to the input directory.
        output_dir: The path to the output directory.
        fields_to_remove: A list of field names to remove from the image metadata.
        fields_to_replace: A dictionary of field names to replace and their corresponding values.

    Returns:
        None
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for file_path in input_path.glob("*"):
        if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            output_file = output_path / file_path.name
            process_image(file_path, output_file, fields_to_remove, fields_to_replace)


def remove_fields_from_dir(
    input_dir: Union[str, Path], fields_to_remove: List[str], output_dir: Union[str, Path]
) -> None:
    """
    Remove specified fields from all supported image files in a directory.

    Args:
        input_dir: The path to the input directory.
        fields_to_remove: A list of field names to remove from the image metadata.
        output_dir: The path to the output directory.

    Returns:
        None
    """
    process_directory(input_dir, output_dir, fields_to_remove, {})


def replace_fields_in_dir(
    input_dir: Union[str, Path], fields_to_replace: Dict[str, str], output_dir: Union[str, Path]
) -> None:
    """
    Replace specified fields in all supported image files in a directory.

    Args:
        input_dir: The path to the input directory.
        fields_to_replace: A dictionary of field names to replace and their corresponding values.
        output_dir: The path to the output directory.

    Returns:
        None
    """
    process_directory(input_dir, output_dir, [], fields_to_replace)


def remove_and_replace_fields_in_dir(
    input_dir: Union[str, Path],
    fields_to_remove: List[str],
    fields_to_replace: Dict[str, str],
    output_dir: Union[str, Path],
) -> None:
    """
    Remove and replace specified fields in all supported image files in a directory.

    Args:
        input_dir: The path to the input directory.
        fields_to_remove: A list of field names to remove from the image metadata.
        fields_to_replace: A dictionary of field names to replace and their corresponding values.
        output_dir: The path to the output directory.

    Returns:
        None
    """
    process_directory(input_dir, output_dir, fields_to_remove, fields_to_replace)
