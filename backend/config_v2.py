import os
from dotenv import load_dotenv

load_dotenv()

# Set HuggingFace download timeout
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '600'  # 10 minutes

class Config:
    """Application configuration for Advanced AI Humanization System"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Model settings - Using PARAPHRASING-TRAINED models
    BART_MODEL = "eugenesiow/bart-paraphrase"  # BART trained for paraphrasing
    T5_MODEL = "Vamsi/T5_Paraphrase_Paws"  # T5 trained on PAWS paraphrase dataset
    PEGASUS_MODEL = "tuner007/pegasus_paraphrase"  # Pegasus trained for paraphrasing
    
    # ADVANCED Generation parameters - Optimized for detection evasion
    MAX_LENGTH = 1024
    MIN_LENGTH = 10
    NUM_BEAMS = 5  # Lower beams = more diversity
    NUM_RETURN_SEQUENCES = 3
    
    # CRITICAL: High temperature + nucleus sampling for unpredictable outputs
    # These settings are optimized to bypass Originality.ai and GPTZero
    TEMPERATURE = 2.0  # Very high for maximum creativity
    TOP_K = 200  # More word choices
    TOP_P = 0.99  # High nucleus sampling for diverse vocabulary
    
    # Processing settings
    BATCH_SIZE = 1
    DEVICE = "cuda" if os.getenv('USE_GPU', 'False').lower() == 'true' else "cpu"
    
    # API settings
    MAX_TEXT_LENGTH = 10000
    RATE_LIMIT = "100 per hour"
    
    # ADVANCED Scoring weights - Optimized for detection evasion
    # These weights are calibrated based on Originality.ai and GPTZero research
    PERPLEXITY_WEIGHT = 0.22  # Slightly reduced, GPT-2 is most accurate
    BURSTINESS_WEIGHT = 0.20  # Increased - critical for detection evasion
    BIGRAM_ENTROPY_WEIGHT = 0.12  # Important for pattern breaking
    TRIGRAM_ENTROPY_WEIGHT = 0.10  # Higher-order patterns
    POS_ENTROPY_WEIGHT = 0.10  # Part-of-speech diversity
    COHERENCE_WEIGHT = 0.08  # Lower - too much coherence is AI-like
    REPETITION_WEIGHT = 0.08  # Penalize repetitive patterns
    TYPE_TOKEN_RATIO_WEIGHT = 0.10  # Vocabulary richness
    
    # Default strategy for humanization
    DEFAULT_STRATEGY = "adaptive"
    
    # Iterative humanization settings
    TARGET_SCORE = 85.0  # Higher threshold for better evasion
    MAX_ITERATIONS = 5  # More iterations for refinement
    
    # Ultra mode settings (maximum evasion)
    ULTRA_TEMPERATURE = 2.5  # Maximum creativity
    ULTRA_TOP_K = 250  # Maximum word choices
    ULTRA_TOP_P = 0.995  # Maximum nucleus sampling
    ULTRA_NUM_VARIATIONS = 5  # More variations
    
    # Style templates
    STYLE_TEMPLATES = {
        'academic': {'formal': 0.9, 'sentence_length': 'long', 'complexity': 'high'},
        'casual': {'formal': 0.3, 'sentence_length': 'short', 'complexity': 'low'},
        'professional': {'formal': 0.7, 'sentence_length': 'medium', 'complexity': 'medium'},
        'creative': {'formal': 0.4, 'sentence_length': 'varied', 'complexity': 'medium'}
    }
    
    # Burstiness enhancement thresholds
    BURSTINESS_TARGET = 75.0  # Target burstiness score
    MIN_SENTENCE_LENGTH = 5  # Minimum acceptable sentence length
    MAX_SENTENCE_LENGTH = 30  # Maximum acceptable sentence length
    
    # Repetition detection thresholds
    MAX_2GRAM_REPETITION = 3  # Maximum allowed 2-gram repetitions
    MAX_3GRAM_REPETITION = 2  # Maximum allowed 3-gram repetitions
    MAX_4GRAM_REPETITION = 1  # Maximum allowed 4-gram repetitions
    
    # GPT-2 model settings for perplexity
    GPT2_MODEL = "gpt2"  # Use small GPT-2 for speed
    GPT2_MAX_LENGTH = 1024  # Maximum context length
    ENABLE_GPT2_CACHE = True  # Enable caching for GPT-2 calculations
    
    # Cache settings
    METRICS_CACHE_SIZE = 1000  # Number of cached metrics calculations
    
    # Advanced preprocessing settings
    AI_CLICHES_DETECTION_THRESHOLD = 0.5  # Threshold for cliché replacement
    SYNTACTIC_RESTRUCTURING_PROBABILITY = 0.3  # 30% chance to restructure sentences
    LINGUISTIC_NOISE_PROBABILITY = 0.1  # 10% chance to add noise
    
    # Ultra mode specific settings
    ULTRA_MODE_ENABLED = True  # Enable ultra mode for maximum evasion
    ULTRA_PREPROCESSING_STAGES = 3  # Number of preprocessing stages
    ULTRA_POSTPROCESSING_STAGES = 2  # Number of postprocessing stages
