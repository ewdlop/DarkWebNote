#!/usr/bin/env python3
"""
Example usage of Dark Web Crawler

This script demonstrates various use cases of the Dark Crawler system.
Note: These examples use mock/demonstration URLs for safety.
"""

from dark_crawler import (
    DarkCrawler, 
    create_domain_filter, 
    create_pattern_filter
)
from dark_rag import DarkKnowledgeBase, DarkRAG


def example_1_basic_crawling():
    """Example 1: Basic crawling (without actual network calls)"""
    print("=" * 70)
    print("Example 1: Basic Crawler Setup")
    print("=" * 70)
    
    # Create a crawler with conservative settings
    crawler = DarkCrawler(
        user_agent="DarkCrawlerExample/1.0",
        delay=2.0,              # 2 seconds between requests
        max_depth=2,            # Crawl 2 levels deep
        max_pages=10,           # Limit to 10 pages
        respect_robots_txt=True
    )
    
    print("\nCrawler Configuration:")
    print(f"  User Agent: {crawler.user_agent}")
    print(f"  Delay: {crawler.delay}s")
    print(f"  Max Depth: {crawler.max_depth}")
    print(f"  Max Pages: {crawler.max_pages}")
    print(f"  Respects robots.txt: {crawler.respect_robots_txt}")
    
    print("\nNote: To actually crawl URLs, use:")
    print("  results = crawler.crawl(['https://example.com'])")
    print("  This example avoids network calls for safety.")


def example_2_domain_filtering():
    """Example 2: Using domain filters"""
    print("\n" + "=" * 70)
    print("Example 2: Domain Filtering")
    print("=" * 70)
    
    # Create domain filter
    allowed_domains = ['example.com', 'docs.example.com']
    domain_filter = create_domain_filter(allowed_domains)
    
    # Test the filter
    test_urls = [
        'https://example.com/page1',
        'https://docs.example.com/guide',
        'https://www.example.com/blog',
        'https://other-site.com/page',
        'https://notexample.com/page'
    ]
    
    print(f"\nAllowed domains: {allowed_domains}")
    print("\nTesting URLs:")
    for url in test_urls:
        allowed = domain_filter(url)
        status = "✓ ALLOWED" if allowed else "✗ BLOCKED"
        print(f"  {status}: {url}")
    
    print("\nUsage with crawler:")
    print("  crawler.crawl(seed_urls, filter_func=domain_filter)")


def example_3_pattern_filtering():
    """Example 3: Using pattern filters"""
    print("\n" + "=" * 70)
    print("Example 3: Pattern Filtering")
    print("=" * 70)
    
    # Create pattern filter for specific URL patterns
    patterns = [
        r'/articles/.*',      # Any URL with /articles/
        r'/blog/\d{4}/',      # Blog posts with year
        r'/docs/.*\.html$'    # HTML docs
    ]
    pattern_filter = create_pattern_filter(patterns)
    
    # Test the filter
    test_urls = [
        'https://example.com/articles/python-guide',
        'https://example.com/blog/2024/post',
        'https://example.com/docs/api.html',
        'https://example.com/about',
        'https://example.com/contact'
    ]
    
    print(f"\nPattern filters: {patterns}")
    print("\nTesting URLs:")
    for url in test_urls:
        allowed = pattern_filter(url)
        status = "✓ MATCH" if allowed else "✗ NO MATCH"
        print(f"  {status}: {url}")


def example_4_custom_filter():
    """Example 4: Custom filter function"""
    print("\n" + "=" * 70)
    print("Example 4: Custom Filter Function")
    print("=" * 70)
    
    # Custom filter: only 2024 and 2025 content
    def recent_content_filter(url: str) -> bool:
        """Only crawl recent articles from 2024-2025"""
        return '/2024/' in url or '/2025/' in url
    
    # Test the filter
    test_urls = [
        'https://example.com/blog/2024/article',
        'https://example.com/blog/2025/post',
        'https://example.com/blog/2023/old-post',
        'https://example.com/archive/2020/article'
    ]
    
    print("\nCustom filter: Only 2024-2025 content")
    print("\nTesting URLs:")
    for url in test_urls:
        allowed = recent_content_filter(url)
        status = "✓ RECENT" if allowed else "✗ OLD"
        print(f"  {status}: {url}")
    
    print("\nUsage with crawler:")
    print("  crawler.crawl(seed_urls, filter_func=recent_content_filter)")


def example_5_knowledge_base_integration():
    """Example 5: Integration with Knowledge Base"""
    print("\n" + "=" * 70)
    print("Example 5: Knowledge Base Integration")
    print("=" * 70)
    
    print("\nThis example demonstrates the complete workflow:")
    print("\n1. Create a crawler:")
    print("   crawler = DarkCrawler(delay=2.0, max_depth=2, max_pages=50)")
    
    print("\n2. Create a knowledge base:")
    print("   kb = DarkKnowledgeBase(storage_path='crawled_kb.json')")
    
    print("\n3. Crawl and store:")
    print("   stats = crawler.crawl_and_store(")
    print("       seed_urls=['https://example.com/docs'],")
    print("       knowledge_base=kb,")
    print("       min_content_length=200")
    print("   )")
    
    print("\n4. Results:")
    print("   - Total crawled: stats['total_crawled']")
    print("   - Stored: stats['stored']")
    print("   - Skipped: stats['skipped']")
    print("   - Errors: stats['errors']")
    
    print("\n5. Use with Dark RAG:")
    print("   dark_rag = DarkRAG(knowledge_base=kb)")
    print("   result = dark_rag.generate('How does it work?')")


def example_6_different_crawler_configs():
    """Example 6: Different crawler configurations"""
    print("\n" + "=" * 70)
    print("Example 6: Different Crawler Configurations")
    print("=" * 70)
    
    print("\nConservative (Safe, Slow):")
    conservative = DarkCrawler(
        delay=5.0,
        max_depth=1,
        max_pages=20,
        respect_robots_txt=True
    )
    print(f"  - Delay: {conservative.delay}s (very respectful)")
    print(f"  - Max Depth: {conservative.max_depth} (shallow)")
    print(f"  - Max Pages: {conservative.max_pages} (limited)")
    
    print("\nBalanced (Recommended):")
    balanced = DarkCrawler(
        delay=2.0,
        max_depth=2,
        max_pages=100,
        respect_robots_txt=True
    )
    print(f"  - Delay: {balanced.delay}s (respectful)")
    print(f"  - Max Depth: {balanced.max_depth} (moderate)")
    print(f"  - Max Pages: {balanced.max_pages} (reasonable)")
    
    print("\nAggressive (Fast, Use Responsibly):")
    aggressive = DarkCrawler(
        delay=1.0,
        max_depth=3,
        max_pages=500,
        respect_robots_txt=True
    )
    print(f"  - Delay: {aggressive.delay}s (faster)")
    print(f"  - Max Depth: {aggressive.max_depth} (deeper)")
    print(f"  - Max Pages: {aggressive.max_pages} (many pages)")


def example_7_documentation_crawler():
    """Example 7: Specialized documentation crawler"""
    print("\n" + "=" * 70)
    print("Example 7: Documentation Crawler Pattern")
    print("=" * 70)
    
    print("\nOptimized for crawling documentation sites:")
    
    # Configure for documentation
    crawler = DarkCrawler(
        user_agent="DocCrawler/1.0",
        delay=1.5,
        max_depth=4,    # Docs tend to be nested
        max_pages=200
    )
    
    # Pattern for documentation URLs
    doc_patterns = [
        r'/docs/',
        r'/documentation/',
        r'/guides/',
        r'/tutorials/',
        r'/reference/',
        r'/api/'
    ]
    doc_filter = create_pattern_filter(doc_patterns)
    
    print(f"\nCrawler settings:")
    print(f"  - Max Depth: {crawler.max_depth} (docs are nested)")
    print(f"  - Max Pages: {crawler.max_pages}")
    
    print(f"\nPattern filters: {doc_patterns}")
    
    print("\nExample usage:")
    print("  seed_urls = ['https://docs.python.org/3/']")
    print("  stats = crawler.crawl_and_store(")
    print("      seed_urls=seed_urls,")
    print("      knowledge_base=kb,")
    print("      filter_func=doc_filter,")
    print("      min_content_length=300  # Docs usually have substantial content")
    print("  )")


def example_8_combining_filters():
    """Example 8: Combining multiple filters"""
    print("\n" + "=" * 70)
    print("Example 8: Combining Multiple Filters")
    print("=" * 70)
    
    # Create individual filters
    domain_filter = create_domain_filter(['docs.example.com'])
    pattern_filter = create_pattern_filter([r'/tutorials/', r'/guides/'])
    
    # Combine filters
    def combined_filter(url: str) -> bool:
        """URL must pass both domain AND pattern filters"""
        return domain_filter(url) and pattern_filter(url)
    
    # Test URLs
    test_urls = [
        'https://docs.example.com/tutorials/python',  # Pass both
        'https://docs.example.com/guides/django',     # Pass both
        'https://docs.example.com/reference/api',     # Domain OK, pattern fail
        'https://other.com/tutorials/rust',           # Domain fail, pattern OK
        'https://other.com/contact'                   # Both fail
    ]
    
    print("\nCombined filter: Must be from docs.example.com AND match /tutorials/ or /guides/")
    print("\nTesting URLs:")
    for url in test_urls:
        allowed = combined_filter(url)
        status = "✓ PASS" if allowed else "✗ FAIL"
        print(f"  {status}: {url}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "DARK CRAWLER EXAMPLES" + " " * 29 + "║")
    print("╚" + "═" * 68 + "╝")
    
    example_1_basic_crawling()
    example_2_domain_filtering()
    example_3_pattern_filtering()
    example_4_custom_filter()
    example_5_knowledge_base_integration()
    example_6_different_crawler_configs()
    example_7_documentation_crawler()
    example_8_combining_filters()
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Read DARK_CRAWLER.md for detailed documentation")
    print("  2. Configure a crawler for your use case")
    print("  3. Set up appropriate filters")
    print("  4. Crawl and build your knowledge base")
    print("  5. Use with Dark RAG for augmented generation")
    print("\nImportant:")
    print("  - Always be respectful when crawling (use delays, respect robots.txt)")
    print("  - Test filters before running large crawls")
    print("  - Monitor your crawling behavior")
    print()


if __name__ == "__main__":
    main()
