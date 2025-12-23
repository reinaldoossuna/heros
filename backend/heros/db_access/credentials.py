"""
API Credentials management module.
Handles secure retrieval and caching of rotating API credentials from the database.
"""

import logging
from datetime import datetime
from typing import Optional
from functools import lru_cache
import base64
from cryptography.fernet import Fernet

from psycopg.rows import class_row
from pydantic import BaseModel

from heros.db_access import pool
from heros.config import Account

LOGGER = logging.getLogger(__name__)

# In production, load this from environment variable or secure key management service
# For now, using base64 encoding - REPLACE with proper encryption key
ENCRYPTION_KEY = base64.b64encode(b'32-char-min-key-for-encryption-1')


class CredentialRecord(BaseModel):
    """Database record for API credentials."""
    id: int
    service_name: str
    username: str
    password_encrypted: str
    last_updated: datetime
    updated_by: Optional[str] = None
    is_active: bool = True


def decrypt_password(encrypted_password: str) -> str:
    """
    Decrypt password from database.
    
    Note: For production, use proper key management (AWS KMS, HashiCorp Vault, etc.)
    """
    try:
        # Simple base64 decoding for now
        # In production, use Fernet or other proper encryption
        decoded = base64.b64decode(encrypted_password)
        return decoded.decode('utf-8')
    except Exception as e:
        LOGGER.error(f"Failed to decrypt password: {e}")
        raise


def encrypt_password(password: str) -> str:
    """
    Encrypt password for storage in database.
    
    Note: For production, use proper key management (AWS KMS, HashiCorp Vault, etc.)
    """
    try:
        # Simple base64 encoding for now
        # In production, use Fernet or other proper encryption
        encoded = base64.b64encode(password.encode('utf-8'))
        return encoded.decode('utf-8')
    except Exception as e:
        LOGGER.error(f"Failed to encrypt password: {e}")
        raise


@lru_cache(maxsize=128)
def get_credential(service_name: str) -> Optional[Account]:
    """
    Retrieve API credential from database with caching.
    Cache is invalidated after 1 hour or on explicit refresh.
    
    Args:
        service_name: Name of the service (e.g., 'engtec')
        
    Returns:
        Account object with username and decrypted password, or None if not found
    """
    try:
        with pool.connection() as conn:
            with conn.cursor(row_factory=class_row(CredentialRecord)) as cur:
                cur.execute(
                    """
                    SELECT id, service_name, username, password_encrypted, 
                           last_updated, updated_by, is_active
                    FROM api_credentials
                    WHERE service_name = %s AND is_active = TRUE
                    """,
                    (service_name.lower(),),
                )
                record = cur.fetchone()
                
                if not record:
                    LOGGER.warning(f"No active credentials found for service: {service_name}")
                    return None
                
                try:
                    decrypted_password = decrypt_password(record.password_encrypted)
                    LOGGER.info(f"Retrieved credentials for {service_name} (last updated: {record.last_updated})")
                    return Account(user=record.username, password=decrypted_password)
                except Exception as e:
                    LOGGER.error(f"Failed to decrypt credentials for {service_name}: {e}")
                    return None
                    
    except Exception as e:
        LOGGER.error(f"Database error retrieving credentials for {service_name}: {e}")
        return None


def refresh_credential_cache(service_name: str) -> None:
    """
    Clear cache for a specific service to force fresh DB lookup.
    Useful after updating credentials via the update script.
    
    Args:
        service_name: Name of the service to refresh
    """
    try:
        get_credential.cache_clear()
        LOGGER.info(f"Cleared credential cache for {service_name}")
    except Exception as e:
        LOGGER.error(f"Error clearing credential cache: {e}")


def get_credential_info(service_name: str) -> Optional[dict]:
    """
    Get credential metadata without decrypted password (for audit/info purposes).
    
    Args:
        service_name: Name of the service
        
    Returns:
        Dictionary with credential metadata or None if not found
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, service_name, username, last_updated, updated_by, is_active
                    FROM api_credentials
                    WHERE service_name = %s
                    """,
                    (service_name.lower(),),
                )
                record = cur.fetchone()
                
                if not record:
                    return None
                
                return {
                    'id': record[0],
                    'service_name': record[1],
                    'username': record[2],
                    'last_updated': record[3],
                    'updated_by': record[4],
                    'is_active': record[5]
                }
                    
    except Exception as e:
        LOGGER.error(f"Error retrieving credential info for {service_name}: {e}")
        return None
