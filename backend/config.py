import os
from dotenv import load_dotenv

load_dotenv()

# Set HuggingFace download timeout
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '600'  # 10 minutes

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Model settings - Using PARAPHRASING-TRAINED models
    BART_MODEL = "eugenesiow/bart-paraphrase"  # BART trained for paraphrasing
    T5_MODEL = "Vamsi/T5_Paraphrase_Paws"  # T5 trained on PAWS paraphrase dataset
    PEGASUS_MODEL = "tuner007/pegasus_paraphrase"  # Pegasus trained for paraphrasing
    
    # Generation parameters - AGGRESSIVE settings for maximum diversity
    MAX_LENGTH = 1024
    MIN_LENGTH = 10
    NUM_BEAMS = 5  # Lower beams = more diversity
    NUM_RETURN_SEQUENCES = 3
    
    # CRITICAL: High temperature + nucleus sampling for unpredictable outputs
    TEMPERATURE = 1.8  # Very high for maximum creativity (normal is 1.0)
    TOP_K = 150  # More word choices
    TOP_P = 0.98  # High nucleus sampling for diverse vocabulary
    
    # Processing settings
    BATCH_SIZE = 1
    DEVICE = "cuda" if os.getenv('USE_GPU', 'False').lower() == 'true' else "cpu"
    
    # API settings
    MAX_TEXT_LENGTH = 10000
    RATE_LIMIT = "100 per hour"
    
    # Scoring weights for ensemble selection (updated for advanced metrics)
    PERPLEXITY_WEIGHT = 0.25
    BURSTINESS_WEIGHT = 0.25
    BIGRAM_ENTROPY_WEIGHT = 0.15
    TRIGRAM_ENTROPY_WEIGHT = 0.10
    POS_ENTROPY_WEIGHT = 0.10
    COHERENCE_WEIGHT = 0.10
    REPETITION_WEIGHT = 0.05
    
    # Default strategy for humanization
    DEFAULT_STRATEGY = "advanced_blend"
    
    # Iterative humanization settings
    TARGET_SCORE = 75.0  # Minimum composite score to pass
    MAX_ITERATIONS = 3  # Maximum refinement iterations
