import axios from 'axios';
import { HumanizeResult, TextMetrics, ComparisonResult, Strategy, TextAnalysis } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 600000, // 10 minutes for advanced processing with ultra mode
});

export const humanizeText = async (
  text: string,
  strategy: Strategy = 'adaptive',
  numVariations: number = 3,
  returnAll: boolean = false,
  useGPT2: boolean = true,
  mode: 'standard' | 'ultra' = 'standard'
): Promise<HumanizeResult> => {
  const endpoint = mode === 'ultra' ? '/api/humanize/ultra' : '/api/humanize';
  const response = await api.post(endpoint, {
    text,
    strategy,
    num_variations: numVariations,
    return_all: returnAll,
    use_gpt2: useGPT2,
  });
  return response.data;
};

export const getMetrics = async (text: string, useGPT2: boolean = true): Promise<TextMetrics> => {
  const response = await api.post('/api/metrics', { text, use_gpt2: useGPT2 });
  return response.data;
};

export const compareTexts = async (
  original: string,
  humanized: string
): Promise<ComparisonResult> => {
  const response = await api.post('/api/compare', {
    original,
    humanized,
  });
  return response.data;
};

export const batchHumanize = async (
  texts: string[],
  strategy: Strategy = 'adaptive'
): Promise<{ results: HumanizeResult[] }> => {
  const response = await api.post('/api/batch', {
    texts,
    strategy,
  });
  return response.data;
};

export const analyzeText = async (text: string): Promise<{
  text_analysis: TextAnalysis;
  metrics: TextMetrics;
  recommendations: string[];
  overall_score: number;
  detection_risk: string;
}> => {
  const response = await api.post('/api/analyze', { text });
  return response.data;
};

export const healthCheck = async (): Promise<{ 
  status: string; 
  models_loaded: boolean; 
  device: string;
  version: string;
}> => {
  const response = await api.get('/health');
  return response.data;
};

export const getModelsInfo = async (): Promise<{
  models_loaded: string[];
  model_count: number;
  device: string;
  bart_model: string | null;
  t5_model: string | null;
  pegasus_model: string | null;
  strategies_available: string[];
  features: string[];
}> => {
  const response = await api.get('/api/models/info');
  return response.data;
};
