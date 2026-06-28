from dataclasses import dataclass
from typing import Literal

CapabilityType = Literal[
    "discover",
    "read",
    "create",
    "update",
    "delete",
    "sync_inbound",
    "sync_outbound",
]
Resource = Literal[
    "products", "collections", "blogs", "articles", "locations", "glossary",
    "capabilities", "search", "links", "bulk",
]
SyncDirection = Literal["shopify_to_wagtail", "wagtail_to_shopify"] | None

SHOP_CONFIG_PREREQ = "ShopConfig with valid offline access token"
ROOT_PAGE_PREREQ = "ShopifyRootPage with slug=root under Wagtail site"
LOCATIONS_ROOT_PREREQ = (
    'ShopifyRootPage with slug=local-us under Wagtail site '
    '(optional parent_page_id on create_location; env LOCATIONS_PARENT_PAGE_ID)'
)
GLOSSARY_ROOT_PREREQ = (
    'ShopifyRootPage with slug=glossary under Wagtail site '
    '(optional parent_page_id on create_glossary_term)'
)


@dataclass(frozen=True)
class AgentCapability:
    operation_id: str
    method: str
    path: str
    capability_type: CapabilityType
    resource: Resource
    summary: str
    when_to_use: str
    prerequisites: tuple[str, ...]
    response_schema: str
    next_tools: tuple[str, ...]
    sync_direction: SyncDirection = None


def _cap(
    operation_id: str,
    method: str,
    path: str,
    capability_type: CapabilityType,
    resource: Resource,
    summary: str,
    when_to_use: str,
    response_schema: str,
    next_tools: tuple[str, ...] = (),
    prerequisites: tuple[str, ...] = (),
    sync_direction: SyncDirection = None,
) -> AgentCapability:
    return AgentCapability(
        operation_id=operation_id,
        method=method,
        path=path,
        capability_type=capability_type,
        resource=resource,
        summary=summary,
        when_to_use=when_to_use,
        prerequisites=prerequisites,
        response_schema=response_schema,
        next_tools=next_tools,
        sync_direction=sync_direction,
    )


CAPABILITIES: dict[str, AgentCapability] = {
    # Products
    "list_products": _cap(
        "list_products", "GET", "/products/",
        "discover", "products",
        "List Product pages from Wagtail",
        "Discover products, check sync status, or filter by locale before editing.",
        "List[ProductOut]",
        ("get_product", "update_product"),
    ),
    "create_product": _cap(
        "create_product", "POST", "/products/",
        "create", "products",
        "Create a Product page in Wagtail",
        "Create a Wagtail page manually when not using pull; set shopify_id or pull first.",
        "ProductOut",
        ("update_product", "push_product"),
        (ROOT_PAGE_PREREQ,),
    ),
    "pull_products_sync": _cap(
        "pull_products_sync", "GET", "/products/pull",
        "sync_inbound", "products",
        "Pull products from Shopify (GET alias)",
        "Same as POST pull — import Shopify catalog into Wagtail synchronously.",
        "ImportResultSchema",
        ("list_products", "get_product"),
        (SHOP_CONFIG_PREREQ, ROOT_PAGE_PREREQ),
        sync_direction="shopify_to_wagtail",
    ),
    "pull_products_sync_post": _cap(
        "pull_products_sync_post", "POST", "/products/pull",
        "sync_inbound", "products",
        "Pull products from Shopify (sync)",
        "First step for existing Shopify catalogs — imports all products into Wagtail.",
        "ImportResultSchema",
        ("list_products", "get_product", "update_product"),
        (SHOP_CONFIG_PREREQ, ROOT_PAGE_PREREQ),
        sync_direction="shopify_to_wagtail",
    ),
    "get_product": _cap(
        "get_product", "GET", "/products/{page_id}",
        "read", "products",
        "Get a single Product page",
        "Inspect full product content, shopify_id, and last_synced_at after pull or update.",
        "ProductOut",
        ("update_product", "push_product"),
    ),
    "update_product": _cap(
        "update_product", "PATCH", "/products/{page_id}",
        "update", "products",
        "Update a Product page",
        "Edit content; set publish=true to publish and auto-sync when sync_enabled=true.",
        "ProductOut",
        ("get_product", "push_product"),
    ),
    "delete_product": _cap(
        "delete_product", "DELETE", "/products/{page_id}",
        "delete", "products",
        "Delete a Product page from Wagtail",
        "Remove Wagtail page only — does not delete the Shopify product.",
        "None",
        ("list_products",),
    ),
    "push_product": _cap(
        "push_product", "POST", "/products/{page_id}/push",
        "sync_outbound", "products",
        "Push Product content to Shopify",
        "Explicit outbound sync; requires shopify_id on the page.",
        "SyncResultSchema",
        ("get_product",),
        (SHOP_CONFIG_PREREQ, "Page must have shopify_id"),
        sync_direction="wagtail_to_shopify",
    ),
    # Collections
    "list_collections": _cap(
        "list_collections", "GET", "/collections/",
        "discover", "collections",
        "List Collection pages from Wagtail",
        "Discover collections and sync status before editing.",
        "List[CollectionOut]",
        ("get_collection", "update_collection"),
    ),
    "create_collection": _cap(
        "create_collection", "POST", "/collections/",
        "create", "collections",
        "Create a Collection page in Wagtail",
        "Create Wagtail page manually; link shopify_id or pull from Shopify first.",
        "CollectionOut",
        ("update_collection", "push_collection"),
        (ROOT_PAGE_PREREQ,),
    ),
    "pull_collections_sync": _cap(
        "pull_collections_sync", "POST", "/collections/pull",
        "sync_inbound", "collections",
        "Pull collections from Shopify (sync)",
        "Import all Shopify collections into Wagtail synchronously.",
        "ImportResultSchema",
        ("list_collections", "get_collection"),
        (SHOP_CONFIG_PREREQ, ROOT_PAGE_PREREQ),
        sync_direction="shopify_to_wagtail",
    ),
    "get_collection": _cap(
        "get_collection", "GET", "/collections/{page_id}",
        "read", "collections",
        "Get a single Collection page",
        "Inspect collection content and sync state.",
        "CollectionOut",
        ("update_collection", "push_collection"),
    ),
    "update_collection": _cap(
        "update_collection", "PATCH", "/collections/{page_id}",
        "update", "collections",
        "Update a Collection page",
        "Edit content; publish=true triggers sync when sync_enabled=true.",
        "CollectionOut",
        ("get_collection", "push_collection"),
    ),
    "delete_collection": _cap(
        "delete_collection", "DELETE", "/collections/{page_id}",
        "delete", "collections",
        "Delete a Collection page from Wagtail",
        "Removes Wagtail page only — Shopify collection is untouched.",
        "None",
        ("list_collections",),
    ),
    "push_collection": _cap(
        "push_collection", "POST", "/collections/{page_id}/push",
        "sync_outbound", "collections",
        "Push Collection content to Shopify",
        "Explicit outbound sync; requires shopify_id.",
        "SyncResultSchema",
        ("get_collection",),
        (SHOP_CONFIG_PREREQ, "Page must have shopify_id"),
        sync_direction="wagtail_to_shopify",
    ),
    # Blogs
    "list_blogs": _cap(
        "list_blogs", "GET", "/blogs/",
        "discover", "blogs",
        "List Blog pages from Wagtail",
        "Discover blogs and article counts before managing articles.",
        "List[BlogOut]",
        ("get_blog", "list_articles"),
    ),
    "create_blog": _cap(
        "create_blog", "POST", "/blogs/",
        "create", "blogs",
        "Create a Blog page in Wagtail",
        "Create blog container; push to Shopify to obtain shopify_id for articles.",
        "BlogOut",
        ("update_blog", "push_blog"),
        (ROOT_PAGE_PREREQ,),
    ),
    "pull_blogs_sync": _cap(
        "pull_blogs_sync", "POST", "/blogs/pull",
        "sync_inbound", "blogs",
        "Pull blogs and articles from Shopify (sync)",
        "Imports blogs and nested articles in one synchronous call.",
        "ImportResultSchema",
        ("list_blogs", "list_articles"),
        (SHOP_CONFIG_PREREQ, ROOT_PAGE_PREREQ),
        sync_direction="shopify_to_wagtail",
    ),
    "get_blog": _cap(
        "get_blog", "GET", "/blogs/{page_id}",
        "read", "blogs",
        "Get a single Blog page",
        "Inspect blog metadata and article_count.",
        "BlogOut",
        ("update_blog", "list_articles"),
    ),
    "update_blog": _cap(
        "update_blog", "PATCH", "/blogs/{page_id}",
        "update", "blogs",
        "Update a Blog page",
        "Edit blog settings; publish=true may create blog in Shopify if no shopify_id.",
        "BlogOut",
        ("get_blog", "push_blog"),
    ),
    "delete_blog": _cap(
        "delete_blog", "DELETE", "/blogs/{page_id}",
        "delete", "blogs",
        "Delete a Blog page from Wagtail",
        "Cascades to child Article pages in Wagtail; Shopify content untouched.",
        "None",
        ("list_blogs",),
    ),
    "push_blog": _cap(
        "push_blog", "POST", "/blogs/{page_id}/push",
        "sync_outbound", "blogs",
        "Push Blog content to Shopify",
        "Creates blog in Shopify if shopify_id is empty; required before pushing articles.",
        "SyncResultSchema",
        ("get_blog", "create_article"),
        (SHOP_CONFIG_PREREQ,),
        sync_direction="wagtail_to_shopify",
    ),
    # Articles
    "list_articles": _cap(
        "list_articles", "GET", "/articles/",
        "discover", "articles",
        "List Article pages from Wagtail",
        "Discover articles; filter by blog_id to scope to one blog.",
        "List[ArticleOut]",
        ("get_article", "update_article"),
    ),
    "create_article": _cap(
        "create_article", "POST", "/articles/",
        "create", "articles",
        "Create an Article page under a Blog",
        "Add article content; parent BlogPage should have shopify_id before sync.",
        "ArticleOut",
        ("update_article", "push_article"),
        ("Valid blog_id (parent BlogPage)",),
    ),
    "pull_articles_sync": _cap(
        "pull_articles_sync", "POST", "/articles/pull",
        "sync_inbound", "articles",
        "Pull articles from Shopify (sync)",
        "Alias for blogs pull — imports blogs and articles together.",
        "ImportResultSchema",
        ("list_articles", "get_article"),
        (SHOP_CONFIG_PREREQ, ROOT_PAGE_PREREQ),
        sync_direction="shopify_to_wagtail",
    ),
    "get_article": _cap(
        "get_article", "GET", "/articles/{page_id}",
        "read", "articles",
        "Get a single Article page",
        "Inspect article body, parent blog_id, and sync state.",
        "ArticleOut",
        ("update_article", "push_article"),
    ),
    "update_article": _cap(
        "update_article", "PATCH", "/articles/{page_id}",
        "update", "articles",
        "Update an Article page",
        "Edit content; publish=true syncs when sync_enabled and parent blog has shopify_id.",
        "ArticleOut",
        ("get_article", "push_article"),
    ),
    "delete_article": _cap(
        "delete_article", "DELETE", "/articles/{page_id}",
        "delete", "articles",
        "Delete an Article page from Wagtail",
        "Removes Wagtail page only — Shopify article is untouched.",
        "None",
        ("list_articles",),
    ),
    "push_article": _cap(
        "push_article", "POST", "/articles/{page_id}/push",
        "sync_outbound", "articles",
        "Push Article content to Shopify",
        "Creates article in Shopify; parent BlogPage must have shopify_id.",
        "SyncResultSchema",
        ("get_article",),
        (SHOP_CONFIG_PREREQ, "Parent BlogPage must have shopify_id"),
        sync_direction="wagtail_to_shopify",
    ),
    # Locations (no pull)
    "list_locations": _cap(
        "list_locations", "GET", "/locations/",
        "discover", "locations",
        "List Location pages from Wagtail",
        "Discover Wagtail-origin location pages before push to Shopify metaobjects.",
        "List[LocationOut]",
        ("get_location", "create_location"),
    ),
    "create_location": _cap(
        "create_location", "POST", "/locations/",
        "create", "locations",
        "Create a Location page in Wagtail",
        "Author location content in Wagtail; push to Shopify metaobject type local_page.",
        "LocationOut",
        ("update_location", "push_location"),
        (LOCATIONS_ROOT_PREREQ,),
    ),
    "get_location": _cap(
        "get_location", "GET", "/locations/{page_id}",
        "read", "locations",
        "Get a single Location page",
        "Verify shopify_id and last_synced_at after push.",
        "LocationOut",
        ("update_location", "push_location"),
    ),
    "update_location": _cap(
        "update_location", "PATCH", "/locations/{page_id}",
        "update", "locations",
        "Update a Location page",
        "Edit location fields; publish=true optional before push.",
        "LocationOut",
        ("push_location", "get_location"),
    ),
    "delete_location": _cap(
        "delete_location", "DELETE", "/locations/{page_id}",
        "delete", "locations",
        "Delete a Location page from Wagtail",
        "Removes Wagtail page only — Shopify metaobject is untouched.",
        "None",
        ("list_locations",),
    ),
    "push_location": _cap(
        "push_location", "POST", "/locations/{page_id}/push",
        "sync_outbound", "locations",
        "Push Location page to Shopify metaobject",
        "Upserts metaobject local_page; saves shopify_id on first success.",
        "SyncResultSchema",
        ("get_location",),
        (SHOP_CONFIG_PREREQ,),
        sync_direction="wagtail_to_shopify",
    ),
    # Glossary (no pull)
    "list_glossary_terms": _cap(
        "list_glossary_terms", "GET", "/glossary/",
        "discover", "glossary",
        "List Glossary term pages from Wagtail",
        "Discover Wagtail-origin glossary terms before push to Shopify metaobjects.",
        "List[GlossaryTermOut]",
        ("get_glossary_term", "create_glossary_term"),
    ),
    "create_glossary_term": _cap(
        "create_glossary_term", "POST", "/glossary/",
        "create", "glossary",
        "Create a Glossary term page in Wagtail",
        "Author glossary term content in Wagtail; push to Shopify metaobject type glossary_term.",
        "GlossaryTermOut",
        ("update_glossary_term", "push_glossary_term"),
        (GLOSSARY_ROOT_PREREQ,),
    ),
    "get_glossary_term": _cap(
        "get_glossary_term", "GET", "/glossary/{page_id}",
        "read", "glossary",
        "Get a single Glossary term page",
        "Verify shopify_id and last_synced_at after push.",
        "GlossaryTermOut",
        ("update_glossary_term", "push_glossary_term"),
    ),
    "update_glossary_term": _cap(
        "update_glossary_term", "PATCH", "/glossary/{page_id}",
        "update", "glossary",
        "Update a Glossary term page",
        "Edit term fields; publish=true optional before push.",
        "GlossaryTermOut",
        ("push_glossary_term", "get_glossary_term"),
    ),
    "delete_glossary_term": _cap(
        "delete_glossary_term", "DELETE", "/glossary/{page_id}",
        "delete", "glossary",
        "Delete a Glossary term page from Wagtail",
        "Removes Wagtail page only — Shopify metaobject is untouched.",
        "None",
        ("list_glossary_terms",),
    ),
    "push_glossary_term": _cap(
        "push_glossary_term", "POST", "/glossary/{page_id}/push",
        "sync_outbound", "glossary",
        "Push Glossary term page to Shopify metaobject",
        "Upserts metaobject glossary_term; saves shopify_id on first success.",
        "SyncResultSchema",
        ("get_glossary_term",),
        (SHOP_CONFIG_PREREQ,),
        sync_direction="wagtail_to_shopify",
    ),
    # Capabilities catalog
    "list_agent_capabilities": _cap(
        "list_agent_capabilities", "GET", "/capabilities/",
        "discover", "capabilities",
        "List all agent capabilities and workflows",
        "Entry point for agents — machine-readable tool catalog with prerequisites and next tools.",
        "AgentCapabilitiesOut",
        ("pull_products_sync_post", "list_products"),
    ),
    # Search
    "search_content": _cap(
        "search_content", "GET", "/search/",
        "discover", "search",
        "Full-text search across all content resources",
        (
            "Use to find pages by keyword before editing, linking, or auditing. "
            "Filter by resource, locale, or live status. "
            "Returns excerpt with match context."
        ),
        "SearchResponse",
        ("get_article", "get_product", "links_index", "update_article"),
    ),
    # Links index
    "links_index": _cap(
        "links_index", "GET", "/links/index/",
        "discover", "links",
        "Complete slug/handle index for internal linking",
        (
            "Use to build internal links without iterating individual resource endpoints. "
            "Returns all page slugs, URLs, and shopify_handles. Cached 5 min."
        ),
        "SlugIndexResponse",
        ("get_article", "get_product", "bulk_update"),
    ),
    # Bulk update
    "bulk_update": _cap(
        "bulk_update", "POST", "/bulk/update/",
        "update", "bulk",
        "Batch-update up to 50 pages in a single call",
        (
            "Use to update SEO fields, locale, or other attributes across many pages efficiently. "
            "Each operation is independent — one failure does not stop others. Max 50 ops."
        ),
        "BulkUpdateResponse",
        ("links_index", "get_article", "get_product"),
    ),
    # Body patch
    "body_patch_article": _cap(
        "body_patch_article", "POST", "/articles/{page_id}/body/patch/",
        "update", "articles",
        "Patch article body with structured insert/replace/delete operations",
        (
            "Use to surgically edit article body content without replacing the whole field. "
            "Target headings by tag:text or blocks by index. "
            "Supports StreamField and RichTextField bodies automatically."
        ),
        "ArticleOut",
        ("get_article", "push_article"),
        ("Valid article page_id",),
    ),
    # Article versions
    "list_article_versions": _cap(
        "list_article_versions", "GET", "/articles/{page_id}/versions/",
        "read", "articles",
        "List available Wagtail revisions for an article",
        "Use to audit edit history or find a revision_id before reverting.",
        "List[RevisionItem]",
        ("get_article_version", "revert_article_version"),
    ),
    "get_article_version": _cap(
        "get_article_version", "GET", "/articles/{page_id}/versions/{revision_id}/",
        "read", "articles",
        "Get the content of a specific article revision",
        "Use to preview or compare a past revision before deciding to revert.",
        "ArticleOut",
        ("revert_article_version",),
    ),
    "revert_article_version": _cap(
        "revert_article_version", "POST", "/articles/{page_id}/revert/{revision_id}/",
        "update", "articles",
        "Restore a past article revision as the current draft",
        "Use to roll back bad edits. Does NOT auto-publish — creates a new draft.",
        "ArticleOut",
        ("get_article", "push_article"),
    ),
}

WORKFLOWS: dict[str, tuple[str, ...]] = {
    "products_existing_store": (
        "pull_products_sync_post",
        "list_products",
        "update_product",
        "get_product",
    ),
    "collections_existing_store": (
        "pull_collections_sync",
        "list_collections",
        "update_collection",
        "get_collection",
    ),
    "blogs_and_articles": (
        "pull_blogs_sync",
        "list_blogs",
        "list_articles",
        "update_article",
        "get_article",
    ),
    "locations_wagtail_origin": (
        "create_location",
        "update_location",
        "push_location",
        "get_location",
    ),
    "glossary_wagtail_origin": (
        "create_glossary_term",
        "update_glossary_term",
        "push_glossary_term",
        "get_glossary_term",
    ),
    "search_and_link": (
        "search_content",
        "links_index",
        "update_article",
    ),
    "bulk_meta_update": (
        "links_index",
        "bulk_update",
    ),
    "body_surgery": (
        "get_article",
        "body_patch_article",
        "push_article",
    ),
}

TAG_DESCRIPTIONS: dict[str, str] = {
    "Products": (
        "Capability group: Shopify Product content. Supports discover, read, create, update, "
        "delete, sync_inbound (pull), sync_outbound (push)."
    ),
    "Collections": (
        "Capability group: Shopify Collection content. Supports discover, read, create, update, "
        "delete, sync_inbound (pull), sync_outbound (push)."
    ),
    "Blogs": (
        "Capability group: Shopify Blog containers. Pull also imports nested articles. "
        "Push creates blog in Shopify when shopify_id is missing."
    ),
    "Articles": (
        "Capability group: Shopify Blog articles nested under BlogPage. "
        "Parent blog must be synced before article push."
    ),
    "Locations": (
        "Capability group: Wagtail-origin Location pages pushed to Shopify metaobjects "
        "(type local_page). No pull endpoint — content is authored in Wagtail."
    ),
    "Glossary": (
        "Capability group: Wagtail-origin Glossary term pages pushed to Shopify metaobjects "
        "(type glossary_term). No pull endpoint — content is authored in Wagtail."
    ),
    "Capabilities": (
        "Meta capability group: machine-readable agent tool catalog and predefined workflows."
    ),
    "Search": (
        "Capability group: full-text cross-resource search. Returns excerpts and page metadata."
    ),
    "Links": (
        "Capability group: slug/handle index for building internal links without iterating resources."
    ),
    "Bulk": (
        "Capability group: batch updates across up to 50 pages in a single API call."
    ),
    "Versions": (
        "Capability group: Wagtail revision history for articles — list, get, and revert revisions."
    ),
}
