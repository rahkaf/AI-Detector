"""
Advanced Text Preprocessing for Maximum Humanization
Based on research: perplexity scaling, burstiness optimization, stylometric manipulation
"""
import re
import random
from typing import List, Dict, Tuple

class AdvancedPreprocessor:
    """
    Advanced preprocessing techniques to maximize human-likeness
    """
    
    # Expanded AI clichés list (from research)
    AI_CLICHES = {
        'delve': ['explore', 'examine', 'investigate', 'look into', 'study'],
        'delve into': ['explore', 'examine', 'dig into', 'investigate'],
        'comprehensive': ['complete', 'thorough', 'full', 'detailed', 'extensive'],
        'tapestry': ['mix', 'blend', 'combination', 'mixture', 'array'],
        'unveiling': ['revealing', 'showing', 'exposing', 'disclosing'],
        'seamless': ['smooth', 'easy', 'effortless', 'fluid'],
        'leverage': ['use', 'utilize', 'employ', 'apply', 'harness'],
        'robust': ['strong', 'solid', 'sturdy', 'powerful', 'effective'],
        'paradigm': ['model', 'framework', 'approach', 'system'],
        'synergy': ['cooperation', 'collaboration', 'teamwork', 'partnership'],
        'holistic': ['complete', 'comprehensive', 'integrated', 'unified'],
        'furthermore': ['also', 'additionally', 'plus', 'and', 'besides'],
        'moreover': ['also', 'additionally', 'plus', 'what\'s more'],
        'in conclusion': ['finally', 'to sum up', 'in the end', 'ultimately'],
        'it is important to note': ['note that', 'importantly', 'notably'],
        'in today\'s digital landscape': ['today', 'nowadays', 'currently'],
        'navigate': ['handle', 'manage', 'deal with', 'work through'],
        'crucial': ['important', 'key', 'vital', 'essential', 'critical'],
        'pivotal': ['key', 'crucial', 'important', 'central'],
        'multifaceted': ['complex', 'varied', 'diverse', 'multi-layered'],
        'underscore': ['highlight', 'emphasize', 'stress', 'show'],
        'facilitate': ['help', 'enable', 'assist', 'support'],
        'utilize': ['use', 'employ', 'apply'],
        'implement': ['use', 'apply', 'put in place', 'set up'],
        'optimize': ['improve', 'enhance', 'better', 'refine'],
    }
    
    @staticmethod
    def remove_ai_cliches_advanced(text: str) -> str:
        """
        Advanced cliché removal with context-aware replacements
        """
        for cliche, replacements in AdvancedPreprocessor.AI_CLICHES.items():
            if cliche in text.lower():
                # Choose random replacement for variety
                replacement = random.choice(replacements)
                
                # Case-insensitive replacement preserving original case
                pattern = re.compile(re.escape(cliche), re.IGNORECASE)
                
                def replace_with_case(match):
                    original = match.group(0)
                    if original[0].isupper():
                        return replacement.capitalize()
                    return replacement
                
                text = pattern.sub(replace_with_case, text)
        
        return text
    
    @staticmethod
    def increase_burstiness(text: str) -> str:
        """
        Dramatically increase sentence length variation
        Combines short sentences, splits long ones
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return text
        
        new_sentences = []
        i = 0
        
        while i < len(sentences):
            sentence = sentences[i]
            words = sentence.split()
            
            # If sentence is medium length (10-20 words), randomly split or combine
            if 10 <= len(words) <= 20:
                if random.random() > 0.5 and i + 1 < len(sentences):
                    # Combine with next sentence
                    next_sentence = sentences[i + 1]
                    combined = f"{sentence} {next_sentence}"
                    new_sentences.append(combined)
                    i += 2
                else:
                    new_sentences.append(sentence)
                    i += 1
            
            # If sentence is long (>20 words), split it
            elif len(words) > 20:
                # Find a good split point (after a comma or conjunction)
                split_point = len(words) // 2
                
                # Look for comma near middle
                for j in range(split_point - 3, split_point + 3):
                    if j < len(words) and words[j].endswith(','):
                        split_point = j + 1
                        break
                
                # Split sentence
                first_part = ' '.join(words[:split_point])
                second_part = ' '.join(words[split_point:])
                
                # Ensure proper punctuation
                if not first_part.endswith(('.', '!', '?')):
                    first_part += '.'
                if second_part and second_part[0].islower():
                    second_part = second_part[0].upper() + second_part[1:]
                
                new_sentences.append(first_part)
                new_sentences.append(second_part)
                i += 1
            
            # If sentence is short (<10 words), keep as is
            else:
                new_sentences.append(sentence)
                i += 1
        
        return ' '.join(new_sentences)
    
    @staticmethod
    def add_linguistic_noise(text: str) -> str:
        """
        Add natural linguistic "imperfections" that humans make
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        modified_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Randomly start sentences with conjunctions (10% chance)
            if i > 0 and random.random() < 0.1:
                conjunctions = ['And', 'But', 'So', 'Yet', 'Or']
                if not sentence.split()[0] in conjunctions:
                    sentence = f"{random.choice(conjunctions)} {sentence.lower()}"
            
            # Randomly add filler words (5% chance)
            if random.random() < 0.05:
                fillers = ['actually', 'basically', 'essentially', 'really', 'quite']
                words = sentence.split()
                if len(words) > 3:
                    insert_pos = random.randint(1, min(3, len(words) - 1))
                    words.insert(insert_pos, random.choice(fillers))
                    sentence = ' '.join(words)
            
            # Randomly use em dashes instead of commas (5% chance)
            if random.random() < 0.05 and ',' in sentence:
                sentence = sentence.replace(',', ' —', 1)
            
            modified_sentences.append(sentence)
        
        return ' '.join(modified_sentences)
    
    @staticmethod
    def vary_sentence_structure(text: str) -> str:
        """
        Vary sentence openings and structures
        AI tends to start sentences similarly
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        modified_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) < 5:
                modified_sentences.append(sentence)
                continue
            
            # Randomly invert sentence structure (10% chance)
            if random.random() < 0.1:
                # If sentence starts with "The X is/was", try inverting
                if words[0].lower() == 'the' and len(words) > 3:
                    if words[2].lower() in ['is', 'was', 'are', 'were']:
                        # Invert: "The X is Y" -> "Y is the X"
                        inverted = f"{' '.join(words[3:])} {words[2]} {words[0]} {words[1]}"
                        if inverted[0].islower():
                            inverted = inverted[0].upper() + inverted[1:]
                        modified_sentences.append(inverted)
                        continue
            
            modified_sentences.append(sentence)
        
        return ' '.join(modified_sentences)
    
    @staticmethod
    def add_contractions_strategically(text: str) -> str:
        """
        Add contractions strategically (not all, for variety)
        """
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
            'must not': "mustn't",
            'need not': "needn't",
            'dare not': "daren't",
            'it is': "it's",
            'that is': "that's",
            'there is': "there's",
            'what is': "what's",
            'who is': "who's",
            'where is': "where's",
            'when is': "when's",
            'why is': "why's",
            'how is': "how's",
        }
        
        # Apply contractions randomly (50% chance for each)
        for formal, casual in contractions.items():
            if formal in text.lower():
                # Find all occurrences
                pattern = re.compile(re.escape(formal), re.IGNORECASE)
                matches = list(pattern.finditer(text))
                
                # Replace only some of them (50% chance each)
                for match in matches:
                    if random.random() < 0.5:
                        start, end = match.span()
                        replacement = casual if text[start].islower() else casual.capitalize()
                        text = text[:start] + replacement + text[end:]
        
        return text
    
    @staticmethod
    def reduce_passive_voice(text: str) -> str:
        """
        Convert passive voice to active voice
        AI overuses passive voice
        """
        # Common passive patterns
        passive_patterns = [
            (r'(\w+) was (\w+ed) by', r'by \1 \2'),  # "X was done by Y" -> "Y did X"
            (r'(\w+) is (\w+ed) by', r'by \1 \2'),
            (r'(\w+) are (\w+ed) by', r'by \1 \2'),
            (r'(\w+) were (\w+ed) by', r'by \1 \2'),
        ]
        
        for pattern, replacement in passive_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    @staticmethod
    def add_idiomatic_expressions(text: str) -> str:
        """
        Add natural idiomatic expressions
        AI rarely uses idioms
        """
        idioms = {
            'very important': 'crucial',
            'very good': 'excellent',
            'very bad': 'terrible',
            'very big': 'huge',
            'very small': 'tiny',
            'a lot of': 'plenty of',
            'many': 'numerous',
        }
        
        # Apply some idioms (30% chance)
        for phrase, idiom in idioms.items():
            if phrase in text.lower() and random.random() < 0.3:
                pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                text = pattern.sub(idiom, text, count=1)
        
        return text
    
    @staticmethod
    def comprehensive_humanization(text: str) -> str:
        """
        Apply ALL humanization techniques in optimal order
        """
        # Step 1: Remove AI clichés
        text = AdvancedPreprocessor.remove_ai_cliches_advanced(text)
        
        # Step 2: Increase burstiness
        text = AdvancedPreprocessor.increase_burstiness(text)
        
        # Step 3: Add linguistic noise
        text = AdvancedPreprocessor.add_linguistic_noise(text)
        
        # Step 4: Vary sentence structure
        text = AdvancedPreprocessor.vary_sentence_structure(text)
        
        # Step 5: Add contractions
        text = AdvancedPreprocessor.add_contractions_strategically(text)
        
        # Step 6: Reduce passive voice
        text = AdvancedPreprocessor.reduce_passive_voice(text)
        
        # Step 7: Add idiomatic expressions
        text = AdvancedPreprocessor.add_idiomatic_expressions(text)
        
        # Step 8: Final cleanup
        text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)  # Ensure spacing after punctuation
        
        return text.strip()




class IterativeHumanizer:
    """Iterative humanization with feedback loop"""
    
    def __init__(self, target_score=75.0, max_iterations=3):
        self.target_score = target_score
        self.max_iterations = max_iterations
    
    def humanize_until_passing(self, text, metrics_calculator):
        """Keep humanizing until the text passes detection threshold"""
        current_text = text
        iterations = 0
        
        for i in range(self.max_iterations):
            iterations = i + 1
            metrics = metrics_calculator(current_text)
            current_score = metrics.get('composite_score', 0)
            print(f'Iteration {iterations}: Score = {current_score:.1f}')
            
            if current_score >= self.target_score:
                print(f'Target score reached after {iterations} iteration(s)')
                return current_text, metrics, iterations
            
            current_text = AdvancedPreprocessor.comprehensive_humanization(current_text)
        
        final_metrics = metrics_calculator(current_text)
        print(f'Max iterations reached. Final score: {final_metrics.get("composite_score", 0):.1f}')
        return current_text, final_metrics, iterations
