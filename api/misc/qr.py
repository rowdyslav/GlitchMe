from functools import lru_cache
from io import BytesIO
from urllib.request import urlopen

from config import QR_BACKGROUND_URL
from pydantic import AnyUrl
from segno import make


@lru_cache(None)
def generate(qr_url: AnyUrl) -> tuple[bytes, str]:
    """Возвращает кортеж: bytes картинки qr кода и ее mime тип"""

    out = BytesIO()
    url = QR_BACKGROUND_URL.unicode_string()
    img_kind = url.split(".")[-1]

    make(qr_url, error="h").to_artistic(  # type: ignore
        background=urlopen(url),
        target=out,
        scale=5,
        kind=img_kind,
    )
    return (out.getvalue(), img_kind)
