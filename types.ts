
export interface AnalysisResult {
  similarityScore: number;
  aiLikelihood: number;
  clarityScore: number;
  grammarScore: number; // New metric
  wordCount: number;
  characterCount: number;
  flaggedSections: FlaggedSection[];
  grammarIssues: GrammarIssue[]; // New field
  sources: Source[];
  aiAnalysis: AIAnalysisDetails;
  summary: string;
}

export interface FlaggedSection {
  text: string;
  type: 'plagiarism' | 'ai';
  probability: number;
  reason: string;
  sourceUrl?: string;
}

export interface GrammarIssue {
  original: string;
  correction: string;
  type: 'grammar' | 'spelling' | 'punctuation' | 'style';
  explanation: string;
}

export interface Source {
  title: string;
  url: string;
  matchPercentage: number;
  sourceType: 'Wikipedia' | 'Reddit' | 'Academic' | 'News' | 'Other';
}

export interface AIAnalysisDetails {
  perplexity: string;
  burstiness: string;
  stylometricConsistency: string;
  conclusion: string;
}

export enum AppState {
  IDLE = 'IDLE',
  UPLOADING = 'UPLOADING',
  ANALYZING = 'ANALYZING',
  COMPLETED = 'COMPLETED',
  REFining = 'REFINING',
  ERROR = 'ERROR',
  HISTORY = 'HISTORY',
  SETTINGS = 'SETTINGS'
}

export interface HistoryItem {
  id: string;
  fileName: string;
  timestamp: number;
  result: AnalysisResult;
  rawText: string;
}

export interface WritingSuggestion {
  original: string;
  suggested: string;
  reason: string;
}
