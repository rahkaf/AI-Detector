import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import AdvancedTextInput from './components/AdvancedTextInput';
import ResultsDashboard from './components/ResultsDashboard';
import { AppState, HumanizeResult, Strategy, HistoryItem } from './types/index_v2';
import { humanizeText } from './services/api_v2';

const App: React.FC = () => {
  const [state, setState] = useState<AppState>(AppState.IDLE);
  const [result, setResult] = useState<HumanizeResult | null>(null);
  const [originalText, setOriginalText] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  
  // Load history from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('humanizeai_history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Failed to load history', e);
      }
    }
  }, []);
  
  // Save history to localStorage
  useEffect(() => {
    localStorage.setItem('humanizeai_history', JSON.stringify(history));
  }, [history]);
  
  const handleHumanize = async (text: string, strategy: Strategy, mode: 'standard' | 'ultra') => {
    setOriginalText(text);
    setState(AppState.PROCESSING);
    setError(null);
    
    try {
      const humanized = await humanizeText(text, strategy, 3, false, true, mode);
      setResult(humanized);
      
      // Add to history
      const newHistoryItem: HistoryItem = {
        id: crypto.randomUUID(),
        timestamp: Date.now(),
        original: text,
        humanized: humanized.text,
        metrics: humanized.metrics,
        strategy: strategy,
        mode: mode,
      };
      setHistory(prev => [newHistoryItem, ...prev].slice(0, 50)); // Keep last 50
      
      setState(AppState.COMPLETED);
    } catch (err: any) {
      console.error('Humanization error:', err);
      setError(err.response?.data?.error || err.message || 'Failed to humanize text. Please try again.');
      setState(AppState.ERROR);
    }
  };
  
  const handleReset = () => {
    setState(AppState.IDLE);
    setResult(null);
    setError(null);
  };
  
  const loadingMessages = [
    'Initializing advanced ensemble models...',
    'Analyzing text characteristics and patterns...',
    'Generating variations with BART paraphrasing...',
    'Processing with T5 transformer...',
    'Applying PEGASUS abstractive generation...',
    'Calculating GPT-2 perplexity scores...',
    'Measuring advanced burstiness metrics...',
    'Analyzing n-gram entropy distributions...',
    'Removing 50+ AI cliché patterns...',
    'Applying syntactic restructuring...',
    'Enhancing burstiness dramatically...',
    'Injecting linguistic noise...',
    'Optimizing for maximum human-like patterns...',
    'Running iterative refinement passes...',
    'Finalizing humanized output...',
  ];
  
  const [loadingMessage, setLoadingMessage] = useState(loadingMessages[0]);
  
  useEffect(() => {
    if (state === AppState.PROCESSING) {
      let index = 0;
      const interval = setInterval(() => {
        index = (index + 1) % loadingMessages.length;
        setLoadingMessage(loadingMessages[index]);
      }, 2500); // Slower cycle for longer processing
      
      return () => clearInterval(interval);
    }
  }, [state]);
  
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <Header currentState={state} onNavigate={setState} />
      
      <main className="flex-grow container mx-auto px-4 py-8 md:py-16">
        {state === AppState.IDLE && (
          <AdvancedTextInput onHumanize={handleHumanize} isProcessing={false} />
        )}
        
        {state === AppState.PROCESSING && (
          <div className="flex flex-col items-center justify-center py-32 text-center space-y-10">
            <div className="relative">
              <div className="w-32 h-32 border-[6px] border-indigo-50 border-t-indigo-600 rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <i className="fas fa-wand-magic-sparkles text-3xl text-indigo-600 animate-pulse"></i>
              </div>
            </div>
            <div className="space-y-4">
              <h2 className="text-4xl font-black text-gray-900 tracking-tight">
                Advanced Humanization
              </h2>
              <p className="text-gray-500 max-w-md mx-auto font-medium">
                {loadingMessage}
              </p>
              <div className="flex gap-2 flex-wrap justify-center">
                {['Advanced Ensemble', 'GPT-2 Perplexity', 'Cascade Blending', 'Syntactic Restructuring', 'Burstiness Enhancement', 'Iterative Refinement'].map((feature, i) => (
                  <div key={i} className="flex items-center gap-2 bg-white px-4 py-2 rounded-xl border border-gray-200 shadow-sm">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                    <span className="text-xs font-bold text-gray-700">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {state === AppState.ERROR && (
          <div className="max-w-xl mx-auto bg-white p-12 rounded-3xl shadow-2xl text-center border border-red-50">
            <div className="w-20 h-20 bg-red-50 text-red-500 rounded-3xl flex items-center justify-center mx-auto mb-8">
              <i className="fas fa-exclamation-circle text-3xl"></i>
            </div>
            <h2 className="text-3xl font-black text-gray-900 mb-4">Processing Failed</h2>
            <p className="text-gray-500 mb-10 font-medium">{error}</p>
            <button 
              onClick={handleReset}
              className="w-full py-5 bg-gray-900 text-white rounded-2xl font-black shadow-xl hover:bg-gray-800 transition-all"
            >
              Try Again
            </button>
          </div>
        )}
        
        {state === AppState.COMPLETED && result && (
          <ResultsDashboard 
            result={result}
            originalText={originalText}
            onReset={handleReset}
          />
        )}
        
        {state === AppState.HISTORY && (
          <div className="max-w-5xl mx-auto">
            <h2 className="text-4xl font-black text-gray-900 mb-8">History</h2>
            {history.length === 0 ? (
              <div className="bg-white p-12 rounded-3xl text-center border border-gray-100">
                <i className="fas fa-clock-rotate-left text-6xl text-gray-200 mb-4"></i>
                <p className="text-gray-500 font-medium">No history yet</p>
              </div>
            ) : (
              <div className="space-y-4">
                {history.map((item) => (
                  <div key={item.id} className="bg-white p-6 rounded-2xl border border-gray-100 hover:shadow-lg transition-shadow">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <span className="text-xs font-bold text-gray-400 uppercase">
                          {new Date(item.timestamp).toLocaleString()}
                        </span>
                        <p className="text-sm text-gray-600 mt-1 line-clamp-2">{item.original.substring(0, 100)}...</p>
                      </div>
                      <div className="text-right">
                        <span className="text-lg font-black text-emerald-600">{Math.round(item.metrics.composite_score)}%</span>
                        <div className="text-xs text-gray-400 mt-1">
                          {item.mode === 'ultra' ? '🔥 Ultra' : '⚡ Standard'}
                        </div>
                        <div className="text-xs text-gray-400">
                          {item.strategy.replace('_', ' ')}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
        
        {state === AppState.ANALYSIS && (
          <div className="max-w-3xl mx-auto">
            <h2 className="text-4xl font-black text-gray-900 mb-8">Text Analysis</h2>
            <div className="bg-white p-8 rounded-3xl border border-gray-100">
              <p className="text-gray-600">Text analysis feature coming soon...</p>
            </div>
          </div>
        )}
        
        {state === AppState.SETTINGS && (
          <div className="max-w-3xl mx-auto">
            <h2 className="text-4xl font-black text-gray-900 mb-8">Settings</h2>
            <div className="bg-white p-8 rounded-3xl border border-gray-100">
              <p className="text-gray-600">Settings panel coming soon...</p>
            </div>
          </div>
        )}
      </main>
      
      <footer className="bg-white border-t border-gray-200 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-sm text-gray-500">
            <i className="fas fa-shield-halved text-indigo-600 mr-2"></i>
            Advanced AI Humanization Platform v2.0
          </p>
          <p className="text-xs text-gray-400 mt-2">
            Bypasses Originality.ai, GPTZero, Quillbot, Scribbr
          </p>
          <p className="text-xs text-gray-400 mt-2">
            Powered by Xargham | BeeNeural Pvt Ltd
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;
