"""
GraphQL read queries for importing Shopify content into Wagtail.

Field names use the Shopify Admin API 2025-04 schema:
  - Article.body  (HTML) — NOT bodyHtml
  - Article.summary (HTML) — NOT summaryHtml
  - Blog.commentPolicy — NOT commentable
"""

# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------

PRODUCT_FIELDS = """
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
  images(first: 20) {
    edges {
      node {
        id
        url
        altText
        width
        height
      }
    }
  }
  metafields(first: 50) {
    edges {
      node {
        id
        namespace
        key
        type
        value
      }
    }
  }
"""

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
""" % PRODUCT_FIELDS

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

COLLECTION_FIELDS = """
  id
  handle
  title
  descriptionHtml
  sortOrder
  seo {
    title
    description
  }
  image {
    id
    url
    altText
    width
    height
  }
  metafields(first: 50) {
    edges {
      node {
        id
        namespace
        key
        type
        value
      }
    }
  }
"""

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
""" % COLLECTION_FIELDS

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

BLOG_FIELDS = """
  id
  handle
  title
  commentPolicy
  metafields(first: 20) {
    edges {
      node {
        id
        namespace
        key
        type
        value
      }
    }
  }
"""

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
""" % BLOG_FIELDS

# ---------------------------------------------------------------------------
# Articles
# Note: Article has no native seo field in Admin GraphQL API.
#       SEO is stored as metafields (global.title_tag / global.description_tag).
# ---------------------------------------------------------------------------

ARTICLE_FIELDS = """
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
  image {
    id
    url
    altText
    width
    height
  }
  metafields(first: 50) {
    edges {
      node {
        id
        namespace
        key
        type
        value
      }
    }
  }
"""

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
""" % ARTICLE_FIELDS
