from Markdown2docx import Markdown2docx
from io import BytesIO
import tempfile
import os
import logging

def convert_md_to_docx(md_content: str) -> BytesIO:
    md_path = None
    docx_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as md_file:
            md_file.write(md_content)
            md_path = md_file.name

        docx_path = md_path.replace('.md', '.docx')

        project = Markdown2docx(md_path[:-3])  # Инициализируем без расширения md!
        project.eat_soup()
        project.save()

        if not os.path.isfile(docx_path) or os.path.getsize(docx_path) == 0:
            raise ValueError("Generated DOCX file is empty")

        with open(docx_path, 'rb') as f:
            docx_bytes = f.read()
        docx_buffer = BytesIO(docx_bytes)
        docx_buffer.seek(0)

        return docx_buffer

    except Exception as e:
        logging.error(f"DOCX conversion error: {e}")
        raise
    finally:
        if md_path and os.path.exists(md_path):
            os.unlink(md_path)
        if docx_path and os.path.exists(docx_path):
            os.unlink(docx_path)
