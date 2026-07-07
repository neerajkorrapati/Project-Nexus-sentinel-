"""
===========================================================
Invoice Agent V4

Base Extractor

Every extractor inherits from this class.

Author : Project Nexus
===========================================================
"""

from abc import ABC, abstractmethod

from extractors.utils import ExtractorUtils


class BaseExtractor(ABC):

    def __init__(self):

        self.utils = ExtractorUtils()

    @abstractmethod
    def extract(self, tokens):
        """
        Every V4 extractor must strictly implement this.
        It consumes DocumentTokens instead of raw strings.
        
        Returns:
            extracted value
        """
        pass

    # ---------------------------------------------------
    # Helper Functions
    # ---------------------------------------------------

    def aliases(self, field):

        return self.utils.aliases(field)

    def contains_alias(self, line, field):

        aliases = self.aliases(field)

        return self.utils.contains_alias(line, aliases)

    def after_colon(self, line):

        return self.utils.value_after_colon(line)

    def number(self, line):

        return self.utils.extract_number(line)

    def date(self, line):

        return self.utils.extract_date(line)

    def debug(self, title, value):

        self.utils.debug(title, value)