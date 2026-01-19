"""
Advanced AI Detection Metrics
Based on research from GPTZero, Originality.ai, and academic papers
Implements: True Perplexity, Entropy, N-gram Analysis, Stylometry, POS Tagging
"""
import math
import re
from typing import List, Dict, Tuple
from collections import Counter
import numpy as np

try:
    import nltk
    from nltk import pos_tag, word_tokenize
    from nltk.util import ngrams
    # Download required NLTK data
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


class AdvancedTextMetrics:
    """
    Advanced metrics based on state-of-the-art AI detection research
    """
    
    @staticmethod
    def calculate_true_perplexity_with_gpt2(text: str) -> float:
        """
        Calculate TRUE perplexity using GPT-2 model (like GPTZero does)
        This is the most accurate perplexity measurement
        """
        try:
            from transformers import GPT2LMHeadModel, GPT2TokenizerFast
            import torch
            
            # Load GPT-2 (small, fast)
            model = GPT2LMHeadModel.from_pretrained('gpt2')
            tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
            model.eval()
            
            # Tokenize
            encodings = tokenizer(text, return_tensors='pt')
            
            # Calculate perplexity
            with torch.no_grad():
                outputs = model(**encodings, labels=encodings['input_ids'])
                loss = outputs.loss
                perplexity = torch.exp(loss).item()
            
            # Normalize to 0-100 (lower perplexity = more AI-like)
            # Human text typically has perplexity 50-200
            # AI text typically has perplexity 10-50
            normalized = max(0, min(100, (perplexity - 10) / 190 * 100))
            
            return normalized
            
        except Exception as e:
            print(f"GPT-2 perplexity calculation failed: {e}")
            return AdvancedTextMetrics.calculate_entropy_based_perplexity(text)
    
    @staticmethod
    def calculate_entropy_based_perplexity(text: str) -> float:
        """
        Calculate perplexity using Shannon entropy
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
        
        # Combine metrics
        burstiness = (word_cv * 0.5 + char_cv * 0.3 + word_range * 0.2)
        
        # Normalize to 0-100 (CV of 0.8-1.2 is typical for humans)
        normalized = min(100, (burstiness / 1.2) * 100)
        
        return normalized
    
    @staticmethod
    def calculate_ngram_entropy(text: str, n: int = 2) -> float:
        """
        Calculate n-gram entropy
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
        Stylometric analysis - examines writing style patterns
        Used by Originality.ai and academic detectors
        """
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not words or not sentences:
            return {
                'avg_word_length': 0,
                'avg_sentence_length': 0,
                'lexical_density': 0,
                'function_word_ratio': 0,
                'punctuation_diversity': 0
            }
        
        # Average word length
        avg_word_length = np.mean([len(w) for w in words])
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Lexical density (content words / total words)
        # Function words: the, a, an, is, are, was, were, etc.
        function_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                         'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                         'would', 'should', 'could', 'may', 'might', 'must', 'can',
                         'of', 'to', 'in', 'for', 'on', 'with', 'at', 'by', 'from'}
        
        function_word_count = sum(1 for w in words if w.lower() in function_words)
        function_word_ratio = function_word_count / len(words)
        lexical_density = 1 - function_word_ratio
        
        # Punctuation diversity
        punctuation = [c for c in text if c in '.,!?;:']
        punct_diversity = len(set(punctuation)) / len(punctuation) if punctuation else 0
        
        return {
            'avg_word_length': avg_word_length,
            'avg_sentence_length': avg_sentence_length,
            'lexical_density': lexical_density,
            'function_word_ratio': function_word_ratio,
            'punctuation_diversity': punct_diversity
        }
    
    @staticmethod
    def calculate_pos_tag_entropy(text: str) -> float:
        """
        POS (Part-of-Speech) tag entropy
        AI text has more uniform POS patterns
        """
        if not NLTK_AVAILABLE:
            return 50.0  # Default middle value
        
        try:
            # Tokenize and POS tag
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            
            # Extract just the tags
            tags = [tag for _, tag in pos_tags]
            
            if not tags:
                return 0.0
            
            # Calculate tag frequency
            tag_freq = Counter(tags)
            total_tags = len(tags)
            
            # Calculate entropy
            entropy = 0
            for count in tag_freq.values():
                prob = count / total_tags
                if prob > 0:
                    entropy -= prob * math.log2(prob)
            
            # Normalize
            max_entropy = math.log2(total_tags) if total_tags > 1 else 1
            normalized = (entropy / max_entropy) * 100 if max_entropy > 0 else 0
            
            return min(100, max(0, normalized))
            
        except Exception as e:
            print(f"POS tagging failed: {e}")
            return 50.0
    
    @staticmethod
    def detect_repetitive_patterns(text: str) -> Dict[str, any]:
        """
        Detect repetitive patterns common in AI text
        """
        words = text.lower().split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Check for repeated phrases (3-grams)
        trigrams = list(zip(words, words[1:], words[2:]))
        trigram_freq = Counter(trigrams)
        repeated_trigrams = {k: v for k, v in trigram_freq.items() if v > 1}
        
        # Check for repeated sentence structures
        sentence_starts = [s.split()[0].lower() if s.split() else '' for s in sentences]
        start_freq = Counter(sentence_starts)
        repeated_starts = sum(1 for count in start_freq.values() if count > 2)
        
        # Check for word repetition
        word_freq = Counter(words)
        overused_words = {k: v for k, v in word_freq.items() if v > len(words) * 0.05 and len(k) > 4}
        
        return {
            'repeated_trigrams': len(repeated_trigrams),
            'repeated_sentence_starts': repeated_starts,
            'overused_words': len(overused_words),
            'repetition_score': min(100, (len(repeated_trigrams) + repeated_starts + len(overused_words)) * 10)
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
        
        return min(100, max(0, coherence_score))
    
    @staticmethod
    def calculate_comprehensive_score(text: str, use_gpt2: bool = False) -> Dict[str, any]:
        """
        Calculate ALL advanced metrics
        This is the most comprehensive detection-resistant scoring
        """
        # Basic metrics
        if use_gpt2:
            perplexity = AdvancedTextMetrics.calculate_true_perplexity_with_gpt2(text)
        else:
            perplexity = AdvancedTextMetrics.calculate_entropy_based_perplexity(text)
        
        burstiness = AdvancedTextMetrics.calculate_advanced_burstiness(text)
        
        # Advanced metrics
        bigram_entropy = AdvancedTextMetrics.calculate_ngram_entropy(text, n=2)
        trigram_entropy = AdvancedTextMetrics.calculate_ngram_entropy(text, n=3)
        pos_entropy = AdvancedTextMetrics.calculate_pos_tag_entropy(text)
        
        # Stylometric features
        stylometric = AdvancedTextMetrics.calculate_stylometric_features(text)
        
        # Pattern detection
        patterns = AdvancedTextMetrics.detect_repetitive_patterns(text)
        
        # Semantic coherence
        coherence = AdvancedTextMetrics.calculate_semantic_coherence(text)
        
        # Calculate composite score with advanced weighting
        composite = (
            perplexity * 0.25 +
            burstiness * 0.25 +
            bigram_entropy * 0.15 +
            trigram_entropy * 0.10 +
            pos_entropy * 0.10 +
            coherence * 0.10 +
            (100 - patterns['repetition_score']) * 0.05
        )
        
        # Penalize for AI-like stylometric features
        if stylometric['avg_sentence_length'] > 25:  # AI tends to write longer sentences
            composite -= 5
        if stylometric['function_word_ratio'] < 0.3:  # AI uses fewer function words
            composite -= 5
        
        composite = max(0, min(100, composite))
        
        return {
            'perplexity': round(perplexity, 2),
            'burstiness': round(burstiness, 2),
            'bigram_entropy': round(bigram_entropy, 2),
            'trigram_entropy': round(trigram_entropy, 2),
            'pos_entropy': round(pos_entropy, 2),
            'semantic_coherence': round(coherence, 2),
            'stylometric_features': {k: round(v, 2) for k, v in stylometric.items()},
            'repetitive_patterns': patterns,
            'composite_score': round(composite, 2),
            'detection_resistance': 'HIGH' if composite > 75 else 'MEDIUM' if composite > 50 else 'LOW',
            'word_count': len(text.split()),
            'sentence_count': len(re.split(r'[.!?]+', text))
        }

