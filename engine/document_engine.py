import pdfplumber

from models.document import Document


class DocumentEngine:

    def process(self, file_path: str):

        raw_text = ""

        pages = []

        page_count = 0

        with pdfplumber.open(file_path) as pdf:

            page_count = len(pdf.pages)

            for page in pdf.pages:

                text = page.extract_text()

                if text is None:
                    text = ""

                pages.append(text)

                raw_text += text + "\n"

        document = Document(

            file_name=file_path,

            raw_text=raw_text,

            page_count=page_count,

            source="PDF_TEXT",

            confidence=1.0,

            pages=pages

        )

        return document