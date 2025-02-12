from io import BytesIO
from typing import Union

from PIL import Image as ImageModule
from PIL import ImageDraw
from PIL.Image import Image
from qrcode_styled import QRCodeStyled


async def gen(link: str) -> bytes:
    image_padding: int = 10
    image_round: int = 50
    padded_image = process_optional_image(BytesIO(...), image_padding, image_round)

    qr = QRCodeStyled(border=1, box_size=60)
    qrcode_image = await qr.get_buffer_async(data=link, image=padded_image)
    qrcode_image_data = qrcode_image.getvalue()
    return qrcode_image_data


def process_optional_image(
    image_stream: BytesIO, image_padding: int = 10, image_round: int = 50
):
    """
    Processes an optional image to be included in the QR code.

    :param image_stream: BytesIO object containing the image data
    :param image_padding: Padding around the optional image in the QR code (optional)
    :param image_round: Radius for rounding corners of the optional image in the QR code (optional)
    :return: Processed Image object
    """
    if image_stream:
        logo_image = ImageModule.open(image_stream).convert("RGBA")

        # If the image has an alpha channel (transparency), replace transparent areas with white
        if logo_image.mode == "RGBA":
            alpha = logo_image.split()[3]
            white_background = ImageModule.new(
                "RGBA", logo_image.size, (255, 255, 255, 255)
            )
            white_background.paste(logo_image, (0, 0), alpha)
            logo_image = white_background

        # Create a rounded rectangle mask for the logo image
        mask = ImageModule.new("L", logo_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            (0, 0, logo_image.width, logo_image.height), image_round, fill=255
        )

        # Apply the mask to the logo image
        logo_image.putalpha(mask)
        logo_image = Image.alpha_composite(
            ImageModule.new("RGBA", logo_image.size, (255, 255, 255, 255)), logo_image
        )

        # Add padding to the logo image
        padded_size = (
            logo_image.width + 2 * image_padding,
            logo_image.height + 2 * image_padding,
        )
        padded_image = ImageModule.new("RGBA", padded_size, (255, 255, 255, 255))
        padded_image.paste(logo_image, (image_padding, image_padding))

        return padded_image

    return None
