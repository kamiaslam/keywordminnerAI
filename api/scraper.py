import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from typing import List, Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import ssl

# Download required NLTK data
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class WebsiteScraper:
    def __init__(self):
        self.stop_words = set(stopwords.words('english')) if 'stopwords' in dir(stopwords) else set()
        # Add common web-related stop words
        self.stop_words.update(['click', 'here', 'more', 'read', 'view', 'see', 'new', 'home', 'page', 'site', 'web'])
        
    def scrape_website(self, url: str) -> Dict:
        """Scrape website and extract content"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.find('title').text if soup.find('title') else ''
            
            # Extract meta description
            meta_desc = ''
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag:
                meta_desc = meta_tag.get('content', '')
            
            # Extract meta keywords
            meta_keywords = ''
            meta_keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords_tag:
                meta_keywords = meta_keywords_tag.get('content', '')
            
            # Extract all text content
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Extract headings
            headings = []
            for tag in ['h1', 'h2', 'h3']:
                headings.extend([h.text.strip() for h in soup.find_all(tag)])
            
            # Extract links text
            links_text = [a.text.strip() for a in soup.find_all('a') if a.text.strip()]
            
            return {
                'title': title,
                'meta_description': meta_desc,
                'meta_keywords': meta_keywords,
                'content': text,
                'headings': headings,
                'links_text': links_text,
                'url': url
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def extract_keywords(self, content: Dict) -> List[Dict]:
        """Extract keywords from scraped content"""
        if not content:
            return []
        
        # Combine all text sources
        all_text = ' '.join([
            content.get('title', ''),
            content.get('meta_description', ''),
            content.get('meta_keywords', ''),
            ' '.join(content.get('headings', [])),
            content.get('content', '')
        ])
        
        # Clean and tokenize
        all_text = re.sub(r'[^a-zA-Z\s]', ' ', all_text.lower())
        words = word_tokenize(all_text)
        
        # Filter out stop words and short words
        meaningful_words = [w for w in words if w not in self.stop_words and len(w) > 2]
        
        # Count word frequency
        word_freq = Counter(meaningful_words)
        
        # Extract phrases (2-3 word combinations)
        phrases = self.extract_phrases(all_text)
        
        # Combine single words and phrases
        keywords = []
        
        # Add top single words
        for word, count in word_freq.most_common(30):
            keywords.append({
                'keyword': word,
                'count': count,
                'type': 'single'
            })
        
        # Add top phrases
        for phrase, count in phrases.most_common(20):
            keywords.append({
                'keyword': phrase,
                'count': count,
                'type': 'phrase'
            })
        
        return keywords
    
    def extract_phrases(self, text: str) -> Counter:
        """Extract 2-3 word phrases"""
        words = text.lower().split()
        phrases = []
        
        # 2-word phrases
        for i in range(len(words) - 1):
            if words[i] not in self.stop_words and words[i+1] not in self.stop_words:
                phrase = f"{words[i]} {words[i+1]}"
                if len(words[i]) > 2 and len(words[i+1]) > 2:
                    phrases.append(phrase)
        
        # 3-word phrases
        for i in range(len(words) - 2):
            if (words[i] not in self.stop_words and 
                words[i+2] not in self.stop_words and
                len(words[i]) > 2 and len(words[i+2]) > 2):
                phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                phrases.append(phrase)
        
        return Counter(phrases)
    
    def generate_keyword_suggestions(self, domain: str, extracted_keywords: List[Dict]) -> Dict:
        """Generate keyword suggestions based on extracted content"""
        domain_name = domain.split('.')[0]
        
        # Get top keywords
        top_keywords = [kw['keyword'] for kw in sorted(extracted_keywords, key=lambda x: x['count'], reverse=True)[:10]]
        
        # Generate long-tail suggestions
        long_tail_suggestions = []
        
        # Question-based long-tails
        question_prefixes = ['how to', 'what is', 'why use', 'when to', 'where to find', 'best way to']
        for keyword in top_keywords[:5]:
            for prefix in question_prefixes:
                long_tail_suggestions.append(f"{prefix} {keyword}")
        
        # Action-based long-tails
        action_prefixes = ['learn', 'master', 'improve', 'optimize', 'enhance']
        for keyword in top_keywords[:5]:
            for prefix in action_prefixes:
                long_tail_suggestions.append(f"{prefix} {keyword} skills")
        
        # Comparison long-tails
        for i, keyword in enumerate(top_keywords[:3]):
            if i < len(top_keywords) - 1:
                long_tail_suggestions.append(f"{keyword} vs {top_keywords[i+1]}")
                long_tail_suggestions.append(f"difference between {keyword} and {top_keywords[i+1]}")
        
        # Location-based long-tails
        long_tail_suggestions.extend([
            f"{domain_name} services near me",
            f"best {domain_name} alternatives",
            f"{domain_name} pricing and features",
            f"{domain_name} customer reviews",
            f"how to get started with {domain_name}"
        ])
        
        # Get unique suggestions
        long_tail_suggestions = list(dict.fromkeys(long_tail_suggestions))[:10]
        
        return {
            'extracted_keywords': extracted_keywords[:30],
            'long_tail_suggestions': long_tail_suggestions,
            'top_keywords': top_keywords
        }