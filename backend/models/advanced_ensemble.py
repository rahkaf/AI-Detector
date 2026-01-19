"""
Advanced Ensemble Humanizer with Sophisticated Detection Evasion
Implements advanced blending, style transfer, multi-pass refinement, and adaptive strategies
"""
import torch
from transformers import (
    BartForConditionalGeneration, BartTokenizer,
    T5ForConditionalGeneration, T5Tokenizer,
    PegasusForConditionalGeneration, PegasusTokenizer
)
from typing import List, Dict, Optional, Tuple
import time
import sys
import os
import random
import re
from collections import defaultdict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advanced_metrics import AdvancedTextMetrics as TextMetrics
from utils.preprocessor import TextPreprocessor
from utils.advanced_preprocessor import AdvancedPreprocessor, IterativeHumanizer
from config import Config


class AdvancedEnsembleHumanizer:
    """
    Advanced ensemble with sophisticated blending strategies for maximum detection evasion
    """
    
    def __init__(
        self,
        device: str = "cpu",
        use_bart: bool = True,
        use_t5: bool = True,
        use_pegasus: bool = True
    ):
        self.device = device
        self.preprocessor = TextPreprocessor()
        self.advanced_preprocessor = AdvancedPreprocessor()
        self.iterative_humanizer = IterativeHumanizer(target_score=85.0, max_iterations=5)
        self.metrics_cache = {}
        
        # Model containers
        self.models = {}
        self.tokenizers = {}
        
        # Style templates for style transfer
        self.style_templates = {
            'academic': {
                'formal': 0.9,
                'sentence_length': 'long',
                'complexity': 'high'
            },
            'casual': {
                'formal': 0.3,
                'sentence_length': 'short',
                'complexity': 'low'
            },
            'professional': {
                'formal': 0.7,
                'sentence_length': 'medium',
                'complexity': 'medium'
            },
            'creative': {
                'formal': 0.4,
                'sentence_length': 'varied',
                'complexity': 'medium'
            }
        }
        
        print("=" * 70)
        print("Initializing ADVANCED Ensemble Humanizer")
        print("=" * 70)
        
        # Load models
        if use_bart:
            self._load_bart()
        
        if use_t5:
            self._load_t5()
        
        if use_pegasus:
            self._load_pegasus()
        
        print("=" * 70)
        print(f"✅ Advanced Ensemble ready with {len(self.models)} models")
        print(f"   Models loaded: {list(self.models.keys())}")
        print(f"   Device: {self.device}")
        print(f"   Strategies available: adaptive, mixed, cascade, style_transfer")
        print("=" * 70)
    
    def _load_bart(self):
        try:
            print("Loading BART model...")
            self.tokenizers['bart'] = BartTokenizer.from_pretrained(
                Config.BART_MODEL,
                resume_download=True
            )
            self.models['bart'] = BartForConditionalGeneration.from_pretrained(
                Config.BART_MODEL,
                resume_download=True
            )
            self.models['bart'].to(self.device)
            self.models['bart'].eval()
            print("✅ BART loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load BART: {e}")
    
    def _load_t5(self):
        try:
            print("Loading T5 model...")
            self.tokenizers['t5'] = T5Tokenizer.from_pretrained(
                Config.T5_MODEL,
                resume_download=True,
                legacy=False
            )
            self.models['t5'] = T5ForConditionalGeneration.from_pretrained(
                Config.T5_MODEL,
                resume_download=True
            )
            self.models['t5'].to(self.device)
            self.models['t5'].eval()
            print("✅ T5 loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load T5: {e}")
    
    def _load_pegasus(self):
        try:
            print("Loading PEGASUS model...")
            self.tokenizers['pegasus'] = PegasusTokenizer.from_pretrained(
                Config.PEGASUS_MODEL,
                resume_download=True
            )
            self.models['pegasus'] = PegasusForConditionalGeneration.from_pretrained(
                Config.PEGASUS_MODEL,
                resume_download=True
            )
            self.models['pegasus'].to(self.device)
            self.models['pegasus'].eval()
            print("✅ PEGASUS loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load PEGASUS: {e}")
    
    def _analyze_text_characteristics(self, text: str) -> Dict:
        """Analyze text to determine optimal strategy"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        word_count = len(words)
        avg_word_length = sum(len(w) for w in words) / word_count if word_count > 0 else 0
        sentence_count = len([s for s in sentences if s.strip()])
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Calculate vocabulary diversity
        unique_words = len(set(w.lower() for w in words))
        vocabulary_diversity = unique_words / word_count if word_count > 0 else 0
        
        # Determine text category
        if avg_sentence_length > 25 and vocabulary_diversity > 0.6:
            category = 'academic'
        elif avg_sentence_length < 15 and vocabulary_diversity < 0.5:
            category = 'casual'
        elif avg_sentence_length > 20:
            category = 'professional'
        else:
            category = 'creative'
        
        return {
            'word_count': word_count,
            'avg_word_length': avg_word_length,
            'sentence_count': sentence_count,
            'avg_sentence_length': avg_sentence_length,
            'vocabulary_diversity': vocabulary_diversity,
            'category': category
        }
    
    def _adaptive_temperature_selection(self, text_analysis: Dict) -> Tuple[float, float, float]:
        """Select adaptive generation parameters based on text analysis"""
        category = text_analysis['category']
        
        if category == 'academic':
            # Academic text: moderate temperature, preserve meaning
            temperature = random.uniform(1.2, 1.5)
            top_k = random.randint(100, 150)
            top_p = random.uniform(0.92, 0.97)
        elif category == 'casual':
            # Casual text: higher temperature for variety
            temperature = random.uniform(1.6, 2.0)
            top_k = random.randint(150, 200)
            top_p = random.uniform(0.95, 0.99)
        elif category == 'professional':
            # Professional text: balanced parameters
            temperature = random.uniform(1.4, 1.7)
            top_k = random.randint(120, 170)
            top_p = random.uniform(0.93, 0.98)
        else:  # creative
            # Creative text: maximum diversity
            temperature = random.uniform(1.7, 2.1)
            top_k = random.randint(150, 200)
            top_p = random.uniform(0.96, 0.99)
        
        return temperature, top_k, top_p
    
    def _generate_with_adaptive_params(
        self,
        model_name: str,
        text: str,
        text_analysis: Dict,
        num_return_sequences: int = 1
    ) -> List[str]:
        """Generate text with adaptive parameters based on text analysis"""
        if model_name not in self.models:
            return []
        
        try:
            # Get adaptive parameters
            temperature, top_k, top_p = self._adaptive_temperature_selection(text_analysis)
            
            # Split into sentences for better paraphrasing
            sentences = re.split(r'(?<=[.!?])\s+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            all_results = [[] for _ in range(num_return_sequences)]
            
            for sentence in sentences:
                sent_length = len(sentence.split())
                sent_max_length = max(60, int(sent_length * 2.5))
                
                # Get model-specific prefix
                if model_name == 't5':
                    input_text = f"paraphrase: {sentence} </s>"
                else:
                    input_text = sentence
                
                inputs = self.tokenizers[model_name](
                    input_text,
                    max_length=512,
                    padding='longest',
                    truncation=True,
                    return_tensors='pt'
                )
                
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.models[model_name].generate(
                        **inputs,
                        max_length=sent_max_length,
                        num_return_sequences=num_return_sequences,
                        num_beams=random.randint(3, 5),
                        temperature=temperature,
                        top_k=top_k,
                        top_p=top_p,
                        do_sample=True,
                        early_stopping=False,
                        no_repeat_ngram_size=random.randint(2, 3),
                        repetition_penalty=random.uniform(1.2, 1.4),
                        diversity_penalty=random.uniform(0.3, 0.7),
                        num_beam_groups=2 if num_return_sequences > 1 else 1,
                    )
                
                for i, output in enumerate(outputs):
                    decoded = self.tokenizers[model_name].decode(
                        output,
                        skip_special_tokens=True,
                        clean_up_tokenization_spaces=True
                    )
                    all_results[i].append(decoded)
            
            # Combine sentences back
            final_results = [' '.join(result) for result in all_results]
            return final_results
        
        except Exception as e:
            print(f"Error in {model_name} generation: {e}")
            return []
    
    def _advanced_cascade_blending(self, all_outputs: List[Dict]) -> str:
        """
        Advanced cascade blending: Pass outputs through multiple models
        This creates more diverse and unpredictable text
        """
        if not all_outputs:
            return ""
        
        # Get best output from each model
        by_model = defaultdict(list)
        for output in all_outputs:
            by_model[output['model']].append(output)
        
        best_by_model = {}
        for model, outputs in by_model.items():
            best = max(outputs, key=lambda x: x.get('metrics', {}).get('composite_score', 0))
            best_by_model[model] = best
        
        # If only one model, return its best output
        if len(best_by_model) == 1:
            return list(best_by_model.values())[0]['text']
        
        # Cascade: Pass each model's best through another model
        cascade_outputs = []
        models_available = list(best_by_model.keys())
        
        for i, (model1, output1) in enumerate(best_by_model.items()):
            # Choose a different model to cascade through
            model2 = models_available[(i + 1) % len(models_available)]
            
            # Cascade output from model1 through model2
            cascade_result = self._generate_with_adaptive_params(
                model2,
                output1['text'],
                self._analyze_text_characteristics(output1['text']),
                num_return_sequences=1
            )
            
            if cascade_result:
                cascade_outputs.append({
                    'text': cascade_result[0],
                    'model': f"{model1}->{model2}",
                    'original_model': model1,
                    'cascade_model': model2
                })
        
        # Score cascade outputs
        for output in cascade_outputs:
            output['metrics'] = TextMetrics.calculate_comprehensive_score(output['text'], use_gpt2=False)
            output['score'] = output['metrics']['composite_score']
        
        # Return best cascade output
        if cascade_outputs:
            best = max(cascade_outputs, key=lambda x: x['score'])
            return best['text']
        
        # Fallback: blend original outputs
        return self._intelligent_sentence_blending(best_by_model)
    
    def _intelligent_sentence_blending(self, outputs: Dict) -> str:
        """
        Intelligent sentence-level blending with context awareness
        Selects best sentences from each model based on quality
        """
        if not outputs:
            return ""
        
        # Split each output into sentences
        sentences_by_model = {}
        for model, output in outputs.items():
            sentences = re.split(r'(?<=[.!?])\s+', output['text'])
            sentences_by_model[model] = [s.strip() for s in sentences if s.strip()]
        
        # Score each sentence from each model
        scored_sentences = []
        models = list(sentences_by_model.keys())
        
        for i in range(max(len(s) for s in sentences_by_model.values())):
            for model in models:
                if i < len(sentences_by_model[model]):
                    sentence = sentences_by_model[model][i]
                    
                    # Simple sentence quality score
                    words = sentence.split()
                    quality_score = 0
                    
                    # Prefer medium length sentences (10-20 words)
                    if 10 <= len(words) <= 20:
                        quality_score += 30
                    elif 5 <= len(words) <= 30:
                        quality_score += 20
                    else:
                        quality_score += 10
                    
                    # Prefer sentences with good structure
                    if any(word in sentence for word in [',', 'and', 'but', 'or', 'so']):
                        quality_score += 20
                    
                    # Penalize very short sentences (< 5 words)
                    if len(words) < 5:
                        quality_score -= 10
                    
                    # Add some randomness for variety
                    quality_score += random.uniform(-10, 10)
                    
                    scored_sentences.append({
                        'sentence': sentence,
                        'model': model,
                        'score': quality_score,
                        'position': i
                    })
        
        # Group by position and select best
        positions = defaultdict(list)
        for s in scored_sentences:
            positions[s['position']].append(s)
        
        # Select best sentence at each position
        blended = []
        for i in range(len(positions)):
            if positions[i]:
                best = max(positions[i], key=lambda x: x['score'])
                blended.append(best['sentence'])
        
        return ' '.join(blended)
    
    def _style_transfer_enhancement(self, text: str, target_style: str) -> str:
        """
        Apply style transfer to match target writing style
        """
        style_config = self.style_templates.get(target_style, self.style_templates['professional'])
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        enhanced_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            
            # Adjust sentence length based on style
            target_length = {
                'short': random.randint(5, 12),
                'medium': random.randint(12, 20),
                'long': random.randint(18, 30)
            }.get(style_config['sentence_length'], 15)
            
            current_length = len(words)
            
            if current_length > target_length + 5:
                # Split long sentences
                split_point = current_length // 2
                part1 = ' '.join(words[:split_point])
                part2 = ' '.join(words[split_point:])
                enhanced_sentences.append(part1 + '.')
                enhanced_sentences.append(part2 + '.')
            elif current_length < target_length - 5:
                # Combine short sentences
                if enhanced_sentences and len(enhanced_sentences[-1].split()) < target_length - 3:
                    enhanced_sentences[-1] = enhanced_sentences[-1][:-1] + ' ' + sentence + '.'
                else:
                    enhanced_sentences.append(sentence + '.')
            else:
                enhanced_sentences.append(sentence + '.' if not sentence.endswith(('.', '!', '?')) else sentence)
        
        # Apply formality adjustments
        result = ' '.join(enhanced_sentences)
        
        if style_config['formal'] < 0.5:
            # More casual: add contractions
            result = self._add_contractions(result)
        elif style_config['formal'] > 0.7:
            # More formal: remove contractions
            result = self._remove_contractions(result)
        
        return result
    
    def _add_contractions(self, text: str) -> str:
        contractions = {
            'do not': "don't", 'does not': "doesn't", 'did not': "didn't",
            'is not': "isn't", 'are not': "aren't", 'was not': "wasn't",
            'were not': "weren't", 'have not': "haven't", 'has not': "hasn't",
            'will not': "won't", 'would not': "wouldn't", 'should not': "shouldn't",
            'cannot': "can't", 'could not': "couldn't", 'it is': "it's"
        }
        
        for formal, casual in contractions.items():
            if random.random() < 0.7:  # 70% chance to contract
                pattern = re.compile(re.escape(formal), re.IGNORECASE)
                matches = list(pattern.finditer(text))
                for match in matches:
                    start, end = match.span()
                    replacement = casual if text[start].islower() else casual.capitalize()
                    text = text[:start] + replacement + text[end:]
        
        return text
    
    def _remove_contractions(self, text: str) -> str:
        contractions = {
            "don't": "do not", "doesn't": "does not", "didn't": "did not",
            "isn't": "is not", "aren't": "are not", "wasn't": "was not",
            "weren't": "were not", "haven't": "have not", "hasn't": "has not",
            "won't": "will not", "wouldn't": "would not", "shouldn't": "should not",
            "can't": "cannot", "couldn't": "could not", "it's": "it is"
        }
        
        for casual, formal in contractions.items():
            pattern = re.compile(re.escape(casual), re.IGNORECASE)
            text = pattern.sub(formal, text)
        
        return text
    
    def humanize(
        self,
        text: str,
        strategy: str = 'adaptive',
        num_variations: int = 3,
        return_all: bool = False,
        max_length: int = 512,
        **kwargs
    ) -> Dict:
        """
        Advanced humanization with multiple sophisticated strategies
        
        Args:
            text: Input text to humanize
            strategy: Selection strategy ('adaptive', 'cascade', 'style_transfer', 'mixed')
            num_variations: Number of variations to generate per model
            return_all: Whether to return all variations
            max_length: Maximum length of generated text
        
        Returns:
            Dict with humanized text and comprehensive metrics
        """
        start_time = time.time()
        
        # Analyze text characteristics
        text_analysis = self._analyze_text_characteristics(text)
        print(f"Text analysis: {text_analysis['category']} style, {text_analysis['vocabulary_diversity']:.2f} diversity")
        
        # Initial preprocessing
        cleaned_text = self.preprocessor.clean_text(text)
        cleaned_text = self.advanced_preprocessor.remove_ai_cliches_advanced(cleaned_text)
        
        input_word_count = len(text.split())
        
        # Generate with all models using adaptive parameters
        all_outputs = []
        
        print(f"Generating with {len(self.models)} models using adaptive parameters...")
        
        for model_name in self.models.keys():
            model_outputs = self._generate_with_adaptive_params(
                model_name,
                cleaned_text,
                text_analysis,
                num_return_sequences=num_variations
            )
            
            for output in model_outputs:
                all_outputs.append({
                    'text': output,
                    'model': model_name
                })
            
            print(f"{model_name.upper()}: Generated {len(model_outputs)} variations")
        
        if not all_outputs:
            raise Exception("No models available for generation")
        
        # Filter outputs
        min_length = int(input_word_count * 0.5)
        filtered_outputs = []
        for output in all_outputs:
            word_count = len(output['text'].split())
            if word_count >= min_length:
                filtered_outputs.append(output)
        
        if not filtered_outputs:
            filtered_outputs = all_outputs
        
        print(f"Kept {len(filtered_outputs)} outputs (min {min_length} words)")
        
        # Apply advanced preprocessing to all outputs
        for output in filtered_outputs:
            output['text'] = self.advanced_preprocessor.comprehensive_humanization(output['text'])
            
            # Score output
            metrics = TextMetrics.calculate_comprehensive_score(output['text'], use_gpt2=False)
            output['metrics'] = metrics
            output['score'] = metrics['composite_score']
        
        # Select best output based on strategy
        if return_all:
            variations = [{
                'text': o['text'],
                'model': o['model'],
                'metrics': o['metrics'],
                'score': o['score']
            } for o in filtered_outputs]
            
            return {
                'variations': variations,
                'count': len(variations),
                'strategy': strategy,
                'processing_time': round(time.time() - start_time, 2),
                'input_words': input_word_count
            }
        
        # Apply advanced blending strategies
        if strategy == 'adaptive':
            # Auto-select best strategy based on text analysis
            if text_analysis['vocabulary_diversity'] > 0.6:
                result_text = self._advanced_cascade_blending(filtered_outputs)
            else:
                result_text = self._intelligent_sentence_blending(filtered_outputs)
        elif strategy == 'cascade':
            result_text = self._advanced_cascade_blending(filtered_outputs)
        elif strategy == 'style_transfer':
            best_output = max(filtered_outputs, key=lambda x: x['score'])
            result_text = self._style_transfer_enhancement(best_output['text'], text_analysis['category'])
        else:  # mixed or default
            # Blend multiple strategies
            cascade_output = self._advanced_cascade_blending(filtered_outputs)
            blend_output = self._intelligent_sentence_blending(filtered_outputs)
            
            # Mix both
            cascade_sentences = re.split(r'(?<=[.!?])\s+', cascade_output)
            blend_sentences = re.split(r'(?<=[.!?])\s+', blend_output)
            
            result_text = []
            for i in range(max(len(cascade_sentences), len(blend_sentences))):
                if i < len(cascade_sentences) and random.random() < 0.5:
                    result_text.append(cascade_sentences[i])
                elif i < len(blend_sentences):
                    result_text.append(blend_sentences[i])
            
            result_text = ' '.join(result_text)
        
        # Final refinement with iterative humanization
        def calc_metrics(t):
            return TextMetrics.calculate_comprehensive_score(t, use_gpt2=False)
        
        refined_text, final_metrics, iterations = self.iterative_humanizer.humanize_until_passing(
            result_text, calc_metrics
        )
        
        # Format output
        output_word_count = len(refined_text.split())
        
        return {
            'text': refined_text,
            'original_text': text,
            'model': 'advanced_ensemble',
            'metrics': final_metrics,
            'score': final_metrics['composite_score'],
            'strategy': strategy,
            'processing_time': round(time.time() - start_time, 2),
            'input_words': input_word_count,
            'output_words': output_word_count,
            'length_ratio': round(output_word_count / input_word_count, 2) if input_word_count > 0 else 0,
            'iterations': iterations,
            'text_analysis': text_analysis
        }
    
    def compare_texts(self, original: str, humanized: str) -> Dict:
        """Compare texts with advanced metrics"""
        original_metrics = TextMetrics.calculate_comprehensive_score(original, use_gpt2=False)
        humanized_metrics = TextMetrics.calculate_comprehensive_score(humanized, use_gpt2=False)
        
        improvements = {
            'perplexity': humanized_metrics['perplexity'] - original_metrics['perplexity'],
            'burstiness': humanized_metrics['burstiness'] - original_metrics['burstiness'],
            'bigram_entropy': humanized_metrics['bigram_entropy'] - original_metrics['bigram_entropy'],
            'trigram_entropy': humanized_metrics['trigram_entropy'] - original_metrics['trigram_entropy'],
            'pos_entropy': humanized_metrics['pos_entropy'] - original_metrics['pos_entropy'],
            'semantic_coherence': humanized_metrics['semantic_coherence'] - original_metrics['semantic_coherence'],
            'composite_score': humanized_metrics['composite_score'] - original_metrics['composite_score']
        }
        
        return {
            'original': original_metrics,
            'humanized': humanized_metrics,
            'improvements': improvements,
            'improvement_percentage': {
                'perplexity': round((improvements['perplexity'] / original_metrics['perplexity'] * 100) if original_metrics['perplexity'] > 0 else 0, 2),
                'burstiness': round((improvements['burstiness'] / original_metrics['burstiness'] * 100) if original_metrics['burstiness'] > 0 else 0, 2),
                'composite_score': round((improvements['composite_score'] / original_metrics['composite_score'] * 100) if original_metrics['composite_score'] > 0 else 0, 2)
            }
        }
    
    def get_model_info(self) -> Dict:
        """Get information about loaded models"""
        return {
            'models_loaded': list(self.models.keys()),
            'model_count': len(self.models),
            'device': self.device,
            'bart_model': Config.BART_MODEL if 'bart' in self.models else None,
            't5_model': Config.T5_MODEL if 't5' in self.models else None,
            'pegasus_model': Config.PEGASUS_MODEL if 'pegasus' in self.models else None,
            'strategies_available': ['adaptive', 'cascade', 'style_transfer', 'mixed'],
            'features': ['adaptive_parameters', 'cascade_blending', 'style_transfer', 'iterative_refinement']
        }
