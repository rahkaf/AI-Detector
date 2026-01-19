from typing import List, Dict, Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advanced_metrics import AdvancedTextMetrics as TextMetrics
import random

class OutputSelector:
    """Select best output from ensemble model generations"""
    
    @staticmethod
    def weighted_voting(
        outputs: List[Dict[str, any]], 
        weights: Dict[str, float] = None
    ) -> Dict[str, any]:
        """
        Select output based on weighted scoring of advanced metrics
        
        Args:
            outputs: List of dicts with 'text' and 'model' keys
            weights: Dict with metric weights
        
        Returns:
            Best output dict with added 'score' and 'metrics' keys
        """
        if not outputs:
            return None
        
        if weights is None:
            weights = {
                'perplexity': 0.25,
                'burstiness': 0.25,
                'bigram_entropy': 0.15,
                'trigram_entropy': 0.10,
                'pos_entropy': 0.10,
                'semantic_coherence': 0.10,
                'repetition_penalty': 0.05
            }
        
        scored_outputs = []
        
        for output in outputs:
            text = output['text']
            metrics = TextMetrics.calculate_comprehensive_score(text, use_gpt2=False)
            
            # Calculate weighted score
            score = (
                metrics['perplexity'] * weights['perplexity'] +
                metrics['burstiness'] * weights['burstiness'] +
                metrics['bigram_entropy'] * weights['bigram_entropy'] +
                metrics['trigram_entropy'] * weights['trigram_entropy'] +
                metrics['pos_entropy'] * weights['pos_entropy'] +
                metrics['semantic_coherence'] * weights['semantic_coherence'] +
                (100 - metrics['repetitive_patterns']['repetition_score']) * weights['repetition_penalty']
            )
            
            scored_outputs.append({
                **output,
                'score': score,
                'metrics': metrics
            })
        
        # Return highest scoring output
        return max(scored_outputs, key=lambda x: x['score'])
    
    @staticmethod
    def diversity_selection(outputs: List[Dict[str, any]], top_k: int = 3) -> List[Dict[str, any]]:
        """
        Select top K most diverse outputs using advanced metrics
        """
        if not outputs:
            return []
        
        scored_outputs = []
        
        for output in outputs:
            text = output['text']
            metrics = TextMetrics.calculate_comprehensive_score(text, use_gpt2=False)
            
            scored_outputs.append({
                **output,
                'metrics': metrics,
                'score': metrics['composite_score']
            })
        
        # Sort by score and return top K
        scored_outputs.sort(key=lambda x: x['score'], reverse=True)
        return scored_outputs[:top_k]
    
    @staticmethod
    def sentence_level_mixing(outputs: List[Dict[str, any]]) -> str:
        """
        Mix sentences from different outputs to create hybrid
        This creates maximum diversity and unpredictability
        """
        if not outputs:
            return ""
        
        import re
        
        # Split all outputs into sentences
        all_sentences = []
        for output in outputs:
            sentences = re.split(r'(?<=[.!?])\s+', output['text'])
            sentences = [s.strip() for s in sentences if s.strip()]
            all_sentences.append(sentences)
        
        # Ensure all have same number of sentences (pad if needed)
        max_sentences = max(len(s) for s in all_sentences)
        
        # Mix sentences: alternate between models
        mixed_text = []
        for i in range(max_sentences):
            # Pick from different model each time
            model_idx = i % len(all_sentences)
            if i < len(all_sentences[model_idx]):
                mixed_text.append(all_sentences[model_idx][i])
        
        return ' '.join(mixed_text)
    
    @staticmethod
    def ensemble_blend(
        outputs: List[Dict[str, any]], 
        strategy: str = 'weighted'
    ) -> Dict[str, any]:
        """
        Main ensemble selection method
        
        Args:
            outputs: List of model outputs
            strategy: 'weighted', 'diverse', 'mixed', or 'best'
        
        Returns:
            Selected output with metrics
        """
        if not outputs:
            return None
        
        if strategy == 'weighted':
            return OutputSelector.weighted_voting(outputs)
        
        elif strategy == 'diverse':
            diverse_outputs = OutputSelector.diversity_selection(outputs, top_k=1)
            return diverse_outputs[0] if diverse_outputs else outputs[0]
        
        elif strategy == 'mixed':
            mixed_text = OutputSelector.sentence_level_mixing(outputs)
            metrics = TextMetrics.calculate_comprehensive_score(mixed_text, use_gpt2=False)
            return {
                'text': mixed_text,
                'model': 'ensemble_mixed',
                'metrics': metrics,
                'score': metrics['composite_score']
            }
        
        elif strategy == 'best':
            # Simply return the one with highest composite score
            best = None
            best_score = -1
            
            for output in outputs:
                metrics = TextMetrics.calculate_comprehensive_score(output['text'], use_gpt2=False)
                if metrics['composite_score'] > best_score:
                    best_score = metrics['composite_score']
                    best = {
                        **output,
                        'metrics': metrics,
                        'score': best_score
                    }
            
            return best
        
        else:
            # Default: return first output
            return outputs[0]
    
    @staticmethod
    def get_all_variations(outputs: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Return all outputs with their advanced metrics for user to choose
        """
        variations = []
        
        for output in outputs:
            metrics = TextMetrics.calculate_comprehensive_score(output['text'], use_gpt2=False)
            variations.append({
                **output,
                'metrics': metrics,
                'score': metrics['composite_score']
            })
        
        # Sort by score
        variations.sort(key=lambda x: x['score'], reverse=True)
        
        return variations
