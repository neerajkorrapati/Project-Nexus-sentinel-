"""
===========================================================

Invoice Agent V3.5

Document Token

Represents one structured piece of information
extracted from the OCR/document parser.

===========================================================
"""


class DocumentToken:

    def __init__(

        self,

        label="",

        value="",

        line_number=-1,

        confidence=1.0

    ):

        self.label = label

        self.value = value

        self.line_number = line_number

        self.confidence = confidence

    def to_dict(self):

        return {

            "label": self.label,

            "value": self.value,

            "line_number": self.line_number,

            "confidence": self.confidence

        }

    def __repr__(self):

        return (

            f"DocumentToken("

            f"label='{self.label}', "

            f"value='{self.value}', "

            f"line={self.line_number}, "

            f"confidence={self.confidence}"

            f")"

        )   