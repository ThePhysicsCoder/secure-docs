import os
import io
from pdf2image import convert_from_path
from django.core.files.base import ContentFile
from PIL import Image


def generate_thumbnail(document):
    """
    Generates thumbnail for uploaded document.
    - Images → use same image
    - PDFs → convert first page to image
    """

    file_path = document.file.path
    extension = os.path.splitext(file_path)[1].lower()

    # 🖼 IMAGE FILES (CREATE REAL THUMBNAIL)
    if extension in ['.jpg', '.jpeg', '.png']:
        img = Image.open(file_path)
        img.thumbnail((300, 300))

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')

        thumb_name = os.path.basename(file_path)

        document.thumbnail.save(
            thumb_name,
            ContentFile(buffer.getvalue()),
            save=True
        )
        return

    # 📄 PDF FILES
    if extension == '.pdf':
        pages = convert_from_path(
            file_path,
            first_page=1,
            last_page=1
        )

        first_page = pages[0]

        # Resize to thumbnail size
        first_page.thumbnail((300, 300))

        buffer = io.BytesIO()
        first_page.save(buffer, format='JPEG')

        thumb_name = os.path.basename(file_path).replace('.pdf', '.jpg')

        document.thumbnail.save(
            thumb_name,
            ContentFile(buffer.getvalue()),
            save=True
        )
