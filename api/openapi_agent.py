from .agent_registry import CAPABILITIES, TAG_DESCRIPTIONS, AgentCapability


def get_capability(operation_id: str) -> AgentCapability:
    try:
        return CAPABILITIES[operation_id]
    except KeyError as exc:
        raise KeyError(f"Unknown operation_id: {operation_id}") from exc


def agent_openapi_extra(operation_id: str) -> dict:
    cap = get_capability(operation_id)
    extra = {
        "x-agent-capability-type": cap.capability_type,
        "x-agent-resource": cap.resource,
        "x-agent-next-tools": list(cap.next_tools),
        "x-agent-prerequisites": list(cap.prerequisites),
    }
    if cap.sync_direction:
        extra["x-agent-sync-direction"] = cap.sync_direction
    return extra


def capability_docstring(operation_id: str) -> str:
    cap = get_capability(operation_id)
    lines = [
        f"Capability: {cap.capability_type} — {cap.resource}",
        f"When to use: {cap.when_to_use}",
    ]
    if cap.prerequisites:
        lines.append(f"Prerequisites: {'; '.join(cap.prerequisites)}")
    lines.append(f"Returns: {cap.response_schema}")
    if cap.next_tools:
        lines.append(f"Next tools: {', '.join(cap.next_tools)}")
    return "\n".join(lines)


def build_openapi_tags() -> list[dict[str, str]]:
    return [
        {"name": name, "description": description}
        for name, description in TAG_DESCRIPTIONS.items()
    ]
