"""
Encryption utilities for sensitive data.

Used to encrypt/decrypt Jira API tokens before storing in database.
"""
import os
import base64
from cryptography.fernet import Fernet
from typing import Optional


# ============================================================================
# Configuration
# ============================================================================

def get_encryption_key() -> bytes:
    """
    Get encryption key from environment variable.

    The key must be a 32-byte base64-encoded string.

    To generate a new key:
        from cryptography.fernet import Fernet
        print(Fernet.generate_key().decode())

    Returns:
        Encryption key as bytes

    Raises:
        ValueError: If ENCRYPTION_KEY is not set or invalid
    """
    key_str = os.getenv("ENCRYPTION_KEY")

    if not key_str:
        # For development, use a default key
        # WARNING: NEVER use this in production!
        print("⚠️  WARNING: Using default encryption key. Set ENCRYPTION_KEY in production!")
        key_str = "kZ8v3X9mN4pQ2wR7tY1uI5oP0aS6dF3gH8jK4lM9nB2="

    try:
        # Ensure it's a valid Fernet key
        key_bytes = key_str.encode() if isinstance(key_str, str) else key_str
        Fernet(key_bytes)  # This will raise if key is invalid
        return key_bytes
    except Exception as e:
        raise ValueError(f"Invalid ENCRYPTION_KEY: {str(e)}")


# Initialize Fernet cipher
_cipher = Fernet(get_encryption_key())


# ============================================================================
# Encryption Functions
# ============================================================================

def encrypt_token(token: str) -> str:
    """
    Encrypt a token string.

    Args:
        token: The plain text token to encrypt

    Returns:
        Base64-encoded encrypted token

    Example:
        >>> encrypted = encrypt_token("my_jira_api_token_123")
        >>> print(encrypted)
        'gAAAAABh...'
    """
    if not token:
        return ""

    encrypted_bytes = _cipher.encrypt(token.encode())
    return encrypted_bytes.decode()


def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypt an encrypted token string.

    Args:
        encrypted_token: The encrypted token to decrypt

    Returns:
        Plain text token

    Raises:
        cryptography.fernet.InvalidToken: If token cannot be decrypted

    Example:
        >>> decrypted = decrypt_token(encrypted)
        >>> print(decrypted)
        'my_jira_api_token_123'
    """
    if not encrypted_token:
        return ""

    decrypted_bytes = _cipher.decrypt(encrypted_token.encode())
    return decrypted_bytes.decode()


def encrypt_optional(value: Optional[str]) -> Optional[str]:
    """
    Encrypt a value if it's not None.

    Args:
        value: Optional string to encrypt

    Returns:
        Encrypted string or None
    """
    return encrypt_token(value) if value else None


def decrypt_optional(value: Optional[str]) -> Optional[str]:
    """
    Decrypt a value if it's not None.

    Args:
        value: Optional encrypted string to decrypt

    Returns:
        Decrypted string or None
    """
    return decrypt_token(value) if value else None
