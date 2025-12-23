"""
API endpoints for managing rotating API credentials.
Allows authorized users to update service credentials without restarting the server.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from fastapi import APIRouter, HTTPException, status

from heros.db_access import pool
from heros.db_access.credentials import encrypt_password, refresh_credential_cache
from heros.logging import LOGGER

router = APIRouter(prefix="/credentials", tags=["credentials"])


class CredentialUpdate(BaseModel):
    """Request body for updating credentials."""
    service_name: str = Field(..., description="Name of the service (e.g., 'engtec')")
    username: str = Field(..., description="New username for the service")
    password: str = Field(..., description="New password for the service")


class CredentialInfo(BaseModel):
    """Response body for credential information."""
    service_name: str
    username: str
    last_updated: datetime
    updated_by: Optional[str] = None
    is_active: bool


class CredentialUpdateResponse(BaseModel):
    """Response body after successful credential update."""
    success: bool
    message: str
    service_name: str
    updated_at: datetime
    updated_by: str


@router.get("/info/{service_name}", response_model=CredentialInfo)
def get_credential_info(service_name: str) -> CredentialInfo:
    """
    Get information about a service's credentials (without the password).
    
    Args:
        service_name: Name of the service (e.g., 'engtec')
        
    Returns:
        Credential metadata including last update time
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT service_name, username, last_updated, updated_by, is_active
                    FROM api_credentials
                    WHERE service_name = %s
                    """,
                    (service_name.lower(),)
                )
                result = cur.fetchone()
                
                if not result:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Service '{service_name}' not found"
                    )
                
                return CredentialInfo(
                    service_name=result[0],
                    username=result[1],
                    last_updated=result[2],
                    updated_by=result[3],
                    is_active=result[4]
                )
                
    except HTTPException:
        raise
    except Exception as e:
        LOGGER.error(f"Error retrieving credential info for {service_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve credential information"
        )


@router.get("/services")
def list_services() -> dict:
    """
    List all configured services and their credential status.
    
    Returns:
        Dictionary with list of services and their metadata
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT service_name, username, is_active, last_updated, updated_by
                    FROM api_credentials
                    ORDER BY service_name
                    """
                )
                results = cur.fetchall()
                
                services = [
                    {
                        "service_name": row[0],
                        "username": row[1],
                        "is_active": row[2],
                        "last_updated": row[3],
                        "updated_by": row[4]
                    }
                    for row in results
                ]
                
                return {
                    "services": services,
                    "count": len(services)
                }
                
    except Exception as e:
        LOGGER.error(f"Error listing services: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve services list"
        )


@router.post("/update", response_model=CredentialUpdateResponse)
def update_credential(credential_update: CredentialUpdate) -> CredentialUpdateResponse:
    """
    Update API credentials for a service.
    
    The new credentials will be encrypted before storage and the application's
    credential cache will be refreshed to use the new credentials on the next request.
    
    Args:
        credential_update: Object containing service_name, username, and password
        
    Returns:
        Success response with update timestamp
        
    Raises:
        HTTPException: If service not found or update fails
    """
    try:
        # Encrypt the password
        encrypted_password = encrypt_password(credential_update.password)
        
        with pool.connection() as conn:
            with conn.cursor() as cur:
                # Update the credential
                cur.execute(
                    """
                    UPDATE api_credentials
                    SET username = %s,
                        password_encrypted = %s,
                        last_updated = CURRENT_TIMESTAMP,
                        updated_by = %s
                    WHERE service_name = %s AND is_active = TRUE
                    RETURNING service_name, last_updated, updated_by
                    """,
                    (
                        credential_update.username,
                        encrypted_password,
                        "api_update",
                        credential_update.service_name.lower()
                    )
                )
                
                result = cur.fetchone()
                conn.commit()
                
                if not result:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Service '{credential_update.service_name}' not found or is inactive"
                    )
                
                # Clear the credential cache so new credentials are used immediately
                refresh_credential_cache(credential_update.service_name)
                
                LOGGER.info(
                    f"Credentials updated for service: {result[0]} "
                    f"by {result[2]} at {result[1]}"
                )
                
                return CredentialUpdateResponse(
                    success=True,
                    message=f"Credentials updated successfully for {credential_update.service_name}",
                    service_name=result[0],
                    updated_at=result[1],
                    updated_by=result[2]
                )
                
    except HTTPException:
        raise
    except Exception as e:
        LOGGER.error(f"Error updating credentials for {credential_update.service_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update credentials"
        )


@router.get("/audit/{service_name}")
def get_credential_audit_log(service_name: str, limit: int = 10) -> dict:
    """
    Retrieve the audit log for a service's credential changes.
    
    Args:
        service_name: Name of the service
        limit: Maximum number of audit records to return (default: 10)
        
    Returns:
        Dictionary with audit log entries
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT service_name, action, changed_at, changed_by, previous_username, 
                           new_username, notes
                    FROM api_credentials_audit
                    WHERE service_name = %s
                    ORDER BY changed_at DESC
                    LIMIT %s
                    """,
                    (service_name.lower(), limit)
                )
                results = cur.fetchall()
                
                audit_log = [
                    {
                        "service_name": row[0],
                        "action": row[1],
                        "changed_at": row[2],
                        "changed_by": row[3],
                        "previous_username": row[4],
                        "new_username": row[5],
                        "notes": row[6]
                    }
                    for row in results
                ]
                
                return {
                    "service_name": service_name,
                    "audit_log": audit_log,
                    "count": len(audit_log)
                }
                
    except Exception as e:
        LOGGER.error(f"Error retrieving audit log for {service_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve audit log"
        )
