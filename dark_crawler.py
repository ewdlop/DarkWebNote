"""
Dark Web Crawler - A crawler system for collecting and indexing web content
Themed around the Dark Web metaphor of discovering hidden knowledge
"""

import re
import time
import hashlib
from typing import List, Dict, Any, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.robotparser import RobotFileParser
from html.parser import HTMLParser
from dataclasses import dataclass


@dataclass
class CrawlResult:
    """Represents the result of crawling a single URL"""
    url: str
    content: str
    title: Optional[str]
    metadata: Dict[str, Any]
    links: List[str]
    success: bool
    error: Optional[str] = None


class HTMLContentExtractor(HTMLParser):
    """Extract text content and links from HTML"""
    
    def __init__(self):
        super().__init__()
        self.title = None
        self.text_content = []
        self.links = []
        self.in_script = False
        self.in_style = False
        self.in_title = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.in_script = True
        elif tag == 'style':
            self.in_style = True
        elif tag == 'title':
            self.in_title = True
        elif tag == 'a':
            for attr, value in attrs:
                if attr == 'href' and value:
                    self.links.append(value)
    
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
        elif tag == 'title':
            self.in_title = False
    
    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
        elif not self.in_script and not self.in_style:
            text = data.strip()
            if text:
                self.text_content.append(text)
    
    def get_content(self) -> str:
        """Get extracted text content"""
        return ' '.join(self.text_content)
    
    def get_links(self) -> List[str]:
        """Get extracted links"""
        return self.links


class DarkCrawler:
    """
    Dark Web Crawler - Discovers and indexes hidden knowledge
    
    Like a dark matter detector, this crawler explores the information space
    to find and collect knowledge for the Dark Knowledge Base.
    """
    
    def __init__(
        self,
        user_agent: str = "DarkWebCrawler/1.0",
        delay: float = 1.0,
        max_depth: int = 2,
        max_pages: int = 100,
        respect_robots_txt: bool = True
    ):
        """
        Initialize the Dark Crawler
        
        Args:
            user_agent: User agent string to identify the crawler
            delay: Delay between requests in seconds (for rate limiting)
            max_depth: Maximum crawl depth from seed URLs
            max_pages: Maximum number of pages to crawl
            respect_robots_txt: Whether to respect robots.txt
        """
        self.user_agent = user_agent
        self.delay = delay
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.respect_robots_txt = respect_robots_txt
        self.visited_urls: Set[str] = set()
        self.robots_parsers: Dict[str, RobotFileParser] = {}
    
    def can_fetch(self, url: str) -> bool:
        """Check if URL can be fetched according to robots.txt"""
        if not self.respect_robots_txt:
            return True
        
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        if base_url not in self.robots_parsers:
            robots_url = urljoin(base_url, '/robots.txt')
            rp = RobotFileParser()
            rp.set_url(robots_url)
            try:
                rp.read()
                self.robots_parsers[base_url] = rp
            except Exception:
                # If robots.txt cannot be fetched, allow crawling
                self.robots_parsers[base_url] = None
        
        rp = self.robots_parsers[base_url]
        if rp is None:
            return True
        
        return rp.can_fetch(self.user_agent, url)
    
    def fetch_url(self, url: str) -> Optional[str]:
        """Fetch content from a URL"""
        if not self.can_fetch(url):
            return None
        
        try:
            req = Request(url, headers={'User-Agent': self.user_agent})
            with urlopen(req, timeout=10) as response:
                # Only process text/html content
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' not in content_type:
                    return None
                
                return response.read().decode('utf-8', errors='ignore')
        except (URLError, HTTPError, Exception):
            return None
    
    def extract_content(self, html: str, base_url: str) -> Tuple[str, Optional[str], List[str]]:
        """
        Extract text content, title, and links from HTML
        
        Returns:
            Tuple of (content, title, links)
        """
        parser = HTMLContentExtractor()
        try:
            parser.feed(html)
        except Exception:
            pass
        
        content = parser.get_content()
        title = parser.title
        links = parser.get_links()
        
        # Normalize links to absolute URLs
        absolute_links = []
        for link in links:
            try:
                absolute_url = urljoin(base_url, link)
                # Only include http/https links
                if absolute_url.startswith(('http://', 'https://')):
                    absolute_links.append(absolute_url)
            except Exception:
                continue
        
        return content, title, absolute_links
    
    def crawl_url(self, url: str) -> CrawlResult:
        """Crawl a single URL and extract content"""
        try:
            # Fetch the page
            html = self.fetch_url(url)
            if html is None:
                return CrawlResult(
                    url=url,
                    content="",
                    title=None,
                    metadata={},
                    links=[],
                    success=False,
                    error="Failed to fetch or not allowed"
                )
            
            # Extract content
            content, title, links = self.extract_content(html, url)
            
            # Create metadata
            metadata = {
                'url': url,
                'title': title,
                'crawled_at': time.time(),
                'content_length': len(content),
                'num_links': len(links)
            }
            
            return CrawlResult(
                url=url,
                content=content,
                title=title,
                metadata=metadata,
                links=links,
                success=True
            )
        
        except Exception as e:
            return CrawlResult(
                url=url,
                content="",
                title=None,
                metadata={},
                links=[],
                success=False,
                error=str(e)
            )
    
    def crawl(
        self,
        seed_urls: List[str],
        filter_func: Optional[callable] = None
    ) -> List[CrawlResult]:
        """
        Crawl starting from seed URLs
        
        Args:
            seed_urls: List of starting URLs
            filter_func: Optional function to filter which URLs to crawl
                         Should return True to crawl, False to skip
        
        Returns:
            List of CrawlResult objects
        """
        results = []
        queue = [(url, 0) for url in seed_urls]  # (url, depth)
        
        while queue and len(results) < self.max_pages:
            url, depth = queue.pop(0)
            
            # Skip if already visited
            if url in self.visited_urls:
                continue
            
            # Skip if depth exceeded
            if depth > self.max_depth:
                continue
            
            # Skip if filter function returns False
            if filter_func and not filter_func(url):
                continue
            
            # Mark as visited
            self.visited_urls.add(url)
            
            # Crawl the URL
            result = self.crawl_url(url)
            results.append(result)
            
            # Add discovered links to queue if crawl was successful
            if result.success and depth < self.max_depth:
                for link in result.links:
                    if link not in self.visited_urls:
                        queue.append((link, depth + 1))
            
            # Rate limiting
            if queue:  # Only delay if there are more URLs to process
                time.sleep(self.delay)
        
        return results
    
    def crawl_and_store(
        self,
        seed_urls: List[str],
        knowledge_base: Any,
        filter_func: Optional[callable] = None,
        min_content_length: int = 100
    ) -> Dict[str, Any]:
        """
        Crawl and directly store results in a Dark Knowledge Base
        
        Args:
            seed_urls: List of starting URLs
            knowledge_base: DarkKnowledgeBase instance to store results
            filter_func: Optional function to filter which URLs to crawl
            min_content_length: Minimum content length to store (filters out thin content)
        
        Returns:
            Dictionary with crawl statistics
        """
        results = self.crawl(seed_urls, filter_func)
        
        stored_count = 0
        skipped_count = 0
        error_count = 0
        
        for result in results:
            if not result.success:
                error_count += 1
                continue
            
            if len(result.content) < min_content_length:
                skipped_count += 1
                continue
            
            # Store in knowledge base
            metadata = result.metadata.copy()
            metadata['source'] = 'dark_crawler'
            metadata['crawl_url'] = result.url
            
            knowledge_base.add_document(
                content=result.content,
                metadata=metadata
            )
            stored_count += 1
        
        # Save the knowledge base
        knowledge_base.save()
        
        return {
            'total_crawled': len(results),
            'stored': stored_count,
            'skipped': skipped_count,
            'errors': error_count,
            'visited_urls': len(self.visited_urls)
        }


def create_domain_filter(allowed_domains: List[str]) -> callable:
    """
    Create a filter function that only allows URLs from specific domains
    
    Args:
        allowed_domains: List of allowed domains (e.g., ['example.com', 'test.com'])
    
    Returns:
        Filter function that returns True if URL is from allowed domain
    """
    def filter_func(url: str) -> bool:
        parsed = urlparse(url)
        netloc = parsed.netloc
        return any(
            netloc == domain or netloc.endswith('.' + domain)
            for domain in allowed_domains
        )
    
    return filter_func


def create_pattern_filter(patterns: List[str]) -> callable:
    """
    Create a filter function that only allows URLs matching regex patterns
    
    Args:
        patterns: List of regex patterns
    
    Returns:
        Filter function that returns True if URL matches any pattern
    """
    compiled_patterns = [re.compile(pattern) for pattern in patterns]
    
    def filter_func(url: str) -> bool:
        return any(pattern.search(url) for pattern in compiled_patterns)
    
    return filter_func


if __name__ == "__main__":
    # Example usage
    print("=== Dark Web Crawler ===\n")
    print("This is a demonstration of the Dark Crawler.")
    print("For actual usage, import and use the DarkCrawler class.\n")
    
    # Create a crawler instance
    crawler = DarkCrawler(
        delay=2.0,  # 2 second delay between requests
        max_depth=1,  # Only crawl seed URLs and their immediate links
        max_pages=5   # Limit to 5 pages for demo
    )
    
    print(f"Crawler configured:")
    print(f"  Max depth: {crawler.max_depth}")
    print(f"  Max pages: {crawler.max_pages}")
    print(f"  Delay: {crawler.delay}s")
    print(f"  Respects robots.txt: {crawler.respect_robots_txt}")
    print("\nUse crawler.crawl(urls) to start crawling.")
