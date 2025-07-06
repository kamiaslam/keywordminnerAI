from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio
from typing import Dict, List
import re

class KeywordScraperAgent:
    def __init__(self):
        self.browser = None
        self.context = None
        
    async def _init_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
    
    async def _close_browser(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
    
    async def scrape_website(self, url: str) -> Dict:
        try:
            await self._init_browser()
            page = await self.context.new_page()
            
            await page.goto(url, wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(2000)
            
            html_content = await page.content()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            content = {
                'url': url,
                'title': '',
                'meta_description': '',
                'meta_keywords': '',
                'headings': {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []},
                'paragraphs': [],
                'links': [],
                'images_alt': []
            }
            
            title_tag = soup.find('title')
            if title_tag:
                content['title'] = title_tag.text.strip()
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                content['meta_description'] = meta_desc.get('content', '')
            
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords:
                content['meta_keywords'] = meta_keywords.get('content', '')
            
            for i in range(1, 7):
                headings = soup.find_all(f'h{i}')
                content['headings'][f'h{i}'] = [h.text.strip() for h in headings if h.text.strip()]
            
            paragraphs = soup.find_all('p')
            content['paragraphs'] = [p.text.strip() for p in paragraphs if p.text.strip() and len(p.text.strip()) > 20]
            
            links = soup.find_all('a')
            for link in links:
                link_text = link.text.strip()
                if link_text and len(link_text) > 2:
                    content['links'].append(link_text)
            
            images = soup.find_all('img')
            for img in images:
                alt_text = img.get('alt', '').strip()
                if alt_text:
                    content['images_alt'].append(alt_text)
            
            await self._close_browser()
            return content
            
        except Exception as e:
            await self._close_browser()
            raise Exception(f"Error scraping website: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s-]', '', text)
        return text.strip()