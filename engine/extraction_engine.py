from models.invoice import Invoice


class ExtractionEngine:

    def extract(self, raw_text: str) -> Invoice:

        """
        Extract fields from OCR text.

        Returns Invoice object.
        """

        invoice = Invoice()

        return invoice