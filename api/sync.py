from ninja.errors import HttpError

from shopify_content.sync.service import ImportResource, run_shopify_import_for_api


def execute_pull(resource: ImportResource, *, new_only: bool = False) -> tuple[int, dict]:
    """
    Run a synchronous Shopify → Wagtail import for API consumers.
    Returns (200, ImportResultSchema dict) or raises HttpError(400).
    """
    try:
        return 200, run_shopify_import_for_api(resource, new_only=new_only)
    except RuntimeError as e:
        raise HttpError(400, str(e))
