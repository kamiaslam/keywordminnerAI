import nltk
from collections import Counter
import re
from typing import List, Dict
import string

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams

class NLPKeywordEngine:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.common_words = {
            'click', 'here', 'read', 'more', 'learn', 'get', 'start', 
            'contact', 'us', 'privacy', 'policy', 'terms', 'conditions'
        }
        
    def extract_keywords(self, content: Dict) -> List[Dict]:
        all_text = self._combine_content(content)
        
        cleaned_text = self._clean_text(all_text)
        
        single_keywords = self._extract_ngrams(cleaned_text, 1)
        two_word_keywords = self._extract_ngrams(cleaned_text, 2)
        three_word_keywords = self._extract_ngrams(cleaned_text, 3)
        
        all_keywords = []
        
        for keyword, count in single_keywords.most_common(30):
            if len(keyword) > 3:
                all_keywords.append({
                    'keyword': keyword,
                    'count': count,
                    'type': 'short-tail',
                    'intent': self._classify_intent(keyword)
                })
        
        for keyword, count in two_word_keywords.most_common(20):
            all_keywords.append({
                'keyword': keyword,
                'count': count,
                'type': 'mid-tail',
                'intent': self._classify_intent(keyword)
            })
        
        for keyword, count in three_word_keywords.most_common(15):
            all_keywords.append({
                'keyword': keyword,
                'count': count,
                'type': 'long-tail',
                'intent': self._classify_intent(keyword)
            })
        
        branded_keywords = self._extract_branded_keywords(content)
        all_keywords.extend(branded_keywords)
        
        return sorted(all_keywords, key=lambda x: x['count'], reverse=True)
    
    def _combine_content(self, content: Dict) -> str:
        text_parts = []
        
        if content.get('title'):
            text_parts.append(content['title'] * 3)
        
        if content.get('meta_description'):
            text_parts.append(content['meta_description'] * 2)
        
        if content.get('meta_keywords'):
            text_parts.append(content['meta_keywords'] * 2)
        
        for level, headings in content.get('headings', {}).items():
            weight = 7 - int(level[1])
            for heading in headings:
                text_parts.append(heading * weight)
        
        text_parts.extend(content.get('paragraphs', []))
        text_parts.extend(content.get('links', []))
        text_parts.extend(content.get('images_alt', []))
        
        return ' '.join(text_parts)
    
    def _clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s-]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_ngrams(self, text: str, n: int) -> Counter:
        tokens = word_tokenize(text)
        
        filtered_tokens = [
            token for token in tokens 
            if token not in self.stop_words 
            and token not in self.common_words
            and len(token) > 2
            and not token.isdigit()
        ]
        
        if n == 1:
            return Counter(filtered_tokens)
        else:
            n_grams = list(ngrams(filtered_tokens, n))
            n_gram_strings = [' '.join(gram) for gram in n_grams]
            return Counter(n_gram_strings)
    
    def _classify_intent(self, keyword: str) -> str:
        commercial_indicators = [
            'buy', 'price', 'cost', 'cheap', 'best', 'top', 'review',
            'compare', 'vs', 'deal', 'discount', 'coupon', 'sale'
        ]
        
        informational_indicators = [
            'how', 'what', 'why', 'when', 'where', 'guide', 'tutorial',
            'learn', 'understand', 'definition', 'meaning', 'example'
        ]
        
        navigational_indicators = [
            'login', 'sign', 'download', 'contact', 'location', 'near',
            'website', 'official', 'homepage'
        ]
        
        keyword_lower = keyword.lower()
        
        for indicator in commercial_indicators:
            if indicator in keyword_lower:
                return 'commercial'
        
        for indicator in informational_indicators:
            if indicator in keyword_lower:
                return 'informational'
        
        for indicator in navigational_indicators:
            if indicator in keyword_lower:
                return 'navigational'
        
        return 'general'
    
    def _extract_branded_keywords(self, content: Dict) -> List[Dict]:
        branded_keywords = []
        
        title_words = content.get('title', '').split()
        potential_brands = [
            word for word in title_words 
            if word[0].isupper() and len(word) > 2
        ]
        
        for brand in potential_brands[:3]:
            branded_keywords.append({
                'keyword': brand.lower(),
                'count': 0,
                'type': 'branded',
                'intent': 'navigational'
            })
        
        return branded_keywords