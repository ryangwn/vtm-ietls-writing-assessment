"""
Utility functions for IELTS scoring system
"""
import re
import json
import collections
from typing import Dict, Any, Union, Optional, List, Tuple

def count_words(text: str) -> int:
    """
    Count the number of words in a text.
    
    Args:
        text: The text to count words in
        
    Returns:
        int: The number of words in the text
    """
    # Remove special characters and extra spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split by spaces and count
    words = text.split()
    return len(words)

def extract_json_from_llm_response(response: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from LLM response, handling potential formatting issues.
    
    Args:
        response: The LLM response text
        
    Returns:
        Dict or None: The parsed JSON or None if parsing failed
    """
    try:
        # First try to parse the entire response as JSON
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON block if it exists
        json_pattern = r'```json\s*([\s\S]*?)\s*```|{[\s\S]*}'
        match = re.search(json_pattern, response)
        
        if match:
            json_str = match.group(1) if match.group(1) else match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # Clean up potential issues and try again
                cleaned_json = re.sub(r'[\n\r\t]', ' ', json_str)
                cleaned_json = re.sub(r',\s*}', '}', cleaned_json)
                try:
                    return json.loads(cleaned_json)
                except json.JSONDecodeError:
                    return None
        return None


def analyze_repetitive_words(text: str, top_n: int = 10, min_word_length: int = 3) -> List[Tuple[str, int]]:
    """
    Analyze text to find most frequently used words.
    
    Args:
        text: The essay text to analyze
        top_n: Number of top words to return
        min_word_length: Minimum length of words to consider
        
    Returns:
        List of tuples containing (word, count) sorted by frequency
    """
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Common stopwords to exclude
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
        'when', 'where', 'how', 'who', 'which', 'this', 'that', 'these', 'those',
        'then', 'than', 'so', 'for', 'to', 'of', 'by', 'with', 'about', 'against',
        'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'all', 'any', 'both', 'each',
        'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
        'own', 'same', 'too', 'very', 'can', 'will', 'just', 'should', 'now', 'also',
        'been', 'have', 'has', 'had', 'do', 'does', 'did', 'doing', 'is', 'are',
        'was', 'were', 'be', 'being', 'am', 'they', 'them', 'their', 'he', 'she',
        'him', 'her', 'his', 'hers', 'its', 'we', 'us', 'our', 'i', 'me', 'my',
        'myself', 'yourself', 'himself', 'herself', 'itself', 'themselves', 'ourselves',
        'yourselves', 'you', 'your', 'it', 'at', 'many'
    }
    
    # Filter out stopwords and short words
    filtered_words = [word for word in words if word not in stopwords and len(word) >= min_word_length]
    
    # Count word frequencies
    word_counts = collections.Counter(filtered_words)
    
    # Get the most common words
    most_common = word_counts.most_common(top_n)
    
    return most_common
