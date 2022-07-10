import hashlib
import pytest
from PIL import Image
from tgc_utils.convert_card_images import convert_card_img
from tgc_utils.convert_card_images import create_overlay_img


@pytest.fixture
def config():
    config = {
        "margin": 55,
        "size": (825, 1125),
    }
    return config


@pytest.fixture
def overlay_img(config):
    return create_overlay_img(config)


@pytest.fixture
def img(config):
    img = Image.new("RGB", config["size"], color="white")
    return img


def test_convert_card_img(img, overlay_img, config):
    converted_img = convert_card_img(img, overlay_img, config)
    img_bytes = converted_img.tobytes()
    m = hashlib.md5()
    m.update(img_bytes)
    img_hash = m.hexdigest()
    assert img_hash == "38a8e7f55a5668accef2517ca9a2e50e"
