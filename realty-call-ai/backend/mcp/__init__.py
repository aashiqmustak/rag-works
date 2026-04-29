"""
MCP package initialization
"""
from .clients import (
    get_crm_client,
    get_calendar_client,
    get_gmail_client,
    CRMClient,
    CalendarClient,
    GmailClient
)

__all__ = [
    "get_crm_client",
    "get_calendar_client",
    "get_gmail_client",
    "CRMClient",
    "CalendarClient",
    "GmailClient"
]
