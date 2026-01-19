"""
Enhanced Preprocessing with Syntactic Restructuring and Context-Aware Transformations
Designed for maximum AI detection evasion
"""
import re
import random
from typing import List, Dict, Tuple
from collections import Counter


class EnhancedPreprocessor:
    """
    Advanced preprocessing with syntactic restructuring
    """
    
    # Expanded AI clichés - more comprehensive list
    AI_CLICHES = {
        'delve': ['explore', 'examine', 'investigate', 'look into', 'study', 'dive into'],
        'delve into': ['explore', 'examine', 'dig into', 'investigate', 'dive into'],
        'comprehensive': ['complete', 'thorough', 'full', 'detailed', 'extensive', 'in-depth'],
        'tapestry': ['mix', 'blend', 'combination', 'mixture', 'array', 'collection'],
        'unveiling': ['revealing', 'showing', 'exposing', 'disclosing', 'presenting', 'displaying'],
        'seamless': ['smooth', 'easy', 'effortless', 'fluid', 'natural', 'integrated'],
        'leverage': ['use', 'utilize', 'employ', 'apply', 'harness', 'make use of', 'exploit'],
        'robust': ['strong', 'solid', 'sturdy', 'powerful', 'effective', 'reliable', 'durable'],
        'paradigm': ['model', 'framework', 'approach', 'system', 'method', 'pattern'],
        'synergy': ['cooperation', 'collaboration', 'teamwork', 'partnership', 'joint effort', 'combined effort'],
        'holistic': ['complete', 'comprehensive', 'integrated', 'unified', 'total', 'overall'],
        'furthermore': ['also', 'additionally', 'plus', 'and', 'besides', 'moreover', 'what\'s more'],
        'moreover': ['also', 'additionally', 'plus', 'what\'s more', 'besides'],
        'in conclusion': ['finally', 'to sum up', 'in the end', 'ultimately', 'to wrap up', 'in summary'],
        'it is important to note': ['note that', 'importantly', 'notably', 'keep in mind', 'remember that'],
        'in today\'s digital landscape': ['today', 'nowadays', 'currently', 'in this digital age', 'in our time'],
        'navigate': ['handle', 'manage', 'deal with', 'work through', 'get around', 'find one\'s way through'],
        'crucial': ['important', 'key', 'vital', 'essential', 'critical', 'significant'],
        'pivotal': ['key', 'crucial', 'important', 'central', 'essential', 'significant'],
        'multifaceted': ['complex', 'varied', 'diverse', 'multi-layered', 'many-sided', 'intricate'],
        'underscore': ['highlight', 'emphasize', 'stress', 'show', 'point out', 'call attention to'],
        'facilitate': ['help', 'enable', 'assist', 'support', 'make easier', 'simplify'],
        'utilize': ['use', 'employ', 'apply', 'make use of', 'leverage'],
        'implement': ['use', 'apply', 'put in place', 'set up', 'establish', 'introduce'],
        'optimize': ['improve', 'enhance', 'better', 'refine', 'make the most of', 'maximize'],
        'foster': ['encourage', 'promote', 'support', 'help', 'nurture', 'build'],
        'streamline': ['simplify', 'make efficient', 'improve', 'smooth out', 'organize'],
        'revolutionize': ['change', 'transform', 'improve dramatically', 'completely change'],
        'game-changer': ['important innovation', 'significant improvement', 'major breakthrough'],
        'cutting-edge': ['modern', 'advanced', 'latest', 'state-of-the-art', 'innovative'],
        'groundbreaking': ['innovative', 'new', 'original', 'revolutionary'],
        'landscape': ['environment', 'situation', 'context', 'setting', 'field'],
        'ecosystem': ['environment', 'system', 'network', 'community', 'setting'],
        'empower': ['enable', 'help', 'support', 'give power to', 'strengthen'],
        'scalable': ['flexible', 'adaptable', 'expandable', 'growable'],
        'innovative': ['new', 'creative', 'original', 'fresh', 'novel'],
        'dynamic': ['changing', 'active', 'lively', 'energetic'],
        'essential': ['important', 'key', 'necessary', 'vital', 'critical'],
        'substantial': ['significant', 'considerable', 'notable', 'important', 'major'],
        'significant': ['important', 'major', 'notable', 'considerable', 'meaningful'],
    }
    
    @staticmethod
    def remove_ai_cliches_advanced(text: str) -> str:
        """
        Advanced cliché removal with context-aware replacements
        Prioritizes variety and natural-sounding alternatives
        """
        for cliche, replacements in EnhancedPreprocessor.AI_CLICHES.items():
            if cliche in text.lower():
                # Weighted random selection - prefer natural-sounding words
                replacement = random.choice(replacements)
                
                # Case-insensitive replacement preserving original case
                pattern = re.compile(r'\b' + re.escape(cliche) + r'\b', re.IGNORECASE)
                
                def replace_with_case(match):
                    original = match.group(0)
                    if original[0].isupper():
                        return replacement.capitalize()
                    return replacement
                
                text = pattern.sub(replace_with_case, text)
        
        return text
    
    @staticmethod
    def syntactic_restructuring(text: str) -> str:
        """
        Advanced syntactic restructuring to break AI-like patterns
        Includes sentence reordering, clause manipulation, and structural changes
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        restructured = []
        for i, sentence in enumerate(sentences):
            # Only restructure some sentences (30% chance) for natural feel
            if random.random() < 0.3:
                sentence = EnhancedPreprocessor._restructure_sentence(sentence)
            restructured.append(sentence)
        
        # Occasionally reorder clauses (10% chance)
        if len(restructured) > 2 and random.random() < 0.1:
            idx1, idx2 = random.sample(range(len(restructured)), 2)
            restructured[idx1], restructured[idx2] = restructured[idx2], restructured[idx1]
        
        return ' '.join(restructured)
    
    @staticmethod
    def _restructure_sentence(sentence: str) -> str:
        """Restructure a single sentence"""
        words = sentence.split()
        if len(words) < 5:
            return sentence
        
        # Strategy 1: Move prepositional phrases
        if ' in ' in sentence.lower() or ' on ' in sentence.lower():
            parts = re.split(r' [io]n ', sentence, maxsplit=1)
            if len(parts) == 2:
                if random.random() < 0.5:
                    # Move phrase to end
                    return f"{parts[1]}, {parts[0]}"
        
        # Strategy 2: Split compound sentences
        connectors = [' and ', ' but ', ' or ', ' so ', ' yet ', ' for ', ' nor ']
        for connector in connectors:
            if connector in sentence:
                parts = sentence.split(connector, 1)
                if len(parts) == 2:
                    if len(parts[0].split()) > 5 and len(parts[1].split()) > 5:
                        # Split into two sentences
                        part1 = parts[0].strip()
                        part2 = parts[1].strip()
                        if not part1.endswith(('.', '!', '?')):
                            part1 += '.'
                        if not part2[0].isupper():
                            part2 = part2[0].upper() + part2[1:]
                        return f"{part1} {connector.strip()} {part2}"
        
        # Strategy 3: Invert subject-verb-object structure
        if words[0].lower() in ['the', 'a', 'an']:
            if len(words) > 4:
                verb_idx = None
                for i, word in enumerate(words[2:], start=2):
                    if word.lower() in ['is', 'was', 'are', 'were', 'has', 'have', 'had']:
                        verb_idx = i
                        break
                
                if verb_idx and verb_idx < len(words) - 1:
                    subject = ' '.join(words[:verb_idx])
                    predicate = ' '.join(words[verb_idx+1:])
                    verb = words[verb_idx]
                    
                    # Create inverted structure
                    inverted = f"{predicate} {verb.lower()} {subject}"
                    if inverted[0].islower():
                        inverted = inverted[0].upper() + inverted[1:]
                    
                    # 40% chance to apply inversion
                    if random.random() < 0.4:
                        return inverted
        
        return sentence
    
    @staticmethod
    def enhance_burstiness_dramatic(text: str) -> str:
        """
        Dramatically increase burstiness with aggressive sentence manipulation
        Creates more variation in sentence length and structure
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return text
        
        enhanced = []
        i = 0
        
        while i < len(sentences):
            sentence = sentences[i]
            words = sentence.split()
            
            # Very short sentences (< 8 words) - occasionally combine
            if len(words) < 8 and random.random() < 0.4 and i + 1 < len(sentences):
                next_sentence = sentences[i + 1]
                if len(next_sentence.split()) < 15:
                    connector = random.choice([', and', ', but', ', so', ''])
                    combined = f"{sentence}{connector} {next_sentence}"
                    enhanced.append(combined)
                    i += 2
                    continue
            
            # Medium sentences (8-18 words) - split or keep
            elif 8 <= len(words) <= 18:
                if random.random() < 0.3:
                    # Split sentence
                    split_point = len(words) // 2
                    # Find good split point (after comma or conjunction)
                    for j in range(split_point - 2, split_point + 2):
                        if j < len(words) and (words[j].endswith(',') or words[j].lower() in ['and', 'but', 'or']):
                            split_point = j + 1
                            break
                    
                    part1 = ' '.join(words[:split_point])
                    part2 = ' '.join(words[split_point:])
                    
                    if not part1.endswith(('.', '!', '?', ',')):
                        part1 += ','
                    if part2 and part2[0].islower():
                        part2 = part2[0].upper() + part2[1:]
                    if not part2.endswith(('.', '!', '?')):
                        part2 += '.'
                    
                    enhanced.append(part1)
                    enhanced.append(part2)
                    i += 1
                    continue
                else:
                    enhanced.append(sentence)
                    i += 1
            
            # Long sentences (> 18 words) - definitely split
            elif len(words) > 18:
                split_point = random.randint(6, 12)
                
                # Find comma or conjunction near split point
                for j in range(split_point - 2, split_point + 2):
                    if j < len(words) and (words[j].endswith(',') or words[j].lower() in ['and', 'but', 'or']):
                        split_point = j + 1
                        break
                
                part1 = ' '.join(words[:split_point])
                part2 = ' '.join(words[split_point:])
                
                if not part1.endswith(('.', '!', '?', ',')):
                    part1 += ','
                if part2 and part2[0].islower():
                    part2 = part2[0].upper() + part2[1:]
                if not part2.endswith(('.', '!', '?')):
                    part2 += '.'
                
                enhanced.append(part1)
                enhanced.append(part2)
                i += 1
            else:
                enhanced.append(sentence)
                i += 1
        
        return ' '.join(enhanced)
    
    @staticmethod
    def add_contextual_variations(text: str) -> str:
        """
        Add contextual variations to break predictable patterns
        Uses smart replacements based on sentence context
        """
        # Context-aware replacements
        replacements = [
            # Transition words
            (r'\bhowever\b', ['but', 'yet', 'still', 'on the other hand', 'though']),
            (r'\btherefore\b', ['so', 'thus', 'hence', 'as a result', 'that\'s why']),
            (r'\bmeanwhile\b', ['at the same time', 'while this happens', 'during this time']),
            (r'\bconsequently\b', ['so', 'as a result', 'therefore', 'that\'s why']),
            
            # Common phrases
            (r'\bit is clear that\b', ['clearly', 'obviously', 'it\'s obvious that']),
            (r'\bit should be noted that\b', ['note that', 'remember', 'keep in mind']),
            (r'\bin order to\b', ['to', 'for the purpose of', 'so as to']),
            (r'\bfor example\b', ['for instance', 'such as', 'like']),
            (r'\bsuch as\b', ['including', 'like', 'for example', 'such']),
            
            # Academic phrases
            (r'\bdue to the fact that\b', ['because', 'since', 'as']),
            (r'\bin spite of\b', ['despite', 'even though', 'notwithstanding']),
            (r'\bin addition to\b', ['besides', 'also', 'plus', 'along with']),
            (r'\bwith regard to\b', ['about', 'regarding', 'concerning', 'as for']),
        ]
        
        for pattern, options in replacements:
            if pattern in text.lower():
                # Apply replacement with 30% probability
                if random.random() < 0.3:
                    regex = re.compile(pattern, re.IGNORECASE)
                    
                    def replace_with_case(match):
                        original = match.group(0)
                        replacement = random.choice(options)
                        if original[0].isupper():
                            replacement = replacement.capitalize()
                        return replacement
                    
                    text = regex.sub(replace_with_case, text, count=1)
        
        return text
    
    @staticmethod
    def inject_linguistic_noise_advanced(text: str) -> str:
        """
        Advanced linguistic noise injection for more natural feel
        Includes subtle imperfections humans make
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        noisy_sentences = []
        
        for i, sentence in enumerate(sentences):
            words = sentence.split()
            
            # 1. Occasional sentence fragments (5% chance)
            if len(words) > 8 and random.random() < 0.05:
                # Remove the last word occasionally
                if words[-1].lower() not in ['the', 'a', 'an', 'to', 'in', 'on']:
                    words = words[:-1]
                    sentence = ' '.join(words)
            
            # 2. Conversational fillers (8% chance)
            if len(words) > 5 and random.random() < 0.08:
                fillers = ['I mean', 'like', 'you know', 'basically', 'actually', 'sort of']
                insert_pos = random.randint(1, min(4, len(words) - 1))
                filler = random.choice(fillers)
                words.insert(insert_pos, f"{filler},")
                sentence = ' '.join(words)
            
            # 3. Parenthetical asides (6% chance)
            if len(words) > 8 and random.random() < 0.06:
                aside_options = [
                    'by the way', 'incidentally', 'interestingly', 'notably', 'though'
                ]
                aside = random.choice(aside_options)
                insert_pos = random.randint(2, len(words) - 3)
                words.insert(insert_pos, f"({aside})")
                sentence = ' '.join(words)
            
            # 4. Dash usage instead of commas (7% chance)
            if ',' in sentence and random.random() < 0.07:
                # Replace first comma with em-dash
                sentence = sentence.replace(',', ' —', 1)
            
            # 5. Ellipsis for emphasis (3% chance)
            if len(words) > 10 and random.random() < 0.03:
                sentence = sentence.replace('.', '...')
            
            noisy_sentences.append(sentence)
        
        return ' '.join(noisy_sentences)
    
    @staticmethod
    def vary_sentence_openings(text: str) -> str:
        """
        Dramatically vary sentence openings to break AI patterns
        AI tends to start sentences similarly
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        varied = []
        opening_history = []
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) < 3:
                varied.append(sentence)
                continue
            
            first_word = words[0].lower()
            
            # Check if this opening is overused
            if first_word in opening_history:
                # Try to vary the opening
                variations = {
                    'the': ['', 'a', 'an', 'this', 'that', 'these', 'those'],
                    'a': ['', 'an', 'the', 'this', 'that', 'some'],
                    'an': ['', 'a', 'the', 'this', 'that', 'some'],
                    'it': ['', 'this', 'that', 'there', 'here'],
                    'this': ['', 'that', 'it', 'the', 'a'],
                    'that': ['', 'this', 'it', 'the', 'a'],
                    'there': ['', 'here', 'it', 'this', 'that'],
                    'in': ['', 'at', 'on', 'during', 'within'],
                    'on': ['', 'in', 'at', 'during', 'within'],
                    'for': ['', 'to', 'with', 'from', 'about'],
                    'with': ['', 'for', 'to', 'from', 'by'],
                    'to': ['', 'for', 'from', 'towards', 'toward'],
                    'and': ['', 'but', 'or', 'so', 'yet'],
                    'but': ['', 'however', 'yet', 'still', 'although'],
                    'or': ['', 'and', 'but', 'nor', 'yet'],
                    'so': ['', 'thus', 'therefore', 'hence', 'accordingly'],
                }
                
                if first_word in variations:
                    # Try variations until one works
                    for variation in variations[first_word]:
                        if variation == '':
                            # Remove first word
                            new_sentence = ' '.join(words[1:])
                            if new_sentence and new_sentence[0].islower():
                                new_sentence = new_sentence[0].upper() + new_sentence[1:]
                            sentence = new_sentence
                            break
                        else:
                            # Replace with variation
                            words[0] = variation
                            new_sentence = ' '.join(words)
                            if new_sentence and new_sentence[0].islower():
                                new_sentence = new_sentence[0].upper() + new_sentence[1:]
                            sentence = new_sentence
                            break
            
            # Track this opening
            opening_history.append(first_word)
            # Keep only last 5 in history
            if len(opening_history) > 5:
                opening_history.pop(0)
            
            varied.append(sentence)
        
        return ' '.join(varied)
    
    @staticmethod
    def comprehensive_enhancement(text: str) -> str:
        """
        Apply ALL enhancement techniques in optimal order
        This maximizes human-like characteristics
        """
        # Step 1: Remove AI clichés
        text = EnhancedPreprocessor.remove_ai_cliches_advanced(text)
        
        # Step 2: Syntactic restructuring
        text = EnhancedPreprocessor.syntactic_restructuring(text)
        
        # Step 3: Enhance burstiness dramatically
        text = EnhancedPreprocessor.enhance_burstiness_dramatic(text)
        
        # Step 4: Add contextual variations
        text = EnhancedPreprocessor.add_contextual_variations(text)
        
        # Step 5: Vary sentence openings
        text = EnhancedPreprocessor.vary_sentence_openings(text)
        
        # Step 6: Inject linguistic noise
        text = EnhancedPreprocessor.inject_linguistic_noise_advanced(text)
        
        # Step 7: Final cleanup
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
        
        return text.strip()
