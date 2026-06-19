from ninja import Router

from ..agent_registry import CAPABILITIES, WORKFLOWS
from ..openapi_agent import agent_openapi_extra, capability_docstring
from ..schemas.capabilities import AgentAuthSchema, AgentCapabilitiesOut, AgentToolSchema

router = Router()


@router.get(
    "/",
    response=AgentCapabilitiesOut,
    summary="List Agent Capabilities",
    operation_id="list_agent_capabilities",
    description=capability_docstring("list_agent_capabilities"),
    openapi_extra=agent_openapi_extra("list_agent_capabilities"),
)
def list_agent_capabilities(request):
    """Entry point for agents — see description in OpenAPI."""
    tools = [
        AgentToolSchema(
            operation_id=cap.operation_id,
            method=cap.method,
            path=cap.path,
            capability_type=cap.capability_type,
            resource=cap.resource,
            summary=cap.summary,
            when_to_use=cap.when_to_use,
            prerequisites=list(cap.prerequisites),
            response_schema=cap.response_schema,
            next_tools=list(cap.next_tools),
            sync_direction=cap.sync_direction,
        )
        for cap in CAPABILITIES.values()
        if cap.operation_id != "list_agent_capabilities"
    ]
    return AgentCapabilitiesOut(
        api_version="1.1.0",
        auth=AgentAuthSchema(),
        tools=tools,
        workflows={name: list(steps) for name, steps in WORKFLOWS.items()},
    )
