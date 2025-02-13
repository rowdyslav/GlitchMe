from io import BytesIO
from urllib.request import urlopen

from config import QR_BACKGROUND_URL
from pydantic import AnyUrl
from segno import make


def generate_qr(qr_url: AnyUrl) -> tuple[bytes, str]:
    """Возвращает кортеж: bytes qr-кода и ее mime тип"""

    out = BytesIO()
    url = QR_BACKGROUND_URL.unicode_string()
    img_kind = url.split(".")[-1]

    qr = make(qr_url.unicode_string(), error="h")
    qr.to_artistic(  # type: ignore
        background=urlopen(url),
        target=out,
        scale=5,
        kind=img_kind,
    )
    return (out.getvalue(), img_kind)
