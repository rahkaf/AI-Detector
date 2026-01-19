import axios from 'axios';
import { HumanizeResult, TextMetrics, ComparisonResult, Strategy } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes for model processing (first run takes longer)
});

export const humanizeText = async (
  text: string,
  strategy: Strategy = 'weighted',
  numVariations: number = 3,
  returnAll: boolean = false,
  aggressiveMode: boolean = false
): Promise<HumanizeResult> => {
  const endpoint = aggressiveMode ? '/api/humanize/aggressive' : '/api/humanize';
  const response = await api.post(endpoint, {
    text,
    strategy,
    num_variations: numVariations,
    return_all: returnAll,
  });
  return response.data;
};

export const getMetrics = async (text: string): Promise<TextMetrics> => {
  const response = await api.post('/api/metrics', { text });
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
  strategy: Strategy = 'weighted'
): Promise<{ results: HumanizeResult[] }> => {
  const response = await api.post('/api/batch', {
    texts,
    strategy,
  });
  return response.data;
};

export const healthCheck = async (): Promise<{ status: string; models_loaded: boolean }> => {
  const response = await api.get('/health');
  return response.data;
};
