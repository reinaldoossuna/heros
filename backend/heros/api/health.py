"""Health check endpoints for monitoring system status."""

from pydantic import BaseModel
from typing import Literal

from heros.db_access import pool
from heros.logging import LOGGER
import heros.outbound_apis.noaa as noaa
import heros.outbound_apis.engtec as engtec
from heros.db_access.credentials import get_credential
from heros.config import settings
from fastapi import APIRouter


class ServiceStatus(BaseModel):
    """Status of an external service."""
    name: str
    status: Literal["healthy", "unhealthy", "unknown"]
    message: str = ""


class HealthCheckResponse(BaseModel):
    """Overall health check response."""
    status: Literal["healthy", "degraded", "unhealthy"]
    database: Literal["healthy", "unhealthy"]
    services: list[ServiceStatus]
    message: str = ""


router = APIRouter()


def check_database_health() -> bool:
    """Check if database connection is healthy."""
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return True
    except Exception as e:
        LOGGER.error(f"Database health check failed: {e}")
        return False


def check_noaa_service() -> ServiceStatus:
    """Check NOAA service availability and credentials."""
    try:
        db_config = get_credential("noaa")
        config = db_config if db_config is not None else settings.noaa
        
        if noaa.verify_login(config.user, config.password):
            return ServiceStatus(name="NOAA", status="healthy")
        else:
            return ServiceStatus(name="NOAA", status="unhealthy", message="Authentication failed")
    except Exception as e:
        LOGGER.debug(f"NOAA health check error: {e}")
        return ServiceStatus(name="NOAA", status="unhealthy", message=str(e))


def check_engtec_service() -> ServiceStatus:
    """Check EnGtec service availability."""
    try:
        db_config = get_credential("engtec")
        config = db_config if db_config is not None else settings.engtec
        
        session = engtec._login(config.user, config.password)
        if session is not None:
            session.close()
            return ServiceStatus(name="EnGtec", status="healthy")
        else:
            return ServiceStatus(name="EnGtec", status="unhealthy", message="Failed to authenticate")
    except Exception as e:
        LOGGER.debug(f"EnGtec health check error: {e}")
        return ServiceStatus(name="EnGtec", status="unhealthy", message=str(e))


@router.get("/health", response_model=HealthCheckResponse, status_code=200)
def health_check() -> HealthCheckResponse:
    """
    Comprehensive health check endpoint.
    
    Returns:
        HealthCheckResponse: Overall health status with database and external services status
    """
    db_healthy = check_database_health()
    
    services = [
        check_noaa_service(),
        check_engtec_service(),
    ]
    
    unhealthy_services = [s for s in services if s.status == "unhealthy"]
    
    if not db_healthy:
        return HealthCheckResponse(
            status="unhealthy",
            database="unhealthy",
            services=services,
            message="Database connection failed"
        )
    
    if unhealthy_services:
        return HealthCheckResponse(
            status="degraded",
            database="healthy",
            services=services,
            message=f"{len(unhealthy_services)} external service(s) unavailable"
        )
    
    return HealthCheckResponse(
        status="healthy",
        database="healthy",
        services=services,
        message="All systems operational"
    )
