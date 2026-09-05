"""Resolve Authorization for Streamable HTTP MCP requests."""


def resolve_streamable_authorization(
    *,
    request_authorization: str,
    stored_session_authorization: str,
    fallback_authorization: str,
    authenticate_token,
) -> str:
    """Return a validated Authorization header, or empty string.

    Prefer a valid Bearer on the current request, then a token already bound
    to the MCP session, then MCP_DEFAULT_API_KEY. Invalid or expired tokens
    are skipped so a stale client header cannot overwrite a good session.
    """

    def validated(header: str) -> str:
        if not header or not header.lower().startswith("bearer "):
            return ""
        token = header.split(" ", 1)[1].strip()
        if not token:
            return ""
        if authenticate_token(token):
            return header if header.lower().startswith("bearer ") else f"Bearer {token}"
        return ""

    return (
        validated(request_authorization)
        or validated(stored_session_authorization)
        or validated(fallback_authorization)
    )
