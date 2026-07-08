"""
Enqueue embedded management commands as Celery tasks.
"""

from shopify_content.embedded_commands.registry import get_command_by_id
from shopify_content.models.command_run import EmbeddedCommandRun


def enqueue_embedded_command(command_id: str) -> EmbeddedCommandRun:
    spec = get_command_by_id(command_id)
    if spec is None:
        raise ValueError(f'Unknown command_id: {command_id}')

    run = EmbeddedCommandRun.objects.create(
        command_id=spec.id,
        command_name=spec.command,
        kwargs=dict(spec.kwargs),
        message='Comando en cola.',
    )

    from shopify_content.tasks import run_embedded_command_task

    async_result = run_embedded_command_task.delay(run.pk)
    run.celery_task_id = async_result.id or ''
    run.save(update_fields=['celery_task_id'])
    return run
