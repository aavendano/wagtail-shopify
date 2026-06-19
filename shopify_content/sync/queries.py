"""
GraphQL read queries for importing Shopify content into Wagtail.

Field names use the Shopify Admin API 2025-04 schema:
  - Article.body  (HTML) — NOT bodyHtml
  - Article.summary (HTML) — NOT summaryHtml
  - Blog.commentPolicy — NOT commentable

List/pull queries omit metafields and request only image URLs (no file download).
"""

# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------

PRODUCT_IMAGE_FIELDS = """
  images(first: 10) {
    edges {
      node {
        id
        url
        altText
      }
    }
  }
"""

PRODUCT_LIST_FIELDS = """
  id
  handle
  title
  descriptionHtml
  vendor
  productType
  status
  tags
  seo {
    title
    description
  }
""" + PRODUCT_IMAGE_FIELDS

PRODUCT_FIELDS = PRODUCT_LIST_FIELDS

GET_PRODUCT = """
query GetProduct($id: ID!) {
  product(id: $id) {
    %s
  }
}
""" % PRODUCT_FIELDS

LIST_PRODUCTS = """
query ListProducts($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    edges {
      cursor
      node {
        %s
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
""" % PRODUCT_LIST_FIELDS

GET_PRODUCT_BY_HANDLE = """
query GetProductByHandle($handle: String!) {
  productByHandle(handle: $handle) {
    %s
  }
}
""" % PRODUCT_FIELDS

# ---------------------------------------------------------------------------
# Collections
# ---------------------------------------------------------------------------

COLLECTION_IMAGE_FIELDS = """
  image {
    id
    url
    altText
  }
"""

COLLECTION_LIST_FIELDS = """
  id
  handle
  title
  descriptionHtml
  sortOrder
  seo {
    title
    description
  }
""" + COLLECTION_IMAGE_FIELDS

COLLECTION_FIELDS = COLLECTION_LIST_FIELDS

GET_COLLECTION = """
query GetCollection($id: ID!) {
  collection(id: $id) {
    %s
  }
}
""" % COLLECTION_FIELDS

LIST_COLLECTIONS = """
query ListCollections($first: Int!, $after: String) {
  collections(first: $first, after: $after) {
    edges {
      cursor
      node {
        %s
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
""" % COLLECTION_LIST_FIELDS

GET_COLLECTION_BY_HANDLE = """
query GetCollectionByHandle($handle: String!) {
  collectionByHandle(handle: $handle) {
    %s
  }
}
""" % COLLECTION_FIELDS

# ---------------------------------------------------------------------------
# Blogs
# ---------------------------------------------------------------------------

BLOG_LIST_FIELDS = """
  id
  handle
  title
  commentPolicy
"""

BLOG_FIELDS = BLOG_LIST_FIELDS

GET_BLOG = """
query GetBlog($id: ID!) {
  blog(id: $id) {
    %s
  }
}
""" % BLOG_FIELDS

LIST_BLOGS = """
query ListBlogs($first: Int!, $after: String) {
  blogs(first: $first, after: $after) {
    edges {
      cursor
      node {
        %s
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
""" % BLOG_LIST_FIELDS

# ---------------------------------------------------------------------------
# Articles
# ---------------------------------------------------------------------------

ARTICLE_IMAGE_FIELDS = """
  image {
    id
    url
    altText
  }
"""

ARTICLE_LIST_FIELDS = """
  id
  handle
  title
  body
  summary
  publishedAt
  isPublished
  tags
  author {
    name
  }
""" + ARTICLE_IMAGE_FIELDS

ARTICLE_FIELDS = ARTICLE_LIST_FIELDS

GET_ARTICLE = """
query GetArticle($id: ID!) {
  article(id: $id) {
    blog {
      id
    }
    %s
  }
}
""" % ARTICLE_FIELDS

LIST_ARTICLES_FOR_BLOG = """
query ListArticles($blogId: ID!, $first: Int!, $after: String) {
  blog(id: $blogId) {
    articles(first: $first, after: $after) {
      edges {
        cursor
        node {
          %s
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
""" % ARTICLE_LIST_FIELDS
