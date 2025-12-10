"""
Tests for Dark Web Crawler
"""

import os
import tempfile
from dark_crawler import (
    DarkCrawler, 
    CrawlResult, 
    HTMLContentExtractor,
    create_domain_filter,
    create_pattern_filter
)
from dark_rag import DarkKnowledgeBase


def test_html_content_extractor():
    """Test HTML content extraction"""
    html = """
    <html>
    <head>
        <title>Test Page</title>
        <style>body { color: red; }</style>
    </head>
    <body>
        <h1>Welcome</h1>
        <p>This is a test page.</p>
        <a href="/page1">Link 1</a>
        <a href="https://example.com/page2">Link 2</a>
        <script>console.log('test');</script>
    </body>
    </html>
    """
    
    parser = HTMLContentExtractor()
    parser.feed(html)
    
    content = parser.get_content()
    assert "Welcome" in content
    assert "This is a test page" in content
    assert "console.log" not in content  # Script content should be excluded
    
    assert parser.title == "Test Page"
    
    links = parser.get_links()
    assert len(links) == 2
    assert "/page1" in links
    assert "https://example.com/page2" in links
    
    print("✓ HTML content extractor test passed")


def test_dark_crawler_initialization():
    """Test DarkCrawler initialization"""
    crawler = DarkCrawler(
        user_agent="TestBot/1.0",
        delay=0.5,
        max_depth=3,
        max_pages=50,
        respect_robots_txt=False
    )
    
    assert crawler.user_agent == "TestBot/1.0"
    assert crawler.delay == 0.5
    assert crawler.max_depth == 3
    assert crawler.max_pages == 50
    assert crawler.respect_robots_txt == False
    assert len(crawler.visited_urls) == 0
    
    print("✓ DarkCrawler initialization test passed")


def test_crawl_result():
    """Test CrawlResult data structure"""
    result = CrawlResult(
        url="https://example.com",
        content="Test content",
        title="Test Title",
        metadata={'key': 'value'},
        links=["https://example.com/page1"],
        success=True
    )
    
    assert result.url == "https://example.com"
    assert result.content == "Test content"
    assert result.title == "Test Title"
    assert result.metadata['key'] == 'value'
    assert len(result.links) == 1
    assert result.success == True
    assert result.error is None
    
    # Test failed result
    failed_result = CrawlResult(
        url="https://fail.com",
        content="",
        title=None,
        metadata={},
        links=[],
        success=False,
        error="Connection failed"
    )
    
    assert failed_result.success == False
    assert failed_result.error == "Connection failed"
    
    print("✓ CrawlResult test passed")


def test_extract_content():
    """Test content extraction from HTML"""
    crawler = DarkCrawler()
    
    html = """
    <html>
    <head><title>My Page</title></head>
    <body>
        <h1>Header</h1>
        <p>Paragraph 1</p>
        <p>Paragraph 2</p>
        <a href="/link1">Link</a>
        <a href="http://external.com/page">External</a>
    </body>
    </html>
    """
    
    base_url = "http://example.com/page"
    content, title, links = crawler.extract_content(html, base_url)
    
    assert "Header" in content
    assert "Paragraph 1" in content
    assert "Paragraph 2" in content
    assert title == "My Page"
    
    # Links should be absolute URLs
    assert any("example.com/link1" in link for link in links)
    assert any("external.com/page" in link for link in links)
    
    print("✓ Content extraction test passed")


def test_domain_filter():
    """Test domain filter function"""
    filter_func = create_domain_filter(['example.com', 'test.org'])
    
    assert filter_func('https://example.com/page') == True
    assert filter_func('https://www.example.com/page') == True
    assert filter_func('https://test.org/page') == True
    assert filter_func('https://other.com/page') == False
    assert filter_func('https://notexample.com/page') == False
    
    print("✓ Domain filter test passed")


def test_pattern_filter():
    """Test pattern filter function"""
    filter_func = create_pattern_filter([r'/articles/', r'/blog/'])
    
    assert filter_func('https://example.com/articles/123') == True
    assert filter_func('https://example.com/blog/post') == True
    assert filter_func('https://example.com/about') == False
    assert filter_func('https://example.com/contact') == False
    
    print("✓ Pattern filter test passed")


def test_crawler_visited_tracking():
    """Test that crawler tracks visited URLs"""
    crawler = DarkCrawler(delay=0.1, max_pages=5)
    
    # Initially empty
    assert len(crawler.visited_urls) == 0
    
    # Simulate crawling (without actual network calls)
    # We'll test the visited_urls set directly
    crawler.visited_urls.add('https://example.com/page1')
    crawler.visited_urls.add('https://example.com/page2')
    
    assert len(crawler.visited_urls) == 2
    assert 'https://example.com/page1' in crawler.visited_urls
    assert 'https://example.com/page2' in crawler.visited_urls
    
    print("✓ Crawler visited tracking test passed")


def test_crawl_and_store_integration():
    """Test integration with DarkKnowledgeBase"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        # Create knowledge base
        kb = DarkKnowledgeBase(storage_path=temp_path)
        
        # Create a mock crawler result manually
        # (We won't actually crawl URLs in tests to avoid network dependencies)
        test_content = "This is test content about dark web crawling and knowledge extraction."
        result = CrawlResult(
            url="https://example.com/test",
            content=test_content,
            title="Test Page",
            metadata={
                'url': 'https://example.com/test',
                'title': 'Test Page',
                'crawled_at': 1234567890,
                'content_length': len(test_content),
                'num_links': 0
            },
            links=[],
            success=True
        )
        
        # Manually add to knowledge base (simulating what crawl_and_store would do)
        if result.success and len(result.content) >= 100:
            metadata = result.metadata.copy()
            metadata['source'] = 'dark_crawler'
            metadata['crawl_url'] = result.url
            
            kb.add_document(
                content=result.content,
                metadata=metadata
            )
        
        # For this test, content is less than 100 chars, so it won't be added
        # Let's create a longer content result
        long_content = "This is a much longer piece of content about dark web crawling. " * 5
        long_result = CrawlResult(
            url="https://example.com/long",
            content=long_content,
            title="Long Test Page",
            metadata={
                'url': 'https://example.com/long',
                'title': 'Long Test Page',
                'crawled_at': 1234567890,
                'content_length': len(long_content),
                'num_links': 2
            },
            links=[],
            success=True
        )
        
        metadata = long_result.metadata.copy()
        metadata['source'] = 'dark_crawler'
        metadata['crawl_url'] = long_result.url
        
        kb.add_document(
            content=long_result.content,
            metadata=metadata
        )
        
        # Verify document was added
        assert len(kb.documents) == 1
        
        # Verify we can retrieve it
        docs = kb.retrieve("dark web crawling", top_k=1)
        assert len(docs) > 0
        assert "dark web crawling" in docs[0].content.lower()
        
        # Save and reload
        kb.save()
        kb2 = DarkKnowledgeBase(storage_path=temp_path)
        assert len(kb2.documents) == 1
        
        print("✓ Crawl and store integration test passed")
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_can_fetch_no_robots():
    """Test can_fetch when robots.txt is not required"""
    crawler = DarkCrawler(respect_robots_txt=False)
    
    # Should always return True when robots.txt is not respected
    assert crawler.can_fetch("https://example.com/page") == True
    assert crawler.can_fetch("https://test.com/admin") == True
    
    print("✓ Can fetch (no robots) test passed")


def test_empty_html_extraction():
    """Test extraction from empty or malformed HTML"""
    crawler = DarkCrawler()
    
    # Empty HTML
    content, title, links = crawler.extract_content("", "http://example.com")
    assert content == ""
    assert title is None
    assert links == []
    
    # Malformed HTML
    content, title, links = crawler.extract_content("<html><bod", "http://example.com")
    # Should handle gracefully without crashing
    assert isinstance(content, str)
    assert isinstance(links, list)
    
    print("✓ Empty HTML extraction test passed")


if __name__ == "__main__":
    print("Running Dark Crawler Tests...\n")
    
    test_html_content_extractor()
    test_dark_crawler_initialization()
    test_crawl_result()
    test_extract_content()
    test_domain_filter()
    test_pattern_filter()
    test_crawler_visited_tracking()
    test_crawl_and_store_integration()
    test_can_fetch_no_robots()
    test_empty_html_extraction()
    
    print("\n" + "=" * 50)
    print("All crawler tests passed! ✓")
    print("=" * 50)
