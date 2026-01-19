"""
Advanced Metrics Module with GPT-2 True Perplexity and Caching
Optimized for performance and accuracy
"""
import math
import re
from typing import List, Dict, Tuple
from collections import Counter
from functools import lru_cache
import hashlib
import numpy as np

try:
    import nltk
    from nltk import pos_tag, word_tokenize
    from nltk.util import ngrams
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger', quiet=True)
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("Warning: NLTK not available. Some advanced features disabled.")


class GPT2PerplexityCalculator:
    """
    Singleton class for GPT-2 perplexity calculation with model caching
    """
    _instance = None
    _model = None
    _tokenizer = None
    _device = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._model is None:
            print("Loading GPT-2 model for true perplexity calculation...")
            try:
                from transformers import GPT2LMHeadModel, GPT2TokenizerFast
                import torch
                
                self._device = "cuda" if torch.cuda.is_available() else "cpu"
                print(f"Using device: {self._device}")
                
                self._model = GPT2LMHeadModel.from_pretrained('gpt2')
                self._tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
                self._model.to(self._device)
                self._model.eval()
                self._tokenizer.pad_token = self._tokenizer.eos_token
                
                print("✅ GPT-2 model loaded successfully")
            except Exception as e:
                print(f"❌ Failed to load GPT-2 model: {e}")
                self._model = None
    
    def calculate_perplexity(self, text: str) -> float:
        """Calculate true perplexity using GPT-2 model"""
        if self._model is None:
            return AdvancedTextMetrics.calculate_entropy_based_perplexity(text)
        
        try:
            import torch
            
            # Tokenize with attention mask
            encodings = self._tokenizer(text, return_tensors='pt', truncation=True, max_length=1024)
            encodings = {k: v.to(self._device) for k, v in encodings.items()}
            
            # Calculate perplexity
            with torch.no_grad():
                outputs = self._model(**encodings, labels=encodings['input_ids'])
                loss = outputs.loss
            
            perplexity = torch.exp(loss).item()
            
            # Normalize to 0-100 scale
            # Human text typically has perplexity 50-200
            # AI text typically has perplexity 10-50
            # We invert the scale: higher = more human-like
            normalized = max(0, min(100, (perplexity - 10) / 190 * 100))
            
            return float(normalized)
            
        except Exception as e:
            print(f"GPT-2 perplexity calculation failed: {e}")
            return AdvancedTextMetrics.calculate_entropy_based_perplexity(text)


class AdvancedTextMetrics:
    """
    Advanced metrics optimized for AI detection evasion
    """
    
    def __init__(self):
        self.gpt2_calculator = GPT2PerplexityCalculator()
    
    @lru_cache(maxsize=1000)
    def _get_text_hash(self, text: str) -> str:
        """Cache key for text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def calculate_entropy_based_perplexity(text: str) -> float:
        """
        Calculate perplexity using Shannon entropy (fallback method)
        More accurate than simple word frequency
        """
        words = text.lower().split()
        if len(words) < 2:
            return 0.0
        
        # Calculate word-level entropy
        word_freq = Counter(words)
        total_words = len(words)
        
        entropy = 0
        for count in word_freq.values():
            prob = count / total_words
            if prob > 0:
                entropy -= prob * math.log2(prob)
        
        # Calculate character-level entropy (more granular)
        char_freq = Counter(text.lower())
        total_chars = len(text)
        
        char_entropy = 0
        for count in char_freq.values():
            prob = count / total_chars
            if prob > 0:
                char_entropy -= prob * math.log2(prob)
        
        # Combine both (word entropy is more important)
        combined_entropy = (entropy * 0.7 + char_entropy * 0.3)
        
        # Normalize to 0-100
        max_entropy = math.log2(total_words) if total_words > 1 else 1
        normalized = (combined_entropy / max_entropy) * 100 if max_entropy > 0 else 0
        
        return min(100, max(0, normalized))
    
    @staticmethod
    def calculate_advanced_burstiness(text: str) -> float:
        """
        Advanced burstiness calculation
        Measures variation in sentence lengths AND complexity
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return 0.0
        
        # Calculate multiple metrics
        sentence_lengths = [len(s.split()) for s in sentences]
        char_lengths = [len(s) for s in sentences]
        
        # Word count variation
        word_cv = np.std(sentence_lengths) / np.mean(sentence_lengths) if np.mean(sentence_lengths) > 0 else 0
        
        # Character count variation
        char_cv = np.std(char_lengths) / np.mean(char_lengths) if np.mean(char_lengths) > 0 else 0
        
        # Calculate range (max - min) normalized
        word_range = (max(sentence_lengths) - min(sentence_lengths)) / np.mean(sentence_lengths) if np.mean(sentence_lengths) > 0 else 0
        
        # Calculate skewness (human text has more skewness)
        if len(sentence_lengths) > 3:
            skewness = float(((sentence_lengths - np.mean(sentence_lengths)) ** 3).mean() / 
                           (np.std(sentence_lengths) ** 3 + 1e-8))
        else:
            skewness = 0
        
        # Combine metrics
        burstiness = (word_cv * 0.4 + char_cv * 0.25 + word_range * 0.2 + abs(skewness) * 0.15)
        
        # Normalize to 0-100 (CV of 0.8-1.2 is typical for humans)
        normalized = min(100, (burstiness / 1.2) * 100)
        
        return float(normalized)
    
    @staticmethod
    def calculate_ngram_entropy(text: str, n: int = 2) -> float:
        """
        Calculate n-gram entropy with advanced weighting
        AI text has more predictable n-gram patterns
        """
        words = text.lower().split()
        if len(words) < n:
            return 0.0
        
        # Generate n-grams
        ngram_list = list(zip(*[words[i:] for i in range(n)]))
        
        if not ngram_list:
            return 0.0
        
        # Calculate n-gram frequency
        ngram_freq = Counter(ngram_list)
        total_ngrams = len(ngram_list)
        
        # Calculate entropy
        entropy = 0
        for count in ngram_freq.values():
            prob = count / total_ngrams
            if prob > 0:
                entropy -= prob * math.log2(prob)
        
        # Normalize
        max_entropy = math.log2(total_ngrams) if total_ngrams > 1 else 1
        normalized = (entropy / max_entropy) * 100 if max_entropy > 0 else 0
        
        return min(100, max(0, normalized))
    
    @staticmethod
    def calculate_stylometric_features(text: str) -> Dict[str, float]:
        """
        Enhanced stylometric analysis
        Used by Originality.ai and academic detectors
        """
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not words or not sentences:
            return {
                'avg_word_length': 0.0,
                'avg_sentence_length': 0.0,
                'lexical_density': 0.0,
                'function_word_ratio': 0.0,
                'punctuation_diversity': 0.0,
                'type_token_ratio': 0.0
            }
        
        # Average word length
        avg_word_length = np.mean([len(w) for w in words])
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Type-Token Ratio (vocabulary richness)
        unique_words = len(set(w.lower() for w in words))
        type_token_ratio = unique_words / len(words) if words else 0
        
        # Lexical density (content words / total words)
        function_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                         'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                         'would', 'should', 'could', 'may', 'might', 'must', 'can',
                         'of', 'to', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
                         'and', 'but', 'or', 'so', 'yet', 'nor', 'for', 'that', 'which',
                         'who', 'whom', 'whose', 'this', 'that', 'these', 'those'}
        
        function_word_count = sum(1 for w in words if w.lower() in function_words)
        function_word_ratio = function_word_count / len(words)
        lexical_density = 1 - function_word_ratio
        
        # Punctuation diversity
        punctuation = [c for c in text if c in '.,!?;:']
        punct_diversity = len(set(punctuation)) / len(punctuation) if punctuation else 0
        
        return {
            'avg_word_length': float(avg_word_length),
            'avg_sentence_length': float(avg_sentence_length),
            'lexical_density': float(lexical_density),
            'function_word_ratio': float(function_word_ratio),
            'punctuation_diversity': float(punct_diversity),
            'type_token_ratio': float(type_token_ratio)
        }
    
    @staticmethod
    def calculate_pos_tag_entropy(text: str) -> float:
        """
        Enhanced POS (Part-of-Speech) tag entropy
        AI text has more uniform POS patterns
        """
        if not NLTK_AVAILABLE:
            return 50.0
        
        try:
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            
            if not pos_tags:
                return 0.0
            
            tags = [tag for _, tag in pos_tags]
            
            # Calculate tag frequency
            tag_freq = Counter(tags)
            total_tags = len(tags)
            
            # Calculate entropy
            entropy = 0
            for count in tag_freq.values():
                prob = count / total_tags
                if prob > 0:
                    entropy -= prob * math.log2(prob)
            
            # Calculate tag diversity (unique tags / total tags)
            tag_diversity = len(tag_freq) / total_tags if total_tags > 0 else 0
            
            # Combine entropy and diversity
            combined_score = (entropy * 0.7 + tag_diversity * 100 * 0.3)
            
            # Normalize
            max_entropy = math.log2(total_tags) if total_tags > 1 else 1
            normalized = (combined_score / 100) * 100 if max_entropy > 0 else 0
            
            return min(100, max(0, float(normalized)))
            
        except Exception as e:
            print(f"POS tagging failed: {e}")
            return 50.0
    
    @staticmethod
    def detect_repetitive_patterns(text: str) -> Dict[str, any]:
        """
        Detect repetitive patterns common in AI text
        Enhanced with multi-gram analysis
        """
        words = text.lower().split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Check for repeated phrases (2-4 grams)
        pattern_scores = {}
        
        for n in [2, 3, 4]:
            ngrams = list(zip(*[words[i:] for i in range(n)]))
            ngram_freq = Counter(ngrams)
            repeated = {k: v for k, v in ngram_freq.items() if v > 1}
            pattern_scores[f'{n}gram_repetition'] = len(repeated)
        
        # Check for repeated sentence structures
        sentence_starts = [s.split()[0].lower() if s.split() else '' for s in sentences]
        start_freq = Counter(sentence_starts)
        repeated_starts = sum(1 for count in start_freq.values() if count > 2)
        
        # Check for word repetition
        word_freq = Counter(words)
        overused_words = {k: v for k, v in word_freq.items() 
                         if v > len(words) * 0.05 and len(k) > 4}
        
        # Calculate repetition score
        total_repetition = sum(pattern_scores.values()) + repeated_starts + len(overused_words)
        repetition_score = min(100, total_repetition * 8)
        
        return {
            '2gram_repetition': pattern_scores.get('2gram_repetition', 0),
            '3gram_repetition': pattern_scores.get('3gram_repetition', 0),
            '4gram_repetition': pattern_scores.get('4gram_repetition', 0),
            'repeated_sentence_starts': repeated_starts,
            'overused_words': len(overused_words),
            'repetition_score': float(repetition_score)
        }
    
    @staticmethod
    def calculate_semantic_coherence(text: str) -> float:
        """
        Measure semantic coherence
        AI text is often TOO coherent (smooth transitions)
        Human text has more topic jumps
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.split()) > 3]
        
        if len(sentences) < 2:
            return 50.0
        
        # Calculate word overlap between consecutive sentences
        overlaps = []
        for i in range(len(sentences) - 1):
            words1 = set(sentences[i].lower().split())
            words2 = set(sentences[i + 1].lower().split())
            
            if words1 and words2:
                overlap = len(words1 & words2) / len(words1 | words2)
                overlaps.append(overlap)
        
        if not overlaps:
            return 50.0
        
        # AI text has MORE consistent overlap (too smooth)
        # Human text has MORE variation in overlap
        avg_overlap = np.mean(overlaps)
        std_overlap = np.std(overlaps)
        
        # Lower average overlap + higher std = more human-like
        coherence_score = (1 - avg_overlap) * 50 + std_overlap * 50
        
        return min(100, max(0, float(coherence_score)))
    
    def calculate_comprehensive_score(self, text: str, use_gpt2: bool = True) -> Dict[str, any]:
        """
        Calculate ALL advanced metrics with optimized weighting for detection evasion
        """
        # Use GPT-2 for perplexity if available
        if use_gpt2:
            perplexity = self.gpt2_calculator.calculate_perplexity(text)
        else:
            perplexity = AdvancedTextMetrics.calculate_entropy_based_perplexity(text)
        
        # Calculate all metrics
        burstiness = AdvancedTextMetrics.calculate_advanced_burstiness(text)
        bigram_entropy = AdvancedTextMetrics.calculate_ngram_entropy(text, n=2)
        trigram_entropy = AdvancedTextMetrics.calculate_ngram_entropy(text, n=3)
        pos_entropy = AdvancedTextMetrics.calculate_pos_tag_entropy(text)
        stylometric = AdvancedTextMetrics.calculate_stylometric_features(text)
        patterns = AdvancedTextMetrics.detect_repetitive_patterns(text)
        coherence = AdvancedTextMetrics.calculate_semantic_coherence(text)
        
        # Calculate composite score with adaptive weighting
        # Heavily weight metrics that distinguish human vs AI text
        composite = (
            perplexity * 0.22 +
            burstiness * 0.20 +
            bigram_entropy * 0.12 +
            trigram_entropy * 0.10 +
            pos_entropy * 0.10 +
            coherence * 0.10 +
            (100 - patterns['repetition_score']) * 0.08 +
            stylometric['type_token_ratio'] * 100 * 0.08
        )
        
        # Apply bonuses and penalties based on stylometric features
        # Penalize AI-like patterns
        if stylometric['avg_sentence_length'] > 25:
            composite -= 8
        if stylometric['function_word_ratio'] < 0.3:
            composite -= 6
        if stylometric['type_token_ratio'] < 0.5:
            composite -= 5
        
        # Bonus for human-like features
        if stylometric['avg_sentence_length'] < 20 and stylometric['avg_sentence_length'] > 10:
            composite += 5
        if stylometric['punctuation_diversity'] > 0.4:
            composite += 3
        
        composite = max(0, min(100, composite))
        
        # Determine detection resistance level
        if composite >= 80:
            resistance = 'VERY HIGH'
        elif composite >= 70:
            resistance = 'HIGH'
        elif composite >= 60:
            resistance = 'MEDIUM-HIGH'
        elif composite >= 50:
            resistance = 'MEDIUM'
        else:
            resistance = 'LOW'
        
        return {
            'perplexity': round(perplexity, 2),
            'burstiness': round(burstiness, 2),
            'bigram_entropy': round(bigram_entropy, 2),
            'trigram_entropy': round(trigram_entropy, 2),
            'pos_entropy': round(pos_entropy, 2),
            'semantic_coherence': round(coherence, 2),
            'stylometric_features': stylometric,
            'repetitive_patterns': patterns,
            'composite_score': round(composite, 2),
            'detection_resistance': resistance,
            'word_count': len(text.split()),
            'sentence_count': len(re.split(r'[.!?]+', text))
        }
