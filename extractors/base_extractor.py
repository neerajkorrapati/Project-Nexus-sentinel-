"""
===========================================================
Project Nexus — Base Extractor Interface
===========================================================
"""


class BaseExtractor:

    def __init__(self):
        pass

    def debug(self, msg: str, value=None):
        if value is not None:
            print(f"[{self.__class__.__name__}] {msg}: {value}")
        else:
            print(f"[{self.__class__.__name__}] {msg}")

    def extract(self, tokens: list):
        raise NotImplementedError("Subclasses must implement extract()")