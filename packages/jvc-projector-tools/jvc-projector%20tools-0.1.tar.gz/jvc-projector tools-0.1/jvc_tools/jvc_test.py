#!/usr/bin/env python3

"""JVC projector low level command module"""

import enum

class Error(Exception):
    """JVC protocol error"""
    pass

class CommandNack(Exception):
    """JVC command not acknowledged"""
    pass

class Header(enum.Enum):
    """JVC command and response headers"""
    operation = b'!'
    reference = b'?'
    response = b'@'
    ack = b'\x06'