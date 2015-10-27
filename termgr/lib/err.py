"""Library for terminal configuration errors"""

__all__ = ['KeyExists', 'KeygenError', 'UnconfiguredError']


class KeyExists(Exception):
    """Indicates that a key already exists"""
    pass


class KeygenError(Exception):
    """Indicates error in key generation"""
    pass


class UnconfiguredError(Exception):
    """Indicates error in key generation"""
    pass
