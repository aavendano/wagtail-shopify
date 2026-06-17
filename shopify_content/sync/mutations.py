"""
GraphQL write mutations for pushing Wagtail content to Shopify Admin.

Verified against Shopify Admin API 2025-04 schema:
  - articleCreate(article: ArticleCreateInput!) — fields: title, author (required), blogId, body, summary, isPublished
  - articleUpdate(id: ID!, article: ArticleUpdateInput!) — publishedAt is read-only; not accepted on write inputs
  - blogCreate(blog: BlogCreateInput!) — fields: title (required), handle, commentPolicy
  - blogUpdate(id: ID!, blog: BlogUpdateInput!)
  - Article has no native seo field → use metafieldsSet for global.title_tag / global.description_tag
"""

# ---------------------------------------------------------------------------
# Shared metafields — works for Product, Collection, Article, Blog
# ---------------------------------------------------------------------------

METAFIELDS_SET = """
mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
      type
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""

# ---------------------------------------------------------------------------
# Products — native seo field available
# ---------------------------------------------------------------------------

PRODUCT_UPDATE = """
mutation ProductUpdate($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      handle
      title
      seo {
        title
        description
      }
      updatedAt
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""

# ---------------------------------------------------------------------------
# Collections — native seo field available
# ---------------------------------------------------------------------------

COLLECTION_UPDATE = """
mutation CollectionUpdate($input: CollectionInput!) {
  collectionUpdate(input: $input) {
    collection {
      id
      handle
      title
      seo {
        title
        description
      }
      updatedAt
    }
    userErrors {
      field
      message
    }
  }
}
"""

# ---------------------------------------------------------------------------
# Blogs — no native seo field
# ---------------------------------------------------------------------------

BLOG_CREATE = """
mutation BlogCreate($blog: BlogCreateInput!) {
  blogCreate(blog: $blog) {
    blog {
      id
      handle
      title
      commentPolicy
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""

BLOG_UPDATE = """
mutation BlogUpdate($id: ID!, $blog: BlogUpdateInput!) {
  blogUpdate(id: $id, blog: $blog) {
    blog {
      id
      handle
      title
      commentPolicy
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""

# ---------------------------------------------------------------------------
# Articles — no native seo field; use metafieldsSet for SEO
# ---------------------------------------------------------------------------

ARTICLE_CREATE = """
mutation ArticleCreate($article: ArticleCreateInput!) {
  articleCreate(article: $article) {
    article {
      id
      handle
      title
      publishedAt
      blog {
        id
      }
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""

ARTICLE_UPDATE = """
mutation ArticleUpdate($id: ID!, $article: ArticleUpdateInput!) {
  articleUpdate(id: $id, article: $article) {
    article {
      id
      handle
      title
      publishedAt
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""

# ---------------------------------------------------------------------------
# Translations — for hreflang support across locales
# ---------------------------------------------------------------------------

TRANSLATIONS_REGISTER = """
mutation TranslationsRegister($resourceId: ID!, $translations: [TranslationInput!]!) {
  translationsRegister(resourceId: $resourceId, translations: $translations) {
    translations {
      key
      locale
      value
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""

# ---------------------------------------------------------------------------
# Metaobjects — app-owned definitions (defined in shopify.app.*.toml)
# ---------------------------------------------------------------------------

METAOBJECT_UPSERT = """
mutation MetaobjectUpsert($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
  metaobjectUpsert(handle: $handle, metaobject: $metaobject) {
    metaobject {
      id
      handle
      type
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""
