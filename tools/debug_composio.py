"""Debug helper for Composio / Gmail connection issues.

Run this locally to inspect connected accounts, tools, and fetch Gmail profile for your `GMAIL_USER_ID`.

Example use:
    venv\Scripts\activate
    python tools\debug_composio.py

This prints results to stdout for inspection.
"""
import os
import json
from composio import Composio
from config import config


def main():
    composio = Composio(api_key=config.composio_api_key)
    user_id = config.gmail_user_id or "me"
    connected_account = config.gmail_connected_account_id

    print("Composio API Key OK: ", bool(config.composio_api_key))
    print("GMAIL_USER_ID: ", user_id)
    print("GMAIL_CONNECTED_ACCOUNT_ID: ", connected_account)

    # List connected accounts for this user
    try:
        print("\nListing connected accounts for this user...")
        accounts = composio.connected_accounts.list({"userIds": [user_id]})
        print(json.dumps(accounts, default=str, indent=2))
    except Exception as e:
        print("Failed to list connected accounts:", e)

    # Get tools available for this user from the GMAIL toolkit
    try:
        print("\nListing GMAIL toolkit tools for user...")
        tools = composio.tools.get(user_id=user_id, toolkits=["GMAIL"])
        print(json.dumps(tools, default=str, indent=2))
    except Exception as e:
        print("Failed to get GMAIL toolkit tools:", e)

    # Try getting profile
    try:
        print("\nTrying GMAIL_GET_PROFILE for the user...")
        result = composio.tools.execute(
            slug="GMAIL_GET_PROFILE",
            arguments={},
            user_id=user_id,
            connected_account_id=connected_account,
        )
        print(json.dumps(result, default=str, indent=2))
    except Exception as e:
        print("GMAIL_GET_PROFILE failed:", e)


if __name__ == "__main__":
    main()
