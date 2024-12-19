from typing import Optional

from fastapi import Header, HTTPException, Request

from config import settings
from utils.security import verify_signature


async def verify_github_signature(
    request: Request, x_hub_signature_256: Optional[str] = Header(None)
):
    """
    Dependency to verify GitHub webhook signatures.
    Usage:
        @router.post("/webhook")
        async def webhook(verified=Depends(verify_github_signature)):
            ...
    """
    body = await request.body()
    if not verify_signature(body, settings.webhook_secret, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Invalid signature")
    return True


async def get_terminal_manager():
    """
    Dependency to get a configured TerminalManager instance.
    Usage:
        @router.websocket("/ws/terminal")
        async def terminal(
            websocket: WebSocket,
            terminal=Depends(get_terminal_manager)
        ):
            ...
    """
    from core.terminal import TerminalManager

    return TerminalManager(settings.base_dir)
