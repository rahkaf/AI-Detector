import re
from typing import List, Tuple

class TextPreprocessor:
    """Preprocess and postprocess text for humanization"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize input text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might confuse models
        text = re.sub(r'[^\w\s.,!?;:\-\'"()\[\]{}]', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text.strip()
    
    @staticmethod
    def split_into_chunks(text: str, max_length: int = 400) -> List[str]:
        """
        Split long text into processable chunks at sentence boundaries
        """
        # Split by sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            
            if current_length + sentence_words > max_length and current_chunk:
                # Save current chunk and start new one
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_words
            else:
                current_chunk.append(sentence)
                current_length += sentence_words
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    @staticmethod
    def merge_chunks(chunks: List[str]) -> str:
        """Merge processed chunks back together"""
        return ' '.join(chunks)
    
    @staticmethod
    def add_human_touches(text: str) -> str:
        """
        Add subtle human-like imperfections and variations
        """
        # Occasionally start sentences with conjunctions
        text = re.sub(r'\. However,', '. But', text, count=1)
        text = re.sub(r'\. Additionally,', '. And', text, count=1)
        
        # Add contractions randomly
        contractions = {
            'do not': "don't",
            'does not': "doesn't",
            'did not': "didn't",
            'is not': "isn't",
            'are not': "aren't",
            'was not': "wasn't",
            'were not': "weren't",
            'have not': "haven't",
            'has not': "hasn't",
            'had not': "hadn't",
            'will not': "won't",
            'would not': "wouldn't",
            'should not': "shouldn't",
            'cannot': "can't",
            'could not': "couldn't",
        }
        
        # Apply some contractions (not all, to maintain variety)
        import random
        for formal, casual in contractions.items():
            if formal in text and random.random() > 0.5:
                text = text.replace(formal, casual, 1)
        
        return text
    
    @staticmethod
    def remove_ai_cliches(text: str) -> str:
        """
        Remove or replace common AI clichés
        """
        replacements = {
            'delve into': 'explore',
            'delve': 'examine',
            'comprehensive': 'complete',
            'tapestry': 'mix',
            'unveiling': 'revealing',
            'seamless': 'smooth',
            'leverage': 'use',
            'robust': 'strong',
            'in conclusion': 'finally',
            'furthermore': 'also',
            'moreover': 'also',
            'it is important to note': 'note that',
            'in today\'s digital landscape': 'today',
            'paradigm': 'model',
            'synergy': 'cooperation',
            'holistic': 'complete',
        }
        
        text_lower = text
        for cliche, replacement in replacements.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(cliche), re.IGNORECASE)
            text_lower = pattern.sub(replacement, text_lower)
        
        return text_lower
    
    @staticmethod
    def format_output(text: str) -> str:
        """Final formatting of output text"""
        # Ensure proper spacing after punctuation
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]
        
        return text.strip()
