""" Convert card images for The Game Crafter

  * Add black margin around the card

"""
import argparse
import os

from pathlib import Path
from PIL import Image

from tgc_utils.utils import list_files_at_path

TGC_CARD_SPECS = {
    "euro_card": {
        "margin": 55,
        "size": (825, 1125),
    }
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="A folder with input images and nothing else.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="A folder to write the output images. Output files retain names at input.",
        required=True,
    )
    args = parser.parse_args()
    return args


def create_overlay_img(conf):
    """Create black base image

    :param conf: dict with 'size' key

    :return: PIL Image
    """
    img = Image.new("RGB", conf["size"], color="black")
    return img


def convert_card_img(img, overlay_img, conf):
    """Convert an image file to format that The Game Crafter can print"""
    w, h = conf["size"]
    margin = conf["margin"]
    new_w = w - 2 * margin
    new_h = h - 2 * margin
    img = img.resize((new_w, new_h), Image.ANTIALIAS)
    card_img = overlay_img.copy()
    card_img.paste(img, (margin, margin), img.convert("RGBA"))
    return card_img


def convert_card_images(input_path, output_path, config):
    """Write and convert images at input path

    :return: None, writes directly to output_path
    """
    input_files = list_files_at_path(input_path)
    overlay_img = create_overlay_img(config)
    Path(output_path).mkdir(parents=True, exist_ok=True)

    for input_file in input_files:
        input_img = Image.open(input_file)
        card_img = convert_card_img(input_img, overlay_img, config)
        output_file = os.path.join(output_path, os.path.basename(input_file))
        card_img.save(output_file, "PNG")


def main():
    args = parse_args()
    config = TGC_CARD_SPECS["euro_card"]
    convert_card_images(args.input, args.output, config)
    return 0


if __name__ == "__main__":
    main()
