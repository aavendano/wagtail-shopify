"""Asset reference contract ``asset:<stable-id>`` (resolver decoupled from storage)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass(frozen=True)
class AssetRef:
    stable_id: str

    @classmethod
    def parse(cls, token: str) -> Optional["AssetRef"]:
        if not token.startswith("asset:"):
            return None
        ident = token.split(":", 1)[1].strip()
        if not ident:
            return None
        return cls(stable_id=ident)


class AssetUrlResolver(Protocol):
    def url_for(self, asset: AssetRef) -> str:
        ...


class PassthroughAssetResolver:
    """Default until a shop-specific CDN map is wired."""

    def url_for(self, asset: AssetRef) -> str:
        return f"/cdn/assets/{asset.stable_id}"
