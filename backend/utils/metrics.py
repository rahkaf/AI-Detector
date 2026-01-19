import math
import re
from typing import List, Dict
from collections import Counter
import numpy as np

class TextMetrics:
    """Calculate perplexity, burstiness, and diversity metrics for text"""
    
    @staticmethod
    def calculate_perplexity(text: str, model_probs: List[float] = None) -> float:
        """
        Calculate perplexity score (higher = more unpredictable = more human-like)
        If model_probs not provided, use a heuristic based on word rarity
        """
        if model_probs:
            # True perplexity from model probabilities
            log_probs = [math.log(p) if p > 0 else -100 for p in model_probs]
            avg_log_prob = sum(log_probs) / len(log_probs)
            return math.exp(-avg_log_prob)
        
        # Heuristic perplexity based on word diversity and rarity
        words = text.lower().split()
        if not words:
            return 0.0
        
        # Calculate word frequency distribution
        word_freq = Counter(words)
        total_words = len(words)
        
        # Calculate entropy (higher entropy = higher perplexity)
        entropy = 0
        for count in word_freq.values():
            prob = count / total_words
            entropy -= prob * math.log2(prob)
        
        # Normalize to 0-100 scale (higher is better)
        max_entropy = math.log2(total_words) if total_words > 1 else 1
        normalized_score = (entropy / max_entropy) * 100 if max_entropy > 0 else 0
        
        return min(100, max(0, normalized_score))
    
    @staticmethod
    def calculate_burstiness(text: str) -> float:
        """
        Calculate burstiness score (variation in sentence lengths)
        Higher score = more human-like variation
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return 0.0
        
        # Calculate word count per sentence
        sentence_lengths = [len(s.split()) for s in sentences]
        
        # Calculate coefficient of variation (std/mean)
        mean_length = np.mean(sentence_lengths)
        std_length = np.std(sentence_lengths)
        
        if mean_length == 0:
            return 0.0
        
        cv = std_length / mean_length
        
        # Normalize to 0-100 scale (higher is better)
        # CV of 0.5-1.0 is typical for human writing
        normalized_score = min(100, (cv / 1.0) * 100)
        
        return normalized_score
    
    @staticmethod
    def calculate_diversity(text: str) -> float:
        """
        Calculate lexical diversity (unique words / total words)
        Higher diversity = more human-like
        """
        words = text.lower().split()
        if not words:
            return 0.0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        diversity_ratio = unique_words / total_words
        
        # Normalize to 0-100 scale
        return diversity_ratio * 100
    
    @staticmethod
    def detect_ai_patterns(text: str) -> Dict[str, any]:
        """
        Detect common AI writing patterns
        Returns dict with pattern counts and flags
        """
        text_lower = text.lower()
        
        # Common AI clichés
        ai_phrases = [
            'delve', 'comprehensive', 'tapestry', 'unveiling', 'seamless',
            'crucial', 'pivot', 'navigate', 'in conclusion', 'furthermore',
            'moreover', 'it is important to note', 'in today\'s digital landscape',
            'robust', 'leverage', 'paradigm', 'synergy', 'holistic'
        ]
        
        detected_phrases = [phrase for phrase in ai_phrases if phrase in text_lower]
        
        # Check for overly uniform sentence structure
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Check for passive voice overuse
        passive_indicators = ['was', 'were', 'been', 'being', 'is', 'are']
        passive_count = sum(1 for word in text_lower.split() if word in passive_indicators)
        passive_ratio = passive_count / len(text.split()) if text.split() else 0
        
        return {
            'ai_phrases_found': detected_phrases,
            'ai_phrase_count': len(detected_phrases),
            'passive_voice_ratio': passive_ratio,
            'is_likely_ai': len(detected_phrases) > 3 or passive_ratio > 0.15
        }
    
    @staticmethod
    def calculate_composite_score(text: str) -> Dict[str, float]:
        """
        Calculate all metrics and return composite humanization score
        """
        perplexity = TextMetrics.calculate_perplexity(text)
        burstiness = TextMetrics.calculate_burstiness(text)
        diversity = TextMetrics.calculate_diversity(text)
        ai_patterns = TextMetrics.detect_ai_patterns(text)
        
        # Composite score (weighted average)
        # Penalize for AI patterns
        ai_penalty = ai_patterns['ai_phrase_count'] * 5
        
        composite = (
            perplexity * 0.35 +
            burstiness * 0.35 +
            diversity * 0.30
        ) - ai_penalty
        
        composite = max(0, min(100, composite))
        
        return {
            'perplexity': round(perplexity, 2),
            'burstiness': round(burstiness, 2),
            'diversity': round(diversity, 2),
            'composite_score': round(composite, 2),
            'ai_patterns': ai_patterns,
            'word_count': len(text.split()),
            'sentence_count': len(re.split(r'[.!?]+', text))
        }
