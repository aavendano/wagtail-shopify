from typing import Literal

from ninja import Field, Schema

from ..agent_registry import CapabilityType, Resource, SyncDirection


class AgentToolSchema(Schema):
    operation_id: str = Field(..., description="Stable tool name matching OpenAPI operationId.")
    method: str = Field(..., description="HTTP method for this capability.")
    path: str = Field(..., description="API path relative to /api/v1.")
    capability_type: CapabilityType = Field(
        ...,
        description=(
            "Type of capability: discover, read, create, update, delete, "
            "sync_inbound (Shopify→Wagtail), sync_outbound (Wagtail→Shopify)."
        ),
    )
    resource: Resource = Field(..., description="Content resource this tool operates on.")
    summary: str = Field(..., description="Short human-readable summary of the tool.")
    when_to_use: str = Field(..., description="Guidance for when an agent should call this tool.")
    prerequisites: list[str] = Field(
        default_factory=list,
        description="Conditions that must be met before calling this tool.",
    )
    response_schema: str = Field(..., description="Name of the primary response schema.")
    next_tools: list[str] = Field(
        default_factory=list,
        description="Suggested operation_ids to call after this tool succeeds.",
    )
    sync_direction: SyncDirection = Field(
        None,
        description="Sync direction for sync_inbound/sync_outbound tools; null otherwise.",
    )


class AgentAuthSchema(Schema):
    type: Literal["bearer"] = Field("bearer", description="Authentication scheme type.")
    header: Literal["Authorization"] = Field(
        "Authorization",
        description="HTTP header name for the API key or OAuth access token.",
    )


class AgentCapabilitiesOut(Schema):
    api_version: str = Field(..., description="API version string.")
    auth: AgentAuthSchema = Field(..., description="Authentication requirements for all tools.")
    tools: list[AgentToolSchema] = Field(
        ...,
        description="Complete catalog of agent capabilities keyed by operation_id.",
    )
    workflows: dict[str, list[str]] = Field(
        ...,
        description="Predefined ordered sequences of operation_ids for common agent tasks.",
    )
