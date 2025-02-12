from functools import lru_cache
from io import BytesIO
from urllib.request import urlopen

from config import QR_BACKGROUND_KIND, QR_BACKGROUND_URL
from pydantic import AnyUrl
from segno import make


@lru_cache(None)
def generate(qr_url: AnyUrl) -> tuple[bytes, str]:
    """Возвращает кортеж: bytes картинки qr кода и ее mime тип"""

    out = BytesIO()

    make(qr_url, error="h").to_artistic(  # type: ignore
        background=urlopen(QR_BACKGROUND_URL.unicode_string()),
        target=out,
        scale=5,
        kind=QR_BACKGROUND_KIND,
    )
    return (out.getvalue(), QR_BACKGROUND_KIND)
