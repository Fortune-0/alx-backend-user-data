#!/usr/bin/env python3
"""Filter datum function"""
import logging
import re
from typing import List, Sequence


def filter_datum(fields: list[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ Function that returns the log message obfuscated"""
    pattern = '|'.join(f'(?<={field}=)[^{separator}]+' for field in fields)
    return re.sub(pattern, redaction, message)
