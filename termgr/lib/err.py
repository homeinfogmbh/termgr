"""Library for terminal configuration errors"""

__all__ = ['KeyExist', 'KeygenError', 'UnconfiguredError']


class KeyExist(Exception):
    """Indicates that a key already exists"""
    pass


class KeygenError(Exception):
    """Indicates error in key generation"""
    pass


class UnconfiguredError(Exception):
    """Indicates error in key generation"""
    pass
