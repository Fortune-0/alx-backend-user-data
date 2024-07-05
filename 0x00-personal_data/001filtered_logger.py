#!/usr/bin/env python3
"""Filter datum function"""
import logging
import re
from typing import List, Sequence


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replaces sensitive information in a message with a redacted value
    based on the list of fields to redact
    """
    pattern = '|'.join(f'(?<={field}=)[^{separator}]+' for field in fields)
    return re.sub(pattern, redaction, message)
