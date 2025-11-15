from typing import Any, Dict, Optional
import structlog

logger = structlog.get_logger(__name__)


def execute_tool(composio_client, slug: str, params: Optional[Dict[str, Any]] = None,
                 connected_account_id: Optional[str] = None,
                 user_id: Optional[str] = None,
                 version: Optional[str] = None) -> Dict[str, Any]:
    """Safely execute a Composio tool call.

    Tries the common keyword-argument form first (slug=, arguments=, connected_account_id=,
    user_id=, version=). If that raises a TypeError (client expects different signature),
    falls back to a positional call with defensive kwargs.

    Returns the composio response (usually a dict-like Pydantic model). On error returns
    a dict with `successful: False` and `error` message.
    """
    params = params or {}
    try:
        return composio_client.tools.execute(
            slug=slug,
            arguments=params,
            connected_account_id=connected_account_id,
            user_id=user_id,
            version=version,
        )
    except TypeError:
        # Some versions of the SDK accept positional (slug, params) and different kw names.
        try:
            kw = {}
            if connected_account_id:
                kw["connected_account_id"] = connected_account_id
            if version:
                kw["version"] = version
            if user_id:
                # pass as kw if supported; otherwise it's included in params below
                kw["user_id"] = user_id

            return composio_client.tools.execute(slug, params, **kw)
        except Exception as e:
            logger.error("Composio execute fallback failed", error=str(e))
            return {"successful": False, "error": str(e)}
    except Exception as e:
        logger.error("Composio execute failed", error=str(e))
        return {"successful": False, "error": str(e)}


def validate_connected_account(composio_client, user_id: str, toolkit_slug: str = "GMAIL") -> Optional[str]:
    """Return the active connected_account_id for the given user and toolkit slug.

    If a matching active connected account is found, returns the connected account id
    (e.g. ca_...). Otherwise returns None.
    """
    try:
        # The Composio SDK returns a paginated list with items: use the typed wrapper
        resp = composio_client.connected_accounts.list({"userIds": [user_id], "toolkitSlugs": [toolkit_slug]})
        # Items usually in resp.items — this is typed obj; convert to list if needed
        items = getattr(resp, "items", None) or resp
        for item in items:
            # item.status commonly is ACTIVE/INACTIVE
            status = getattr(item, "status", None) or item.get("status") if isinstance(item, dict) else None
            if status and status.upper() == "ACTIVE":
                # id property usually is `id` or `nanoid` - both are common
                connected_id = getattr(item, "id", None) or item.get("id") if isinstance(item, dict) else None
                if connected_id:
                    return connected_id
        return None
    except Exception as e:
        logger.warning("validate_connected_account failed", error=str(e))
        return None
