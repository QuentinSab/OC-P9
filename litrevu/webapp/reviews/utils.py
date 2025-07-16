from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def resize_image(image_file, max_width=256, max_height=256):
    img = Image.open(image_file)
    img.thumbnail((max_width, max_height), Image.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    return InMemoryUploadedFile(
        buffer,
        field_name='ImageField',
        name=image_file.name,
        content_type='image/jpeg',
        size=sys.getsizeof(buffer),
        charset=None
    )
