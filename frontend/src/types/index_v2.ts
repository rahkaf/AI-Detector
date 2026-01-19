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
    type_token_ratio: number;
  };
  repetitive_patterns: {
    2gram_repetition: number;
    3gram_repetition: number;
    4gram_repetition: number;
    repeated_sentence_starts: number;
    overused_words: number;
    repetition_score: number;
  };
  composite_score: number;
  detection_resistance: 'VERY HIGH' | 'HIGH' | 'MEDIUM-HIGH' | 'MEDIUM' | 'LOW';
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
  iterations?: number;
  text_analysis?: TextAnalysis;
  mode?: 'standard' | 'ultra';
  description?: string;
  input_words?: number;
  output_words?: number;
  length_ratio?: number;
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
  SETTINGS = 'SETTINGS',
  ANALYSIS = 'ANALYSIS'
}

export interface HistoryItem {
  id: string;
  timestamp: number;
  original: string;
  humanized: string;
  metrics: TextMetrics;
  strategy: string;
  mode?: 'standard' | 'ultra';
}

export type Strategy = 'weighted' | 'diverse' | 'mixed' | 'best' | 'advanced_blend' | 'adaptive' | 'cascade' | 'style_transfer';

export interface TextAnalysis {
  word_count: number;
  avg_word_length: number;
  sentence_count: number;
  avg_sentence_length: number;
  vocabulary_diversity: number;
  category: 'academic' | 'casual' | 'professional' | 'creative';
}

export interface ProcessMode {
  value: 'standard' | 'ultra';
  label: string;
  description: string;
  processingTime: string;
  recommended: boolean;
}

export const PROCESS_MODES: ProcessMode[] = [
  {
    value: 'standard',
    label: 'Standard Mode',
    description: 'Fast processing with good evasion capabilities',
    processingTime: '30-60 seconds',
    recommended: true
  },
  {
    value: 'ultra',
    label: 'Ultra Mode',
    description: 'Maximum detection evasion with multi-stage enhancement',
    processingTime: '2-5 minutes',
    recommended: false
  }
];

export const STRATEGY_DESCRIPTIONS: Record<Strategy, string> = {
  'weighted': 'Balanced scoring across all metrics',
  'diverse': 'Maximum lexical variation',
  'mixed': 'Sentence-level blending from all models',
  'best': 'Highest composite score',
  'advanced_blend': 'Intelligent ensemble blending',
  'adaptive': 'Auto-selects optimal strategy based on text analysis',
  'cascade': 'Pass outputs through multiple models',
  'style_transfer': 'Applies style matching transformations'
};
