# Dark Web Crawler

## Overview

The Dark Web Crawler is a web crawling system designed to discover and collect hidden knowledge from the internet, automatically populating the Dark Knowledge Base. Like a dark matter detector that reveals hidden cosmic structures, the Dark Crawler explores the information space to uncover valuable content.

## Philosophy

The Dark Crawler embodies the concept of discovering "dark knowledge" - information that exists but remains hidden until actively sought out. Just as dark matter can only be detected through its gravitational effects on visible matter, valuable knowledge on the web often requires active discovery and extraction.

## Features

### Core Capabilities

1. **Web Crawling**: Fetch and parse HTML content from URLs
2. **Content Extraction**: Extract text content, titles, and links from web pages
3. **Rate Limiting**: Configurable delays between requests to be respectful
4. **Robots.txt Compliance**: Optional respect for robots.txt rules
5. **Depth Control**: Configurable maximum crawl depth
6. **URL Filtering**: Filter URLs by domain or regex patterns
7. **Knowledge Base Integration**: Direct integration with DarkKnowledgeBase

### Safety Features

- User-agent identification
- Configurable request delays
- robots.txt compliance
- Maximum page limits
- Timeout handling
- Error recovery

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Seed URLs                          │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              DarkCrawler                            │
│  ┌─────────────────────────────────────────────┐   │
│  │   1. Check robots.txt (optional)            │   │
│  └─────────────────┬───────────────────────────┘   │
│                    │                                │
│                    ▼                                │
│  ┌─────────────────────────────────────────────┐   │
│  │   2. Fetch HTML Content                     │   │
│  └─────────────────┬───────────────────────────┘   │
│                    │                                │
│                    ▼                                │
│  ┌─────────────────────────────────────────────┐   │
│  │   3. Extract Text & Links                   │   │
│  │      (HTMLContentExtractor)                 │   │
│  └─────────────────┬───────────────────────────┘   │
│                    │                                │
│                    ▼                                │
│  ┌─────────────────────────────────────────────┐   │
│  │   4. Apply Filters                          │   │
│  └─────────────────┬───────────────────────────┘   │
│                    │                                │
│                    ▼                                │
│  ┌─────────────────────────────────────────────┐   │
│  │   5. Store in Knowledge Base                │   │
│  └─────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│          Dark Knowledge Base (Updated)              │
└─────────────────────────────────────────────────────┘
```

## Usage

### Basic Crawling

```python
from dark_crawler import DarkCrawler

# Create a crawler
crawler = DarkCrawler(
    user_agent="MyBot/1.0",
    delay=2.0,              # 2 seconds between requests
    max_depth=2,            # Crawl seed URLs and 2 levels deep
    max_pages=50,           # Maximum 50 pages
    respect_robots_txt=True # Respect robots.txt
)

# Crawl some URLs
seed_urls = [
    'https://example.com/articles',
    'https://example.com/blog'
]

results = crawler.crawl(seed_urls)

# Process results
for result in results:
    if result.success:
        print(f"URL: {result.url}")
        print(f"Title: {result.title}")
        print(f"Content length: {len(result.content)}")
        print(f"Links found: {len(result.links)}")
    else:
        print(f"Failed: {result.url} - {result.error}")
```

### Crawl and Store in Knowledge Base

```python
from dark_crawler import DarkCrawler
from dark_rag import DarkKnowledgeBase

# Create knowledge base
kb = DarkKnowledgeBase(storage_path="crawled_knowledge.json")

# Create crawler
crawler = DarkCrawler(
    delay=2.0,
    max_depth=1,
    max_pages=20
)

# Crawl and automatically store results
seed_urls = ['https://example.com/docs']

stats = crawler.crawl_and_store(
    seed_urls=seed_urls,
    knowledge_base=kb,
    min_content_length=200  # Only store pages with at least 200 chars
)

print(f"Crawled: {stats['total_crawled']} pages")
print(f"Stored: {stats['stored']} documents")
print(f"Skipped: {stats['skipped']} (too short)")
print(f"Errors: {stats['errors']}")
```

### URL Filtering

#### Filter by Domain

```python
from dark_crawler import DarkCrawler, create_domain_filter

crawler = DarkCrawler()

# Only crawl from specific domains
domain_filter = create_domain_filter(['example.com', 'trusted-site.org'])

results = crawler.crawl(
    seed_urls=['https://example.com'],
    filter_func=domain_filter
)
```

#### Filter by Pattern

```python
from dark_crawler import DarkCrawler, create_pattern_filter

crawler = DarkCrawler()

# Only crawl URLs matching specific patterns
pattern_filter = create_pattern_filter([
    r'/articles/',
    r'/blog/\d{4}/',  # Blog posts with year in URL
    r'/docs/.*\.html$'
])

results = crawler.crawl(
    seed_urls=['https://example.com'],
    filter_func=pattern_filter
)
```

#### Custom Filter

```python
def custom_filter(url: str) -> bool:
    """Only crawl recent articles"""
    return '/2024/' in url or '/2025/' in url

results = crawler.crawl(
    seed_urls=['https://example.com/articles'],
    filter_func=custom_filter
)
```

### Complete Workflow

```python
from dark_crawler import DarkCrawler, create_domain_filter
from dark_rag import DarkKnowledgeBase, DarkRAG

# 1. Set up crawler
crawler = DarkCrawler(
    user_agent="DarkKnowledgeBot/1.0",
    delay=2.0,
    max_depth=2,
    max_pages=100,
    respect_robots_txt=True
)

# 2. Create knowledge base
kb = DarkKnowledgeBase(storage_path="my_knowledge.json")

# 3. Set up filtering
domain_filter = create_domain_filter(['example.com'])

# 4. Crawl and store
seed_urls = [
    'https://example.com/docs',
    'https://example.com/tutorials'
]

stats = crawler.crawl_and_store(
    seed_urls=seed_urls,
    knowledge_base=kb,
    filter_func=domain_filter,
    min_content_length=200
)

print(f"Crawling complete: {stats['stored']} documents stored")

# 5. Use with Dark RAG
dark_rag = DarkRAG(knowledge_base=kb)
result = dark_rag.generate("How do I use the API?", top_k=3)
print(result['augmented_prompt'])
```

## Components

### DarkCrawler

The main crawler class that orchestrates the crawling process.

**Parameters:**
- `user_agent` (str): User agent string to identify the crawler
- `delay` (float): Delay between requests in seconds (default: 1.0)
- `max_depth` (int): Maximum crawl depth from seed URLs (default: 2)
- `max_pages` (int): Maximum number of pages to crawl (default: 100)
- `respect_robots_txt` (bool): Whether to respect robots.txt (default: True)

**Methods:**
- `crawl(seed_urls, filter_func=None)`: Crawl URLs and return results
- `crawl_and_store(seed_urls, knowledge_base, filter_func=None, min_content_length=100)`: Crawl and store directly in knowledge base
- `can_fetch(url)`: Check if URL can be fetched according to robots.txt
- `crawl_url(url)`: Crawl a single URL

### CrawlResult

Data structure representing the result of crawling a single URL.

**Attributes:**
- `url` (str): The crawled URL
- `content` (str): Extracted text content
- `title` (str): Page title
- `metadata` (dict): Additional metadata
- `links` (list): List of discovered URLs
- `success` (bool): Whether crawl was successful
- `error` (str): Error message if failed

### HTMLContentExtractor

HTML parser that extracts text content and links.

**Methods:**
- `get_content()`: Get extracted text content
- `get_links()`: Get extracted links

### Filter Functions

Helper functions to create URL filters:

- `create_domain_filter(allowed_domains)`: Filter by domain
- `create_pattern_filter(patterns)`: Filter by regex patterns

## Best Practices

### 1. Be Respectful

Always use appropriate delays and respect robots.txt:

```python
crawler = DarkCrawler(
    delay=2.0,              # At least 2 seconds between requests
    respect_robots_txt=True # Respect website policies
)
```

### 2. Identify Your Crawler

Use a descriptive user agent:

```python
crawler = DarkCrawler(
    user_agent="MyProjectBot/1.0 (+https://mysite.com/bot-info)"
)
```

### 3. Limit Scope

Use appropriate limits to avoid overwhelming sites:

```python
crawler = DarkCrawler(
    max_depth=2,   # Don't go too deep
    max_pages=100  # Limit total pages
)
```

### 4. Filter Content

Only store quality content:

```python
stats = crawler.crawl_and_store(
    seed_urls=urls,
    knowledge_base=kb,
    min_content_length=200  # Skip thin content
)
```

### 5. Use Domain Filtering

Limit crawling to specific domains:

```python
domain_filter = create_domain_filter(['example.com'])
results = crawler.crawl(seed_urls, filter_func=domain_filter)
```

## Configuration Examples

### Conservative Crawler

For careful, slow crawling:

```python
crawler = DarkCrawler(
    delay=5.0,              # 5 seconds between requests
    max_depth=1,            # Only seed URLs and direct links
    max_pages=20,           # Very limited
    respect_robots_txt=True
)
```

### Aggressive Crawler

For faster crawling (use responsibly):

```python
crawler = DarkCrawler(
    delay=1.0,              # 1 second between requests
    max_depth=3,            # Deeper crawling
    max_pages=500,          # More pages
    respect_robots_txt=True # Still respect robots.txt
)
```

### Documentation Crawler

Optimized for documentation sites:

```python
crawler = DarkCrawler(
    delay=1.5,
    max_depth=4,            # Documentation tends to be nested
    max_pages=200
)

pattern_filter = create_pattern_filter([
    r'/docs/',
    r'/guides/',
    r'/tutorials/',
    r'/reference/'
])
```

## Limitations

1. **Text Only**: Currently only extracts text content (no images, videos, etc.)
2. **HTML Only**: Only processes HTML content, not PDFs or other formats
3. **No JavaScript**: Cannot execute JavaScript to render dynamic content
4. **No Authentication**: Cannot crawl password-protected content
5. **No Session State**: Each request is independent

## Future Enhancements

1. **JavaScript Rendering**: Support for dynamic content (e.g., using Playwright)
2. **Multi-format Support**: PDF, Word documents, etc.
3. **Authentication**: Support for login-protected content
4. **Distributed Crawling**: Parallel crawling across multiple workers
5. **Content Deduplication**: Detect and skip duplicate content
6. **Smart Recrawling**: Track and update changed content
7. **Language Detection**: Filter or tag content by language
8. **Topic Classification**: Automatically categorize crawled content

## Integration with Dark RAG

The crawler seamlessly integrates with the Dark RAG system:

```python
# 1. Crawl content
crawler = DarkCrawler()
kb = DarkKnowledgeBase()

crawler.crawl_and_store(
    seed_urls=['https://docs.example.com'],
    knowledge_base=kb
)

# 2. Use with Dark RAG
from dark_rag import DarkRAG

dark_rag = DarkRAG(knowledge_base=kb)

# 3. Query with augmented context
result = dark_rag.generate("How do I configure the API?")
print(result['augmented_prompt'])
```

## Security Considerations

1. **URL Validation**: Always validate URLs before crawling
2. **Content Size Limits**: Set reasonable limits to prevent memory issues
3. **Timeout Handling**: Requests have 10-second timeouts
4. **Error Recovery**: Graceful handling of network errors
5. **Rate Limiting**: Built-in delay between requests

## Example: Building a Documentation Knowledge Base

```python
from dark_crawler import DarkCrawler, create_domain_filter
from dark_rag import DarkKnowledgeBase, DarkRAG

# Configure crawler for documentation
crawler = DarkCrawler(
    user_agent="DocBot/1.0",
    delay=1.5,
    max_depth=3,
    max_pages=200
)

# Create knowledge base
kb = DarkKnowledgeBase(storage_path="docs_knowledge.json")

# Set up domain filter
domain_filter = create_domain_filter(['docs.python.org'])

# Crawl Python documentation
stats = crawler.crawl_and_store(
    seed_urls=['https://docs.python.org/3/tutorial/'],
    knowledge_base=kb,
    filter_func=domain_filter,
    min_content_length=300
)

print(f"Built documentation KB with {stats['stored']} documents")

# Use for Q&A
dark_rag = DarkRAG(knowledge_base=kb)
result = dark_rag.generate("How do I use list comprehensions?")
print(result['augmented_prompt'])
```

## License

This implementation follows the repository's license.
