from typing import Any, BinaryIO, Dict

from zstandard import ZstdCompressor


class ZstdPlugin:
    def __init__(self, file: BinaryIO, feed_options: Dict[str, Any]) -> None:
        compress_level = feed_options.get("zstd_compresslevel", 3)
        if not isinstance(compress_level, int) or compress_level > 22:
            raise ValueError(
                f"Invalid zstd_compresslevel: {compress_level} (must be an integer less than or equal to 22)"
            )
        self.writer = ZstdCompressor(level=compress_level).stream_writer(
            file, closefd=False
        )

    def write(self, data: bytes) -> int:
        return self.writer.write(data)

    def close(self) -> None:
        self.writer.close()
