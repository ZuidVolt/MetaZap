import pytest
from pathlib import Path
from PIL import Image
import piexif  # type: ignore
from metazap import (
    clean_metadata,
    process_image,
    remove_fields_from_file,
    replace_fields_in_file,
    remove_and_replace_fields_in_file,
    process_directory,
    remove_fields_from_dir,
    replace_fields_in_dir,
    remove_and_replace_fields_in_dir,
)

# Test data
TEST_IMAGE = "test_image.jpg"
TEST_OUTPUT = "test_output.jpg"
TEST_DIR = "test_input_dir"
TEST_OUTPUT_DIR = "test_output_dir"


@pytest.fixture
def setup_test_image():
    # Create a test image with metadata
    img = Image.new("RGB", (100, 100), color="red")
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}}
    exif_dict["0th"][piexif.ImageIFD.Artist] = "Test Artist".encode()  # noqa: UP012
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = "2023:01:01 00:00:00".encode()  # noqa: UP012
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = ((10, 1), (20, 1), (30, 1))
    exif_bytes = piexif.dump(exif_dict)
    img.save(TEST_IMAGE, exif=exif_bytes)
    yield
    # Cleanup
    Path(TEST_IMAGE).unlink(missing_ok=True)
    Path(TEST_OUTPUT).unlink(missing_ok=True)


@pytest.fixture
def setup_test_directory(setup_test_image):  # noqa: ARG001
    # Create a test directory with images
    Path(TEST_DIR).mkdir(exist_ok=True)
    Path(TEST_IMAGE).rename(Path(TEST_DIR) / TEST_IMAGE)
    yield
    # Cleanup
    for file in Path(TEST_DIR).glob("*"):
        file.unlink()
    Path(TEST_DIR).rmdir()
    for file in Path(TEST_OUTPUT_DIR).glob("*"):
        file.unlink()
    Path(TEST_OUTPUT_DIR).rmdir()


def test_clean_metadata(setup_test_image):  # noqa: ARG001
    with Image.open(TEST_IMAGE) as img:
        cleaned_exif = clean_metadata(img, ["Artist"], {"Copyright": "New Copyright"})
    assert piexif.ImageIFD.Artist not in cleaned_exif["0th"]
    assert piexif.ImageIFD.Copyright in cleaned_exif["0th"]


def test_process_image(setup_test_image):  # noqa: ARG001
    process_image(Path(TEST_IMAGE), Path(TEST_OUTPUT), ["Artist"], {"Copyright": "New Copyright"})
    assert Path(TEST_OUTPUT).exists()


def test_remove_fields_from_file(setup_test_image):  # noqa: ARG001
    remove_fields_from_file(TEST_IMAGE, ["Artist"], TEST_OUTPUT)
    with Image.open(TEST_OUTPUT) as img:
        exif_dict = piexif.load(img.info["exif"])
        assert piexif.ImageIFD.Artist not in exif_dict["0th"]


def test_replace_fields_in_file(setup_test_image):  # noqa: ARG001
    replace_fields_in_file(TEST_IMAGE, {"Copyright": "New Copyright"}, TEST_OUTPUT)
    with Image.open(TEST_OUTPUT) as img:
        exif_dict = piexif.load(img.info["exif"])
        assert exif_dict["0th"][piexif.ImageIFD.Copyright] == b"New Copyright"


def test_remove_and_replace_fields_in_file(setup_test_image):  # noqa: ARG001
    remove_and_replace_fields_in_file(TEST_IMAGE, ["Artist"], {"Copyright": "New Copyright"}, TEST_OUTPUT)
    with Image.open(TEST_OUTPUT) as img:
        exif_dict = piexif.load(img.info["exif"])
        assert piexif.ImageIFD.Artist not in exif_dict["0th"]
        assert exif_dict["0th"][piexif.ImageIFD.Copyright] == b"New Copyright"


def test_process_directory(setup_test_directory):  # noqa: ARG001
    process_directory(TEST_DIR, TEST_OUTPUT_DIR, ["Artist"], {"Copyright": "New Copyright"})
    assert Path(TEST_OUTPUT_DIR).exists()
    assert len(list(Path(TEST_OUTPUT_DIR).glob("*"))) == 1


def test_remove_fields_from_dir(setup_test_directory):  # noqa: ARG001
    remove_fields_from_dir(TEST_DIR, ["Artist"], TEST_OUTPUT_DIR)
    for file in Path(TEST_OUTPUT_DIR).glob("*"):
        with Image.open(file) as img:
            exif_dict = piexif.load(img.info["exif"])
            assert piexif.ImageIFD.Artist not in exif_dict["0th"]


def test_replace_fields_in_dir(setup_test_directory):  # noqa: ARG001
    replace_fields_in_dir(TEST_DIR, {"Copyright": "New Copyright"}, TEST_OUTPUT_DIR)
    for file in Path(TEST_OUTPUT_DIR).glob("*"):
        with Image.open(file) as img:
            exif_dict = piexif.load(img.info["exif"])
            assert exif_dict["0th"][piexif.ImageIFD.Copyright] == b"New Copyright"


def test_remove_and_replace_fields_in_dir(setup_test_directory):  # noqa: ARG001
    remove_and_replace_fields_in_dir(TEST_DIR, ["Artist"], {"Copyright": "New Copyright"}, TEST_OUTPUT_DIR)
    for file in Path(TEST_OUTPUT_DIR).glob("*"):
        with Image.open(file) as img:
            exif_dict = piexif.load(img.info["exif"])
            assert piexif.ImageIFD.Artist not in exif_dict["0th"]
            assert exif_dict["0th"][piexif.ImageIFD.Copyright] == b"New Copyright"
