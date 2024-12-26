from io import BytesIO

from pytest import raises
from zstandard import MAGIC_NUMBER, decompress

from scrapy_zstd.postprocessing import ZstdPlugin


def test_compress_zstd() -> None:
    output_file = BytesIO()

    plugin = ZstdPlugin(output_file, {})
    plugin.write(b"hello")
    plugin.close()

    compressed_data = output_file.getvalue()
    assert int.from_bytes(compressed_data[:4], "little") == MAGIC_NUMBER
    assert decompress(compressed_data, 1024) == b"hello"


def test_compress_zstd_with_invalid_level() -> None:
    output_file = BytesIO()

    # level is larger than 22
    with raises(ValueError):
        ZstdPlugin(output_file, {"zstd_compresslevel": 23})

    # level is not an integer
    with raises(ValueError):
        ZstdPlugin(output_file, {"zstd_compresslevel": "3"})
