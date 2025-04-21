from io import BytesIO
from urllib.request import urlopen

from pydantic import AnyUrl
from segno import make

from config import QR_BACKGROUND_URL


def generate_qr(qr_url: AnyUrl) -> tuple[bytes, str]:
    """Возвращает кортеж: bytes qr-кода и его mime тип"""

    out = BytesIO()
    img_kind = QR_BACKGROUND_URL.split(".")[-1]

    qr = make(qr_url.unicode_string(), error="h")
    qr.to_artistic(  # type: ignore
        background=urlopen(QR_BACKGROUND_URL),
        target=out,
        scale=5,
        kind=img_kind,
    )
    return (out.getvalue(), img_kind)
