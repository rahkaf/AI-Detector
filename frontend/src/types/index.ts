export interface TextMetrics {
  perplexity: number;
  burstiness: number;
  bigram_entropy: number;
  trigram_entropy: number;
  pos_entropy: number;
  semantic_coherence: number;
  stylometric_features: {
    avg_word_length: number;
    avg_sentence_length: number;
    lexical_density: number;
    function_word_ratio: number;
    punctuation_diversity: number;
  };
  repetitive_patterns: {
    repeated_trigrams: number;
    repeated_sentence_starts: number;
    overused_words: number;
    repetition_score: number;
  };
  composite_score: number;
  detection_resistance: string;
  word_count: number;
  sentence_count: number;
}

export interface HumanizeResult {
  text: string;
  original_text?: string;
  metrics: TextMetrics;
  model?: string;
  score?: number;
  strategy?: string;
  processing_time?: number;
  chunks_processed?: number;
}

export interface Variation {
  text: string;
  model: string;
  metrics: TextMetrics;
  score: number;
}

export interface ComparisonResult {
  original: TextMetrics;
  humanized: TextMetrics;
  improvements: {
    perplexity: number;
    burstiness: number;
    bigram_entropy: number;
    trigram_entropy: number;
    pos_entropy: number;
    semantic_coherence: number;
    composite_score: number;
  };
  improvement_percentage: {
    perplexity: number;
    burstiness: number;
    composite_score: number;
  };
}

export enum AppState {
  IDLE = 'IDLE',
  PROCESSING = 'PROCESSING',
  COMPLETED = 'COMPLETED',
  ERROR = 'ERROR',
  HISTORY = 'HISTORY',
  SETTINGS = 'SETTINGS'
}

export interface HistoryItem {
  id: string;
  timestamp: number;
  original: string;
  humanized: string;
  metrics: TextMetrics;
  strategy: string;
}

export type Strategy = 'weighted' | 'diverse' | 'mixed' | 'best' | 'advanced_blend';
