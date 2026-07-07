import pdfplumber
import pytesseract

from pdf2image import convert_from_path

from models.document import Document

import config


class DocumentEngine:

    def process(self, file_path):

        # --------------------
        # Configure Tesseract
        # --------------------

        pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH

        raw_text = ""

        pages = []

        page_count = 0

        source = "PDF_TEXT"

        confidence = 1.0

        # --------------------
        # Try extracting text
        # --------------------

        with pdfplumber.open(file_path) as pdf:

            page_count = len(pdf.pages)

            for page in pdf.pages:

                text = page.extract_text()

                if text:

                    pages.append(text)

                    raw_text += text + "\n"

        # --------------------
        # OCR Fallback
        # --------------------

        if raw_text.strip() == "":

            print("\nNo embedded text detected.")
            print("Running OCR...\n")

            source = "OCR"

            confidence = 0.85

            images = convert_from_path(
                file_path,
                poppler_path=config.POPPLER_PATH
            )

            pages = []

            raw_text = ""

            for image in images:

                text = pytesseract.image_to_string(image)

                pages.append(text)

                raw_text += text + "\n"

        document = Document(

            file_name=file_path,

            raw_text=raw_text,

            page_count=page_count,

            source=source,

            confidence=confidence,

            pages=pages

        )

        return document