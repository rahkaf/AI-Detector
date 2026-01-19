"""
Recursive Paraphrasing & Multi-Pass Humanization
Research shows passing text through multiple models/iterations degrades AI signatures
"""
import random
from typing import List, Dict, Tuple, Callable

class RecursiveHumanizer:
    """
    Implements recursive paraphrasing attacks to degrade AI watermarks
    Passes text through multiple transformations to break detection patterns
    """
    
    def __init__(self, min_passes: int = 2, max_passes: int = 4):
        """
        Args:
            min_passes: Minimum number of recursive passes
            max_passes: Maximum number of recursive passes
        """
        self.min_passes = min_passes
        self.max_passes = max_passes
    
    def recursive_paraphrase(
        self, 
        text: str, 
        paraphrase_functions: List[Callable],
        metrics_calculator: Callable,
        target_score: float = 75.0
    ) -> Tuple[str, List[Dict], int]:
        """
        Recursively paraphrase text through multiple models/functions
        Each pass uses a different transformation to break AI patterns
        
        Args:
            text: Input text
            paraphrase_functions: List of paraphrasing functions to cycle through
            metrics_calculator: Function to calculate detection metrics
            target_score: Target composite score to achieve
        
        Returns:
            Tuple of (final_text, pass_history, total_passes)
        """
        current_text = text
        pass_history = []
        num_passes = random.randint(self.min_passes, self.max_passes)
        
        print(f"🔄 Starting recursive paraphrasing: {num_passes} passes planned")
        
        for pass_num in range(num_passes):
            # Select paraphrase function (cycle through available ones)
            func_idx = pass_num % len(paraphrase_functions)
            paraphrase_func = paraphrase_functions[func_idx]
            
            print(f"  Pass {pass_num + 1}/{num_passes}: Using function {func_idx}")
            
            # Apply paraphrasing
            try:
                paraphrased = paraphrase_func(current_text)
            except Exception as e:
                print(f"  ⚠️ Error in pass {pass_num + 1}: {e}")
                paraphrased = current_text
            
            # Calculate metrics
            metrics = metrics_calculator(paraphrased)
            score = metrics.get('composite_score', 0)
            
            # Record this pass
            pass_history.append({
                'pass_number': pass_num + 1,
                'function_used': func_idx,
                'score': score,
                'perplexity': metrics.get('perplexity', 0),
                'burstiness': metrics.get('burstiness', 0),
                'text_length': len(paraphrased.split())
            })
            
            print(f"    Score: {score:.1f} | Perplexity: {metrics.get('perplexity', 0):.1f} | Burstiness: {metrics.get('burstiness', 0):.1f}")
            
            # Update current text
            current_text = paraphrased
            
            # Early exit if target reached
            if score >= target_score:
                print(f"  ✅ Target score {target_score} reached at pass {pass_num + 1}")
                break
        
        final_metrics = metrics_calculator(current_text)
        print(f"🎯 Final score after {len(pass_history)} passes: {final_metrics.get('composite_score', 0):.1f}")
        
        return current_text, pass_history, len(pass_history)
    
    def multi_model_cascade(
        self,
        text: str,
        model_outputs: List[str],
        humanize_func: Callable,
        metrics_calculator: Callable
    ) -> Tuple[str, Dict]:
        """
        Cascade through multiple model outputs, selecting best at each stage
        Then apply recursive humanization
        
        Args:
            text: Original text
            model_outputs: List of paraphrased outputs from different models
            humanize_func: Function to humanize text
            metrics_calculator: Function to calculate metrics
        
        Returns:
            Tuple of (best_humanized_text, metrics)
        """
        print(f"🔀 Multi-model cascade: {len(model_outputs)} outputs")
        
        # Score all model outputs
        scored_outputs = []
        for i, output in enumerate(model_outputs):
            metrics = metrics_calculator(output)
            scored_outputs.append({
                'text': output,
                'score': metrics.get('composite_score', 0),
                'model_idx': i
            })
        
        # Sort by score
        scored_outputs.sort(key=lambda x: x['score'], reverse=True)
        
        # Take top 3 and blend them
        top_outputs = scored_outputs[:min(3, len(scored_outputs))]
        
        print(f"  Top scores: {[f\"{o['score']:.1f}\" for o in top_outputs]}")
        
        # Blend top outputs by alternating sentences
        blended = self._blend_outputs([o['text'] for o in top_outputs])
        
        # Apply humanization
        humanized = humanize_func(blended)
        
        # Calculate final metrics
        final_metrics = metrics_calculator(humanized)
        
        return humanized, final_metrics
    
    def _blend_outputs(self, texts: List[str]) -> str:
        """Blend multiple texts by alternating sentences"""
        import re
        
        # Split all texts into sentences
        all_sentences = []
        for text in texts:
            sentences = re.split(r'(?<=[.!?])\s+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            all_sentences.append(sentences)
        
        # Alternate between texts
        blended = []
        max_len = max(len(s) for s in all_sentences)
        
        for i in range(max_len):
            for sentences in all_sentences:
                if i < len(sentences):
                    blended.append(sentences[i])
        
        return ' '.join(blended)
    
    def statistical_randomization_pass(
        self,
        text: str,
        temperature_range: Tuple[float, float] = (1.5, 2.0),
        top_p_range: Tuple[float, float] = (0.95, 0.99)
    ) -> Dict[str, float]:
        """
        Generate randomization parameters for next pass
        Varies temperature and top_p to increase unpredictability
        
        Returns:
            Dict with sampling parameters
        """
        return {
            'temperature': random.uniform(*temperature_range),
            'top_p': random.uniform(*top_p_range),
            'top_k': random.randint(100, 200),
            'repetition_penalty': random.uniform(1.2, 1.5),
        }
    
    def adaptive_recursive_humanization(
        self,
        text: str,
        paraphrase_func: Callable,
        humanize_func: Callable,
        metrics_calculator: Callable,
        target_score: float = 75.0,
        max_attempts: int = 5
    ) -> Tuple[str, List[Dict], bool]:
        """
        Adaptive recursive approach: adjusts strategy based on metrics
        
        Args:
            text: Input text
            paraphrase_func: Function to paraphrase (takes text + params)
            humanize_func: Function to humanize
            metrics_calculator: Function to calculate metrics
            target_score: Target composite score
            max_attempts: Maximum recursive attempts
        
        Returns:
            Tuple of (final_text, attempt_history, success)
        """
        current_text = text
        attempt_history = []
        
        print(f"🎯 Adaptive recursive humanization (target: {target_score})")
        
        for attempt in range(max_attempts):
            # Generate randomization parameters
            params = self.statistical_randomization_pass()
            
            print(f"  Attempt {attempt + 1}/{max_attempts}")
            print(f"    Params: temp={params['temperature']:.2f}, top_p={params['top_p']:.2f}")
            
            # Paraphrase with random parameters
            try:
                paraphrased = paraphrase_func(current_text, **params)
            except TypeError:
                # If function doesn't accept params, use without
                paraphrased = paraphrase_func(current_text)
            
            # Humanize
            humanized = humanize_func(paraphrased)
            
            # Calculate metrics
            metrics = metrics_calculator(humanized)
            score = metrics.get('composite_score', 0)
            
            # Record attempt
            attempt_history.append({
                'attempt': attempt + 1,
                'score': score,
                'perplexity': metrics.get('perplexity', 0),
                'burstiness': metrics.get('burstiness', 0),
                'params': params,
                'detection_resistance': metrics.get('detection_resistance', 'UNKNOWN')
            })
            
            print(f"    Score: {score:.1f} | Resistance: {metrics.get('detection_resistance', 'UNKNOWN')}")
            
            # Update current text
            current_text = humanized
            
            # Check if target reached
            if score >= target_score:
                print(f"  ✅ Target reached at attempt {attempt + 1}")
                return current_text, attempt_history, True
        
        print(f"  ⚠️ Target not reached after {max_attempts} attempts")
        return current_text, attempt_history, False


class GrammarImperfectionInjector:
    """
    Injects natural human grammar imperfections
    AI models rarely produce these patterns
    """
    
    @staticmethod
    def inject_natural_imperfections(text: str, intensity: float = 0.3) -> str:
        """
        Add natural human writing imperfections
        
        Args:
            text: Input text
            intensity: How many imperfections to add (0.0-1.0)
        
        Returns:
            Text with natural imperfections
        """
        import re
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        modified = []
        
        for i, sentence in enumerate(sentences):
            # Apply various imperfections based on intensity
            
            # 1. Occasional comma splices (joining independent clauses with comma)
            if random.random() < intensity * 0.2 and i < len(sentences) - 1:
                # Join with next sentence using comma
                next_sent = sentences[i + 1] if i + 1 < len(sentences) else None
                if next_sent and len(sentence.split()) > 5:
                    sentence = sentence.rstrip('.!?') + ', ' + next_sent[0].lower() + next_sent[1:]
                    sentences[i + 1] = ''  # Mark as used
            
            # 2. Missing oxford comma (human inconsistency)
            if random.random() < intensity * 0.3:
                # "A, B, and C" -> "A, B and C"
                sentence = re.sub(r',\s+and\s+', ' and ', sentence, count=1)
            
            # 3. Informal ellipsis usage
            if random.random() < intensity * 0.15:
                # Add ellipsis for trailing thought
                if sentence.endswith('.'):
                    sentence = sentence[:-1] + '...'
            
            # 4. Parenthetical asides (very human)
            if random.random() < intensity * 0.2 and len(sentence.split()) > 10:
                words = sentence.split()
                insert_pos = random.randint(3, len(words) - 3)
                asides = [
                    '(at least in my view)',
                    '(though I could be wrong)',
                    '(surprisingly)',
                    '(interestingly enough)',
                    '(to be fair)',
                ]
                words.insert(insert_pos, random.choice(asides))
                sentence = ' '.join(words)
            
            # 5. Sentence fragments (intentional)
            if random.random() < intensity * 0.1 and i > 0:
                fragments = [
                    'Which is interesting.',
                    'Pretty cool, right?',
                    'Not always, though.',
                    'At least sometimes.',
                    'Or so it seems.',
                ]
                modified.append(random.choice(fragments))
            
            # 6. Informal intensifiers
            if random.random() < intensity * 0.25:
                intensifiers = {
                    'very': 'super',
                    'really': 'pretty',
                    'extremely': 'crazy',
                    'significantly': 'way',
                }
                for formal, informal in intensifiers.items():
                    if formal in sentence.lower():
                        sentence = re.sub(
                            r'\b' + formal + r'\b',
                            informal,
                            sentence,
                            count=1,
                            flags=re.IGNORECASE
                        )
                        break
            
            if sentence:  # Only add non-empty sentences
                modified.append(sentence)
        
        return ' '.join(modified)
    
    @staticmethod
    def add_stylistic_inconsistencies(text: str) -> str:
        """
        Add minor stylistic inconsistencies that humans naturally produce
        - Inconsistent capitalization of certain terms
        - Mixed number formatting (10 vs ten)
        - Varied punctuation spacing
        """
        import re
        
        # Inconsistent number formatting
        # Sometimes spell out small numbers, sometimes use digits
        def random_number_format(match):
            num = int(match.group(0))
            if num <= 10 and random.random() < 0.5:
                words = ['zero', 'one', 'two', 'three', 'four', 'five',
                        'six', 'seven', 'eight', 'nine', 'ten']
                return words[num]
            return match.group(0)
        
        text = re.sub(r'\b([0-9]|10)\b', random_number_format, text)
        
        # Inconsistent em dash usage (sometimes with spaces, sometimes without)
        if '—' in text:
            parts = text.split('—')
            text = random.choice([' — ', '—', ' —']).join(parts)
        
        # Occasional double space after period (old typing habit)
        if random.random() < 0.2:
            text = re.sub(r'\.\s+', '.  ', text, count=1)
        
        return text
